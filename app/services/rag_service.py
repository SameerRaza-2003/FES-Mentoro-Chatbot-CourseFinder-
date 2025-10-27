import re
from app.services.openai_service import embed_query
from app.services.pinecone_service import pinecone_search

def build_context(matches, max_intro_chars: int = 300) -> str:
    lines = []
    for m in matches:
        meta = m["metadata"] or {}
        title = meta.get("title") or meta.get("slug") or "Untitled"
        chunk = meta.get("chunk") or meta.get("content") or ""
        snippet = re.sub(r"\s+", " ", chunk).strip()[:1000]
        lines.append(f"[Blog: {title}] (Score: {m['score']:.4f})\n{snippet}\n" + "-" * 40)
    return "\n".join(lines)

def run_rag(query: str, top_k: int = 3):
    qvec = embed_query(query)
    return pinecone_search(qvec, top_k)
