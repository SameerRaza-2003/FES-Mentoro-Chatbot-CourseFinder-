
# 🧠 FES Chatbot API

An AI-powered **study-abroad counselling backend** built with **FastAPI**, **OpenAI GPT models**, **Pinecone (RAG)**, and **Tavily (live web search)**.

The system is designed to be:

* 🧠 Context-aware (RAG + conversation memory)
* 🌐 Up-to-date (live web search for policies & visas)
* 🛡️ Safe (anti-hallucination, strict source control)
* ⚡ Efficient (caching, rate limits, fast paths)
* 🌊 Streaming-ready (SSE)

---

## 🧱 Project Structure

```
app/
├── core/
│   ├── config.py                 # Env vars + OpenAI/Pinecone/Tavily setup
│   ├── cors.py                   # CORS middleware
│   ├── rate_limit.py             # Rate limiting (anti-spam)
│   ├── security.py               # Anti-scraping middleware
│   ├── system_prompt.py          # Master system prompt (FES rules + RAG + web)
│   ├── long_term_memory.py       # SQLite long-term answer cache (24h TTL)
│   └── conversation_memory.py    # Short-term conversation memory
│
├── models/
│   └── schemas.py                # Pydantic request/response schemas
│
├── routers/
│   └── chat_router.py            # Chat endpoints (/chat and /stream)
│
├── services/
│   ├── openai_service.py         # OpenAI calls (normal + streaming)
│   ├── pinecone_service.py       # Pinecone vector search
│   ├── rag_service.py            # RAG + Tavily orchestrator
│   ├── web_search_service.py     # Tavily web search (lazy + retry-safe)
│   └── cache_service.py          # Redis cache for Tavily results
│
├── utils/
│   ├── contact_utils.py          # Fast contact/branch queries
│   ├── search_utils.py           # Tavily trigger logic
│   └── followup_utils.py         # Follow-up query detection
│
├── main.py                       # FastAPI app entry point
├── requirements.txt
├── memory.db                     # SQLite DB (auto-created)
└── .example.env                  # Environment variable template
```

---

## 🧠 High-Level Flow

```
User Query
   ↓
Rate Limiting + Security
   ↓
Contact Fast Path (if applicable)
   ↓
Long-Term Cache (SQLite)
   ↓
Conversation Memory (follow-ups)
   ↓
RAG Orchestrator
   ├─ Pinecone (internal knowledge)
   ├─ Tavily (live web, when needed)
   ├─ Redis cache (web results)
   ↓
OpenAI (strict system prompt)
   ↓
Response (JSON or Streaming SSE)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd FES-Mentoro-Backend
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Create `.env` File

Rename `.example.env` to `.env` and fill in:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=fes-embeddings-data
PINECONE_ENV=us-east-1
PINECONE_NAMESPACE=__default__

# Tavily (Live Web Search)
TAVILY_API_KEY=your_tavily_api_key_here

# Redis (Web cache)
REDIS_URL=redis://localhost:6379
WEB_SEARCH_CACHE_TTL=86400
WEB_SEARCH_TIMEOUT=6
```

> ℹ️ Tavily is optional.
> If `TAVILY_API_KEY` is missing, the system still runs (web search disabled).

---

### 4️⃣ Run the Server

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

API:
👉 [http://localhost:8000](http://localhost:8000)
Docs:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧩 Core Features

### ✅ Chat Endpoints

* `POST /chat`
  Standard JSON responses with memory & caching

* `GET /stream?q=...`
  Real-time SSE streaming responses

---

### 🧠 RAG + Live Web Search

* **Pinecone**

  * Universities
  * Programs
  * Blogs
  * FES knowledge

* **Tavily**

  * Visa rules
  * Policy updates
  * Deadlines
  * Official announcements

Triggered only when queries imply **fresh or time-sensitive information**.

---

### 💾 Caching Strategy

#### 1️⃣ Long-Term Memory (SQLite)

* Stored in `memory.db`
* 24-hour TTL
* Prevents repeated OpenAI calls
* Persists across restarts

#### 2️⃣ Web Search Cache (Redis)

* Caches Tavily results
* Reduces latency & cost

---

### 🗣️ Conversation Memory

* Maintains recent user–assistant turns
* Enables natural follow-ups:

  * “tell me more”
  * “continue”
  * “explain further”

---

### ⚡ Fast Paths

* Contact & branch queries
* Instant responses
* No LLM, no web search, no vector search

---

### 🛡️ Safety & Governance

* Strict system prompt
* No hallucinations
* No invented universities or policies
* Deterministic fallback response
* Rate limiting via `slowapi`
* Anti-scraping protection
* Controlled CORS

---

## 🧪 Testing Philosophy

Designed for testing via:

* Swagger (`/docs`)
* Browser (SSE)
* Frontend (React + EventSource)

Test areas:

* RAG-only queries
* Web-enhanced queries
* Cache hits
* Follow-up handling
* Streaming stability
* Contact fast path

---

