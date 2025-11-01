from typing import Optional

CONTACT_KEYWORDS = ["contact", "phone", "email", "branch", "address", "office", "call", "number"]
CITY_HINTS = ["lahore", "karachi", "islamabad"]


def is_contact_query(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in CONTACT_KEYWORDS)


def fast_contact_response(matches: list, query: str) -> Optional[str]:
    if not matches:
        return None

    first_match = matches[0]
    meta = first_match.get("metadata", {})

    branch = meta.get("branch", "Branch")
    address = meta.get("address", "")
    phone = meta.get("phone", "")
    email = meta.get("email", "")

    # ✅ Build a nice readable response
    parts = [f"📍 {branch}", f"🏢 {address}" if address else "", f"📞 {phone}" if phone else "", f"✉️ {email}" if email else ""]
    return "\n".join([p for p in parts if p])
