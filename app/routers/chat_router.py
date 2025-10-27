import time, asyncio
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from app.models.schemas import ChatRequest
from app.services.openai_service import generate_answer, generate_answer_stream
from app.services.rag_service import run_rag, build_context
from app.utils.contact_utils import is_contact_query, fast_contact_response

router = APIRouter(tags=["Chat"])

@router.post("/chat")
def chat(req: ChatRequest):
    start = time.time()
    try:
        matches = run_rag(req.query, 3)
        if not matches:
            return {"response": "No relevant info found."}
        if is_contact_query(req.query):
            fast = fast_contact_response(matches, req.query)
            if fast:
                return {"response": fast}
        context = build_context(matches)
        answer = generate_answer(req.query, context)
        return {"response": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/stream")
async def stream(q: str):
    async def event_generator():
        matches = run_rag(q, 3)
        for token in generate_answer_stream(q, build_context(matches)):
            yield {"event": "message", "data": token}
            await asyncio.sleep(0)
        yield {"event": "message", "data": "[DONE]"}
    return EventSourceResponse(event_generator())
