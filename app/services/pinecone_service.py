from app.core.config import index, pc, PINECONE_NAMESPACE

# Cache for non-chat indexes (courses, future features)
_INDEX_CACHE = {}


# ======================================================
# Chatbot RAG search (USES EXISTING CHAT INDEX)
# ======================================================
def pinecone_search(query_vector, top_k: int = 3):
    res = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE,
    )

    matches = getattr(res, "matches", []) or []
    return [
        {
            "id": m.id,
            "score": m.score,
            "metadata": m.metadata or {},
        }
        for m in matches
    ]


# ======================================================
# Generic index getter (FOR COURSE FINDER)
# ======================================================
def get_index(index_name: str):
    """
    Return a cached Pinecone index instance by name.
    """
    if index_name not in _INDEX_CACHE:
        _INDEX_CACHE[index_name] = pc.Index(index_name)
    return _INDEX_CACHE[index_name]
