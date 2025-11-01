# app/core/rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

# Create limiter with default rate limit
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10/minute"],  # e.g., 10 requests per minute per IP
)

# Custom function to skip rate limiting for specific endpoints
def exempt_healthcheck(request: Request) -> bool:
    return request.url.path == "/health"

# Monkey patch: replace internal filter if present
limiter._request_filter = exempt_healthcheck
