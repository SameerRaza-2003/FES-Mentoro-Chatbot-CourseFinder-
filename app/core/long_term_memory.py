import sqlite3
import time
import hashlib
import os
from typing import Optional

# ======================================================
# CONFIG (ABSOLUTE DB PATH)
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

DB_PATH = os.path.join(BASE_DIR, "memory.db")
TTL_SECONDS = 86400  # 24 hours


# ======================================================
# INTERNAL: FORCE DB + TABLE CREATION
# ======================================================
def _ensure_db() -> None:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS answer_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            query_hash TEXT NOT NULL,
            response TEXT NOT NULL,
            response_type TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_answer_query_hash
        ON answer_memory (query_hash)
    """)

    conn.commit()
    conn.close()


# 🔒 FORCE EXECUTION ON IMPORT (CRITICAL)
_ensure_db()


# ======================================================
# HELPERS
# ======================================================
def _hash_query(query: str) -> str:
    return hashlib.sha256(
        query.lower().strip().encode("utf-8")
    ).hexdigest()


# ======================================================
# READ FROM CACHE
# ======================================================
def get_cached_response(query: str) -> Optional[str]:
    _ensure_db()

    query_hash = _hash_query(query)
    now = time.time()

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        SELECT response, created_at
        FROM answer_memory
        WHERE query_hash = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (query_hash,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    response, created_at = row

    if now - created_at > TTL_SECONDS:
        return None

    return response


# ======================================================
# WRITE TO CACHE
# ======================================================
def set_cached_response(
    query: str,
    response: str,
    response_type: str
) -> None:
    _ensure_db()

    query_hash = _hash_query(query)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO answer_memory (
            query,
            query_hash,
            response,
            response_type,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        query,
        query_hash,
        response,
        response_type,
        time.time()
    ))

    conn.commit()
    conn.close()
