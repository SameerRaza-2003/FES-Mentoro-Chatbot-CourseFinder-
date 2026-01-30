def needs_web_search(query: str) -> bool:
    """
    Determines whether the query requires live web data.
    Keep this conservative to control costs.
    """

    keywords = [
        "latest",
        "current",
        "now",
        "today",
        "2025",
        "2026",
        "deadline",
        "update",
        "recent",
        "ranking",
        "visa",
        "policy",
        "rules",
        "changes"
    ]

    q = query.lower()
    return any(keyword in q for keyword in keywords)
