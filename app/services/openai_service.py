from typing import Iterable
from app.core.config import client

EMBED_CACHE = {}

SYSTEM_INSTRUCTIONS = """You are Mentora, the friendly FES virtual counsellor."""

def embed_query(query: str):
    if query in EMBED_CACHE:
        return EMBED_CACHE[query]
    emb = client.embeddings.create(model="text-embedding-3-small", input=query)
    vec = emb.data[0].embedding
    EMBED_CACHE[query] = vec
    return vec

def generate_answer(user_query: str, context_text: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"User Query: {user_query}\n\nContext:\n{context_text}"},
        ],
    )
    return resp.choices[0].message.content.strip()

def generate_answer_stream(user_query: str, context_text: str) -> Iterable[str]:
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"User Query: {user_query}\n\nContext:\n{context_text}"},
        ],
    )
    for chunk in stream:
        delta = getattr(chunk.choices[0], "delta", None)
        if delta and getattr(delta, "content", None):
            yield delta.content
