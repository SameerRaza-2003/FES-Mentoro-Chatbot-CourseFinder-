

# 🧠 FES Chatbot API

An AI-powered study-abroad counselling backend built with **FastAPI**, **OpenAI GPT models**, and **Pinecone** (RAG-based).
Supports both standard and streaming chat responses.

---

## 🧱 Project Structure

```
app/
├── core/
│   ├── config.py          # Loads environment variables and settings
│   ├── cors.py            # CORS middleware setup
│   ├── rate_limit.py      # Request rate limiter (anti-spam)
│   └── security.py        # Anti-scraping middleware
    └── system_prompt.py        # contains base prompt
│
├── models/
│   └── schemas.py         # Pydantic models for request/response validation
│
├── routers/
│   └── chat_router.py     # Chat endpoints (/chat and /stream)
│
├── services/
│   ├── openai_service.py  # Handles OpenAI API (sync + streaming)
│   ├── pinecone_service.py# Initializes and manages Pinecone client
│   └── rag_service.py     # RAG: retrieves and builds contextual knowledge
│
├── utils/
│   └── contact_utils.py   # Detects contact queries and returns branch info
│
├── main.py                # FastAPI entry point
├── requirements.txt       
└── .example.env           # Example environment variables file
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Create `.env` File

rename `.example.env` to `.env` and fill in your credentials:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=fes-embeddings-data
PINECONE_ENV=us-east1-gcp
PINECONE_NAMESPACE=__default__
```

### 4️⃣ Run the Server from the root folder

```bash
python -m uvicorn app.main:app --reload
```

Your API will be available at:
👉 [http://localhost:8000](http://localhost:8000)

---

## 🧩 Features

### ✅ Chat Endpoints

* `/chat`: Standard JSON chat response
* `/stream`: Real-time SSE streaming response

### 🧠 RAG Integration

* Retrieves relevant context from Pinecone
* Passes context to OpenAI for enriched, factual replies

### 🛡️ Security & Limits

* **Rate limiting** (via `slowapi`) to prevent abuse
* **Anti-scraping** middleware blocks bot-like agents
* **CORS restrictions** to secure allowed origins

### 🧱 Modular Design

Each component (RAG, OpenAI, Pinecone, CORS, Security) is isolated for clarity and reusability. You can consult the project structure.
