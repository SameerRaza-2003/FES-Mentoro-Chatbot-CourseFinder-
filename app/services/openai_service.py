from typing import AsyncGenerator, List, Dict
from app.core.config import client
from app.core.system_prompt import SYSTEM_PROMPT

EMBED_CACHE = {}


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


def generate_answer(
    user_query: str,
    context_text: str,
    history: List[Dict[str, str]]
) -> str:
    """Generate a non-streaming chatbot response with memory."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {
            "role": "user",
            "content": (
                f"Current question:\n{user_query}\n\n"
                f"Retrieved context:\n{context_text}"
            )
        }
    ]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=messages,
    )

    return resp.choices[0].message.content.strip()


async def generate_answer_stream(
    user_query: str,
    context_text: str,
    history: List[Dict[str, str]]
) -> AsyncGenerator[str, None]:
    """Generate a streaming chatbot response with memory."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {
            "role": "user",
            "content": (
                f"Current question:\n{user_query}\n\n"
                f"Retrieved context:\n{context_text}"
            )
        }
    ]

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        stream=True,
        messages=messages,
    )

    for chunk in stream:
        delta = getattr(chunk.choices[0], "delta", None)
        if delta and getattr(delta, "content", None):
            yield delta.content
