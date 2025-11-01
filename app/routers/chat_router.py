import time
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from app.models.schemas import ChatRequest
from app.services.openai_service import generate_answer, generate_answer_stream
from app.services.rag_service import run_rag, build_context
from app.utils.contact_utils import is_contact_query, fast_contact_response
from app.core.rate_limit import limiter  # reuse global limiter

router = APIRouter(tags=["Chat"])

# --- Regular Chat Endpoint ---
@router.post("/chat")
@limiter.limit("5/minute")  # ✅ Rate limit per client IP
def chat(req: ChatRequest, request: Request):
    start = time.time()
    try:
        matches = run_rag(req.query, 3)
        if not matches:
            return {"response": "No relevant info found."}

        # ✅ Quick contact responses (e.g., branch/phone/email)
        if is_contact_query(req.query):
            fast = fast_contact_response(matches, req.query)
            if fast:
                return {"response": fast}

        # ✅ Generate RAG-based context and final answer
        context = build_context(matches)
        answer = generate_answer(req.query, context)

        return {
            "response": answer,
            "elapsed_time": round(time.time() - start, 2),
            "matches": matches,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Chat processing failed: {str(e)}"},
        )


# --- Streaming Chat Endpoint ---
@router.get("/stream")
@limiter.limit("5/minute")
async def stream(request: Request, q: str):
    try:
        matches = run_rag(q, 3)
        context = build_context(matches)

        async def event_generator():
            try:
                async for token in generate_answer_stream(q, context):
                    yield {"event": "message", "data": token}
                    await asyncio.sleep(0)
                yield {"event": "message", "data": "[DONE]"}
            except Exception as e:
                yield {"event": "error", "data": f"Stream error: {str(e)}"}

        return EventSourceResponse(event_generator())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
