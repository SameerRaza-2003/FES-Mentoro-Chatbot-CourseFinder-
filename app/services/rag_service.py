import re
from app.services.openai_service import embed_query
from app.services.pinecone_service import pinecone_search


def build_context(matches, max_intro_chars: int = 1000) -> str:
    lines = []
    for m in matches:
        meta = m.get("metadata", {}) or {}
        title = meta.get("title") or meta.get("slug") or "Untitled"
        chunk = meta.get("chunk") or meta.get("content") or ""
        snippet = re.sub(r"\s+", " ", chunk).strip()[:max_intro_chars]
        lines.append(f"[Doc: {title}] (Score: {m.get('score', 0):.4f})\n{snippet}\n" + "-" * 40)
    return "\n".join(lines)


def run_rag(query: str, top_k: int = 3):
    query_vector = embed_query(query)
    return pinecone_search(query_vector, top_k)
