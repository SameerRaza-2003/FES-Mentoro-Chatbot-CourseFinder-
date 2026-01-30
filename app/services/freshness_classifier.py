from app.services.openai_service import client


def needs_web_search(query: str) -> bool:
    prompt = f"""
User question:
"{query}"

Question:
To answer this accurately, do you need current or real-time information
that may have changed recently (policies, rules, deadlines, updates)?

Answer ONLY with YES or NO.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=5,
        )

        return response.choices[0].message.content.strip().upper() == "YES"

    except Exception:
        # Safe default: do not use web if classifier fails
        return False
