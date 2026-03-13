import requests
import json

url = "http://localhost:8000/chat"
session_id = "test-session-123"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "X-Session-ID": session_id
}

print("--- Query 1 ---")
payload1 = {"query": "I want to study in London"}
r1 = requests.post(url, json=payload1, headers=headers)
print(r1.json())

print("\n--- Query 2 (Follow-up) ---")
payload2 = {"query": "What are the best universities there?"}
r2 = requests.post(url, json=payload2, headers=headers)
print(r2.json())

print("\n--- Query 3 (Follow-up) ---")
payload3 = {"query": "And what is the visa process up to 2026?"}
r3 = requests.post(url, json=payload3, headers=headers)
print(r3.json())

print("\n--- Query 4 (Testing Cache) ---")
payload4 = {"query": "I want to study in London"}
r4 = requests.post(url, json=payload4, headers=headers)
print(r4.json())
