from app.core.config import client
from app.services.pinecone_service import get_index


def search_courses(query: str, answers: dict, top_k: int = 40):
    # Generate embedding
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    index = get_index("courses-data")

    # Build Pinecone filters
    pinecone_filter = {}

    if answers.get("country"):
        pinecone_filter["country"] = {"$eq": answers["country"]}
    if answers.get("discipline"):
        pinecone_filter["discipline"] = {"$eq": answers["discipline"]}
    if answers.get("degree"):
        pinecone_filter["degree"] = {"$eq": answers["degree"]}
    if answers.get("study_level"):
        pinecone_filter["study_level"] = {"$eq": answers["study_level"]}
    if answers.get("duration"):
        pinecone_filter["duration"] = {"$eq": answers["duration"]}
    if answers.get("budget"):
        try:
            pinecone_filter["course_fee"] = {"$lt": float(answers["budget"])}
        except ValueError:
            pass

    # Query with filters
    results = index.query(
        vector=embedding,
        top_k=top_k,
        filter=pinecone_filter if pinecone_filter else None,
        include_metadata=True
    )

    matches = [
        {
            "id": m["id"],
            "score": m["score"],
            **m["metadata"]
        }
        for m in results["matches"]
    ]

    # Fallback if no filtered results
    if not matches:
        results = index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )
        matches = [
            {
                "id": m["id"],
                "score": m["score"],
                **m["metadata"]
            }
            for m in results["matches"]
        ]

    return matches
