from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat_router

app = FastAPI(title="FES Chatbot API (RAG + SSE)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(chat_router.router)

@app.get("/")
def root():
    return {"message": "FES Chatbot API running!"}
