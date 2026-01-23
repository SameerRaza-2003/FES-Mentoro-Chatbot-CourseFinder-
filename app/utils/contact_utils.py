from typing import Optional

CONTACT_KEYWORDS = [
    "contact", "phone", "email", "branch",
    "address", "office", "call", "number"
]

CITY_HINTS = ["lahore", "karachi", "islamabad"]


def is_contact_query(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in CONTACT_KEYWORDS)


from typing import Optional

CONTACT_KEYWORDS = [
    "contact", "phone", "email", "branch",
    "address", "office", "call", "number"
]

CITY_HINTS = [
    "lahore", "rawalpindi", "islamabad",
    "karachi", "multan", "peshawar",
    "quetta", "faisalabad"
]


def is_contact_query(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in CONTACT_KEYWORDS)


def fast_contact_response(matches: list, query: str) -> Optional[str]:
    if not matches:
        return None

    q = query.lower()

    # 1️⃣ Filter only contact entries
    contacts = [
        m for m in matches
        if "branch" in (m.get("metadata") or {})
    ]

    if not contacts:
        return None

    chosen = None

    # 2️⃣ Prefer city-specific match
    for city in CITY_HINTS:
        if city in q:
            for m in contacts:
                meta = m.get("metadata", {})
                text = (
                    meta.get("branch", "") +
                    meta.get("address", "") +
                    meta.get("intro", "")
                ).lower()
                if city in text:
                    chosen = m
                    break
        if chosen:
            break

    # 3️⃣ Fallback: highest score
    if not chosen:
        chosen = max(contacts, key=lambda x: x.get("score", 0))

    meta = chosen.get("metadata", {})

    # Normalize fields
    branch = meta.get("branch", "FES Branch")
    address = meta.get("address", "")
    phone = meta.get("phone", "")
    email = meta.get("email", "info@fespak.com")
    link = meta.get("link", "")

    if isinstance(phone, list):
        phone = ", ".join(p for p in phone if p)

    # 4️⃣ FINAL STRUCTURED RESPONSE (Markdown-safe)
    return f"""
We have FES branches in many cities such as Rawalpindi, Peshawar, Karachi, and more.

📍 **{branch}**

**Branch:** {branch}  
**Address:** {address}  
**Phone:** {phone}  
**Email:** {email}  
**Link:** {link}  

For specific branch information, you can ask about a particular branch, for example, **‘FES Lahore contact’**.
""".strip()
