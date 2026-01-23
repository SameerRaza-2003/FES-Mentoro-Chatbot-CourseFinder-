from collections import defaultdict, deque
from typing import Deque, Dict, Tuple

# session_id -> deque[(role, message)]
CONVERSATION_MEMORY: Dict[str, Deque[Tuple[str, str]]] = defaultdict(
    lambda: deque(maxlen=6)  # last 3 user+assistant turns
)
def add_message(session_id: str, role: str, content: str):
    CONVERSATION_MEMORY[session_id].append((role, content))


def get_history(session_id: str) -> list[dict]:
    return [
        {"role": role, "content": content}
        for role, content in CONVERSATION_MEMORY[session_id]
    ]
