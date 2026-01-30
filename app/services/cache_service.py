import hashlib
import redis
from app.core.config import settings

try:
    redis_client = redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_timeout=2
    )
    redis_client.ping()
except Exception:
    redis_client = None


def _hash_key(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()


def get_cached_search(query: str) -> str | None:
    if not redis_client:
        return None
    return redis_client.get(_hash_key(query))


def set_cached_search(query: str, value: str):
    if not redis_client:
        return
    redis_client.setex(
        _hash_key(query),
        settings.WEB_SEARCH_CACHE_TTL,
        value
    )
