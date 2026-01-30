import asyncio
from tenacity import retry, stop_after_attempt, wait_fixed
from tavily import TavilyClient

from app.core.config import settings

# =========================
# Lazy / Safe Tavily Client
# =========================

_tavily_client = None

def get_tavily_client():
    global _tavily_client

    if _tavily_client:
        return _tavily_client

    if not settings.TAVILY_API_KEY:
        return None

    _tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    return _tavily_client


# =========================
# Web Search Function
# =========================

@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
async def web_search(query: str, max_results: int = 4) -> str:
    """
    Performs a live web search using Tavily.
    Safe if Tavily is disabled.
    """

    client = get_tavily_client()
    if not client:
        return ""

    loop = asyncio.get_event_loop()

    def _search():
        return client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )

    response = await loop.run_in_executor(None, _search)

    results = []
    for r in response.get("results", []):
        results.append(
            f"Title: {r.get('title')}\n"
            f"URL: {r.get('url')}\n"
            f"Content: {r.get('content')}\n"
        )

    return "\n".join(results)
