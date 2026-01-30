import time
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from app.models.schemas import ChatRequest
from app.services.openai_service import (
    generate_answer,
    generate_answer_stream
)

from app.core.long_term_memory import (
    get_cached_response,
    set_cached_response,
)

from app.services.rag_service import (
    run_rag,
    build_final_context
)

from app.services.freshness_classifier import (
    needs_web_search
)

from app.utils.contact_utils import (
    is_contact_query,
    fast_contact_response
)

from app.core.conversation_memory import (
    add_message,
    get_history
)

from app.core.rate_limit import limiter


router = APIRouter(tags=["Chat"])


# =========================
# REGULAR CHAT ENDPOINT
# =========================
@router.post("/chat")
@limiter.limit("5/minute")
async def chat(req: ChatRequest, request: Request):
    start = time.time()

    session_id = (
        request.headers.get("X-Session-ID")
        or (request.client.host if request.client else "anonymous")
    )

    try:
        # Fast contact path (cheap, no LLM, no web)
        matches = run_rag(req.query, 3)
        if is_contact_query(req.query):
            fast = fast_contact_response(matches, req.query)
            if fast:
                set_cached_response(req.query, fast, "contact")
                return {
                    "response": fast,
                    "cached": True,
                    "used_web": False
                }

        # Long-term answer cache
        cached = get_cached_response(req.query)
        if cached:
            return {
                "response": cached,
                "cached": True,
                "used_web": False
            }

        # Short-term conversation memory
        add_message(session_id, "user", req.query)
        history = get_history(session_id)[-5:]

        # Semantic decision for web search
        allow_web = needs_web_search(req.query)

        # Build final context
        context, sources = await build_final_context(
            req.query,
            allow_web=allow_web
        )

        # Single main LLM call
        answer = generate_answer(
            req.query,
            context,
            history
        )

        # Append real sources if web was used
        if allow_web and sources:
            sources_text = "\n\nSources:\n"
            for s in sources:
                sources_text += f"- {s['title']}: {s['url']}\n"
            answer += sources_text

        # Store assistant response
        add_message(session_id, "assistant", answer)
        set_cached_response(req.query, answer, "general")

        return {
            "response": answer,
            "elapsed_time": round(time.time() - start, 2),
            "cached": False,
            "used_web": allow_web
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Chat processing failed: {str(e)}"},
        )


# =========================
# STREAMING CHAT ENDPOINT
# =========================
@router.get("/stream")
@limiter.limit("5/minute")
async def stream(request: Request, q: str):
    start = time.time()

    session_id = (
        request.headers.get("X-Session-ID")
        or (request.client.host if request.client else "anonymous")
    )

    async def event_generator():
        try:
            # Fast contact path
            matches = run_rag(q, 3)
            if is_contact_query(q):
                fast = fast_contact_response(matches, q)
                if fast:
                    yield {"event": "message", "data": fast}
                    yield {"event": "meta", "data": "used_web=false"}
                    yield {"event": "message", "data": "[DONE]"}
                    return

            # Short-term memory
            add_message(session_id, "user", q)
            history = get_history(session_id)[-5:]

            # Semantic decision for web search
            allow_web = needs_web_search(q)

            # Build final context
            context, sources = await build_final_context(
                q,
                allow_web=allow_web
            )

            full_response = ""

            # Stream LLM output
            async for token in generate_answer_stream(q, context, history):
                full_response += token
                yield {"event": "message", "data": token}
                await asyncio.sleep(0)

            # Append sources at the end if web was used
            if allow_web and sources:
                yield {"event": "message", "data": "\n\nSources:\n"}
                for s in sources:
                    yield {
                        "event": "message",
                        "data": f"- {s['title']}: {s['url']}\n"
                    }

            # Store assistant response
            add_message(session_id, "assistant", full_response)

            # Send meta info
            yield {
                "event": "meta",
                "data": f"used_web={str(allow_web).lower()}"
            }
            yield {"event": "message", "data": "[DONE]"}

        except Exception as e:
            yield {"event": "error", "data": f"Stream error: {str(e)}"}
            yield {"event": "message", "data": "[DONE]"}

    return EventSourceResponse(event_generator())
