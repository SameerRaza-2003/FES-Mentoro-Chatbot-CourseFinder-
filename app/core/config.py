import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# --- Load environment variables ---
load_dotenv()

# =========================
# Core Keys
# =========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_INDEX = os.getenv("PINECONE_INDEX", "fes-embeddings-data")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "__default__")

# =========================
# NEW: Tavily + Cache
# =========================
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
WEB_SEARCH_CACHE_TTL = int(os.getenv("WEB_SEARCH_CACHE_TTL", 86400))
WEB_SEARCH_TIMEOUT = int(os.getenv("WEB_SEARCH_TIMEOUT", 6))

# --- Validate required keys ---
if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise RuntimeError("❌ Missing OPENAI_API_KEY or PINECONE_API_KEY in environment")

if not TAVILY_API_KEY:
    print("⚠️  WARNING: TAVILY_API_KEY not set. Web search will be disabled.")

# --- Initialize Clients ---
client = OpenAI(api_key=OPENAI_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

print(f"✅ Connected to Pinecone index: {PINECONE_INDEX} (namespace: {PINECONE_NAMESPACE})")

# =========================
# NEW: settings object (compat layer)
# =========================
class _Settings:
    TAVILY_API_KEY = TAVILY_API_KEY
    REDIS_URL = REDIS_URL
    WEB_SEARCH_CACHE_TTL = WEB_SEARCH_CACHE_TTL
    WEB_SEARCH_TIMEOUT = WEB_SEARCH_TIMEOUT


settings = _Settings()

# --- Export ---
__all__ = [
    "client",
    "index",
    "PINECONE_NAMESPACE",
    "settings",
]
