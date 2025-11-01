from fastapi import Request
from fastapi.responses import JSONResponse

# --- Anti-scraping Middleware ---
async def block_scrapers(request: Request, call_next):
    user_agent = request.headers.get("User-Agent", "").lower()
    blocked_agents = ["python", "curl", "scrapy", "httpx", "wget"]

    if any(bot in user_agent for bot in blocked_agents):
        return JSONResponse(
            status_code=403,
            content={"detail": "Automated scraping not allowed"},
        )
    return await call_next(request)
