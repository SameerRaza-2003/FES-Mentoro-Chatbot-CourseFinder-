from typing import Optional

CONTACT_KEYWORDS = ["contact", "phone", "email", "branch", "address", "office", "call", "number"]
CITY_HINTS = ["lahore", "karachi", "islamabad"]

def is_contact_query(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in CONTACT_KEYWORDS)

def fast_contact_response(matches: list, query: str) -> Optional[str]:
    if not matches: return None
    m = matches[0]
    meta = m.get("metadata", {})
    return f"{meta.get('branch', 'Branch')} - {meta.get('address', '')}"
