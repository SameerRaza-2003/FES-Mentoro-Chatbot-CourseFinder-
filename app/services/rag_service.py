import re
import asyncio
from typing import Tuple, List, Dict

from app.services.openai_service import embed_query
from app.services.pinecone_service import pinecone_search
from app.services.web_search_service import web_search
from app.services.cache_service import (
    get_cached_search,
    set_cached_search
)


# =========================
# CONTEXT BUILDERS
# =========================

def build_context(matches, max_intro_chars: int = 1000) -> str:
    """
    Builds readable context from Pinecone matches.
    """
    lines = []

    for m in matches:
        meta = m.get("metadata", {}) or {}
        title = meta.get("title") or meta.get("slug") or "Untitled"
        chunk = meta.get("chunk") or meta.get("content") or ""
        snippet = re.sub(r"\s+", " ", chunk).strip()[:max_intro_chars]

        lines.append(
            f"[Doc: {title}]\n{snippet}"
        )

    return "\n\n".join(lines)


# =========================
# SYNC RAG (CONTACT FAST PATH)
# =========================

def run_rag(query: str, top_k: int = 3):
    """
    Synchronous RAG for cheap contact lookups.
    """
    query_vector = embed_query(query)
    return pinecone_search(query_vector, top_k)


# =========================
# ASYNC RAG (MAIN PIPELINE)
# =========================

async def run_rag_async(query: str, top_k: int = 3) -> str:
    """
    Async-safe wrapper around Pinecone RAG.
    Runs blocking work off the event loop.
    """
    loop = asyncio.get_event_loop()

    def _rag():
        query_vector = embed_query(query)
        matches = pinecone_search(query_vector, top_k)
        return build_context(matches)

    return await loop.run_in_executor(None, _rag)


# =========================
# FINAL CONTEXT ORCHESTRATOR
# =========================

async def build_final_context(
    query: str,
    allow_web: bool = False
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Builds final LLM context.

    - Internal knowledge (Pinecone RAG) is always used
    - Web search (Tavily) is used only if allow_web=True
    - Returns (context_text, sources)
    """

    # Run RAG in parallel
    rag_task = asyncio.create_task(run_rag_async(query))

    web_context = ""
    sources: List[Dict[str, str]] = []

    if allow_web:
        cached = get_cached_search(query)

        if cached:
            web_context = cached.get("content", "")
            sources = cached.get("sources", [])
        else:
            try:
                results = await web_search(query)

                # Expected normalized structure:
                # {
                #   "content": "...",
                #   "sources": [{"title": "...", "url": "..."}]
                # }

                web_context = results.get("content", "")
                sources = results.get("sources", [])

                set_cached_search(query, {
                    "content": web_context,
                    "sources": sources
                })

            except Exception:
                web_context = ""
                sources = []

    rag_context = await rag_task

    context_text = f"""
### Internal Knowledge Base
{rag_context}

### Live Internet Sources
{web_context}
""".strip()

    return context_text, sources
