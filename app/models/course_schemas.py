from pydantic import BaseModel
from typing import Dict, Any


class CourseSearchRequest(BaseModel):
    query: str
    answers: Dict[str, Any]
    top_k: int = 40
