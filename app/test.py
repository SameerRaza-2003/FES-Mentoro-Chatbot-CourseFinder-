import requests
import json

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/chat"

data = {
    "query": "fes lahore contact"
}

headers = {
    "User-Agent": "Mozilla/5.0",  # Must not match blocked agents
    "Content-Type": "application/json"
}

print(f"Sending POST request to {BASE_URL}{ENDPOINT}...")

try:
    response = requests.post(BASE_URL + ENDPOINT, headers=headers, json=data)
    response.raise_for_status() 

    print("--- Response Received ---")
    print(json.dumps(response.json(), indent=4))

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
