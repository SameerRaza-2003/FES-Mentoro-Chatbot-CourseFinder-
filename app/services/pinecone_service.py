from app.core.config import index, PINECONE_NAMESPACE


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
