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


from app.services.rag_service import run_rag, build_context
from app.utils.contact_utils import is_contact_query, fast_contact_response
from app.core.conversation_memory import add_message, get_history
from app.core.rate_limit import limiter

router = APIRouter(tags=["Chat"])


# =========================
# 🟢 REGULAR CHAT ENDPOINT
# =========================
@router.post("/chat")
@limiter.limit("5/minute")
def chat(req: ChatRequest, request: Request):
    start = time.time()
    session_id = request.client.host

    try:
        # ⚡ FAST CONTACT PATH
        matches = run_rag(req.query, 3)
        if is_contact_query(req.query):
            fast = fast_contact_response(matches, req.query)
            if fast:
                set_cached_response(req.query, fast, "contact")
                return {"response": fast, "cached": True}

        # 🧠 LONG-TERM ANSWER CACHE (SAFE)
        cached = get_cached_response(req.query)
        if cached:
            return {"response": cached, "cached": True}

        if not matches:
            return {"response": "No relevant info found."}

        # 🧠 SHORT-TERM MEMORY
        add_message(session_id, "user", req.query)

        context = build_context(matches)
        history = get_history(session_id)

        answer = generate_answer(req.query, context, history)

        add_message(session_id, "assistant", answer)

        # 💾 STORE FINAL ANSWER
        set_cached_response(req.query, answer, "general")

        return {
            "response": answer,
            "elapsed_time": round(time.time() - start, 2),
            "cached": False,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Chat processing failed: {str(e)}"},
        )

# =========================
# 🌊 STREAMING CHAT ENDPOINT
# =========================
@router.get("/stream")
@limiter.limit("5/minute")
async def stream(request: Request, q: str):
    session_id = request.client.host
    start = time.time()

    try:
        matches = run_rag(q, 3)

        async def event_generator():
            try:
                if not matches:
                    yield {"event": "message", "data": "No relevant info found."}
                    yield {"event": "message", "data": "[DONE]"}
                    return

                # ⚡ FAST CONTACT PATH (NO MEMORY)
                if is_contact_query(q):
                    fast = fast_contact_response(matches, q)
                    if fast:
                        yield {"event": "message", "data": fast}
                        yield {"event": "message", "data": "[DONE]"}
                        return

                # 🧠 MEMORY: store user message
                add_message(session_id, "user", q)

                context = build_context(matches)
                history = get_history(session_id)

                full_response = ""

                async for token in generate_answer_stream(q, context, history):
                    full_response += token
                    yield {"event": "message", "data": token}
                    await asyncio.sleep(0)

                # 🧠 MEMORY: store assistant response
                add_message(session_id, "assistant", full_response)

                yield {
                    "event": "message",
                    "data": f"[Retrieved {len(matches)} chunks | {time.time()-start:.2f}s]"
                }
                yield {"event": "message", "data": "[DONE]"}

            except Exception as e:
                yield {"event": "error", "data": f"Stream error: {str(e)}"}
                yield {"event": "message", "data": "[DONE]"}

        return EventSourceResponse(event_generator())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
