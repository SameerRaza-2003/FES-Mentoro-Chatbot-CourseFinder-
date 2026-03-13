import sys
import os
sys.path.append('f:\\Work\\FES-Mentoro-Backend')

from app.services.freshness_classifier import needs_web_search

print("Testing Needs Web Search for 'uk visa policy in 2026'")
try:
    result = needs_web_search("uk visa policy in 2026")
    print(f"Result: {result}")
except Exception as e:
    print(f"Exception: {e}")
