

# 🧠 FES Chatbot API (RAG + Streaming Chat)

This repository hosts the **FES Chatbot API**, also known as **Mentora** — an AI-powered study-abroad counsellor built for **FES Pakistan**.
It uses **Retrieval-Augmented Generation (RAG)** with **Pinecone** for vector search and **OpenAI GPT models** for contextual chat responses.

---

## 🚀 Overview

**Mentora** is a FastAPI-based backend that provides two main endpoints:

1. `/chat` → Non-streaming JSON response (for debugging or API testing)
2. `/stream` → Streaming chat responses via **Server-Sent Events (SSE)** for smooth frontend integration (e.g., React, Flutter, etc.)

The system combines:

* 🔍 **Pinecone Vector Database** for context retrieval
* 💬 **OpenAI GPT-4o-mini** for intelligent, structured replies
* 🌐 **FastAPI** for fast and reliable API serving
* 🔄 **SSE Streaming** for real-time token generation

---

## 🧩 Features

✅ **RAG-based Query Handling** — Combines vector search and GPT for context-aware answers
✅ **Smart Contact Detection** — Instantly returns FES branch details for contact-related queries
✅ **Structured University Info** — Returns university data in a friendly, readable format
✅ **Streaming Responses** — Token-by-token generation for chat-like UX
✅ **Caching Layer** — Speeds up repeated embedding calls
✅ **CORS Enabled** — Ready for frontend integration

---

## 🏗️ Architecture

```
+-----------------------------+
|          User Query         |
+-------------+---------------+
              |
              v
     ┌─────────────────────┐
     │ OpenAI Embeddings   │ ← Generates vector for query
     └─────────┬───────────┘
               |
               v
     ┌─────────────────────┐
     │ Pinecone Vector DB  │ ← Retrieves top matching context chunks
     └─────────┬───────────┘
               |
               v
     ┌─────────────────────┐
     │ Context Builder     │ ← Formats metadata for GPT
     └─────────┬───────────┘
               |
               v
     ┌─────────────────────┐
     │ GPT-4o-mini Model   │ ← Generates final response
     └─────────────────────┘
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/fes-chatbot-api.git
cd fes-chatbot-api
```

### 2️⃣ Install Dependencies

Make sure you have **Python 3.9+**. Then:

```bash
pip install -r requirements.txt
```


### 3️⃣ Create `.env` File

In the project root, add:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=us-east1-gcp
PINECONE_INDEX=fes-embeddings-data
PINECONE_NAMESPACE=__default__
```

---

## ▶️ Run the Server

Run locally with **Uvicorn**:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Your API will be live at:
👉 [http://localhost:8000](http://localhost:8000)

---

## 🔌 API Endpoints

### 1️⃣ `/chat` — Non-streaming (JSON)

**POST**

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "universities in the UK"}'
```

**Response Example:**

```json
{
  "response": "🎓 University of Glasgow...\n\n[Retrieved 3 chunks | Response time: 1.52s]"
}
```

---

### 2️⃣ `/stream` — Streaming (SSE)

**GET**

```bash
curl -N "http://localhost:8000/stream?q=FES Lahore contact"
```

**Response:**
The API will stream partial messages (token-by-token) that you can display in your chat UI in real time.

---

## 🧠 System Behavior Summary

### 📞 Contact Queries

Mentora detects contact-related queries using keywords like:

> “contact”, “phone”, “branch”, “address”, “office”, “number”, etc.

It quickly returns:

* Branch name
* Address
* Phone
* Email
* Link

### 🎓 University Queries

If the query includes country/university names, the API returns structured results with:

* **🎓 Well-Known Programs**
* **🌟 Highlights**
* **🤝 How FES Can Help**

### 📰 Blog Queries

For general study-abroad guidance, Mentora uses blog data indexed in Pinecone.

---

## 🧱 File Structure

```
.
├── api.py                # Main FastAPI application
├── .env                  # Environment variables
├── requirements.txt       # Python dependencies (recommended)
└── README.md             # This file
```

---

## 💡 Customization Tips

* Adjust `SYSTEM_INSTRUCTIONS` to fine-tune tone or content format.
* Modify `top_k` in `run_rag()` to retrieve more context per query.
* Add more keywords to `CONTACT_KEYWORDS` or `CITY_HINTS` for better contact detection.
* In production, **restrict `CORS` origins** to your frontend domain.

---

## 🧰 Tech Stack

| Component           | Technology              |
| ------------------- | ----------------------- |
| **Framework**       | FastAPI                 |
| **Streaming**       | SSE via `sse-starlette` |
| **AI Model**        | OpenAI GPT-4o-mini      |
| **Vector DB**       | Pinecone                |
| **Embedding Model** | text-embedding-3-small  |
| **Language**        | Python 3.9+             |

---

## 🛡️ Notes

* Sensitive keys (`OPENAI_API_KEY`, `PINECONE_API_KEY`) must **never** be hardcoded.
* The app gracefully handles streaming errors and returns friendly fallback messages.
* `EMBED_CACHE` keeps embeddings in memory for repeated queries — restart clears it.

---

## 💬 Example Use Cases

| Query                                       | Response Type                  |
| ------------------------------------------- | ------------------------------ |
| “FES Lahore contact”                        | Instant contact details        |
| “Universities in UK”                        | List of universities under FES |
| “How to apply for scholarships in Ireland?” | Blog-based study guidance      |
| “Study visa process Canada”                 | Contextual blog advice         |

---
