from typing import AsyncGenerator
from app.core.config import client

EMBED_CACHE = {}

SYSTEM_INSTRUCTIONS = """You are Mentora, the friendly FES virtual counsellor.
Always provide clear, factual, and empathetic responses to user queries.
If information is missing, say so honestly and guide the user helpfully.
"""

def embed_query(query: str):
    """Generate or retrieve cached vector embedding for query."""
    if query in EMBED_CACHE:
        return EMBED_CACHE[query]

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    vec = emb.data[0].embedding
    EMBED_CACHE[query] = vec
    return vec


def generate_answer(user_query: str, context_text: str) -> str:
    """Generate a non-streaming chatbot response."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"User Query:\n{user_query}\n\nContext:\n{context_text}"}
        ],
    )
    return resp.choices[0].message.content.strip()


async def generate_answer_stream(user_query: str, context_text: str) -> AsyncGenerator[str, None]:
    """Generate a streaming chatbot response token by token."""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"User Query:\n{user_query}\n\nContext:\n{context_text}"}
        ],
    )

    for chunk in stream:
        delta = getattr(chunk.choices[0], "delta", None)
        if delta and getattr(delta, "content", None):
            yield delta.content
