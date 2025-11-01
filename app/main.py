from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routers import chat_router
from app.core.cors import setup_cors
from app.core.rate_limit import setup_rate_limiter
from app.core.security import block_scrapers

# --- App setup ---
app = FastAPI(title="FES Chatbot API (RAG + SSE)")

# --- Global Middleware & Configs ---
setup_cors(app)
setup_rate_limiter(app)
app.middleware("http")(block_scrapers)

# --- Routers ---
app.include_router(chat_router.router)

# --- Health Endpoint ---
@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "FES Chatbot API running!"}
