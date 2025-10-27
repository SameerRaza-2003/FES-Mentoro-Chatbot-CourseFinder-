import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone 

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "fes-embeddings-data")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "__default__")

# Validate keys
if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise RuntimeError("❌ Missing API keys in environment/.env")


client = OpenAI(api_key=OPENAI_API_KEY)


pc = Pinecone(api_key=PINECONE_API_KEY)


index = pc.Index(INDEX_NAME)

print(f"✅ Connected to Pinecone index: {INDEX_NAME}")

__all__ = ["client", "index", "PINECONE_NAMESPACE"]