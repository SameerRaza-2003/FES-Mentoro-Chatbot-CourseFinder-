from typing import Optional, List
from pydantic import BaseModel, Field

# --- Metadata & Match Models ---
class Metadata(BaseModel):
    """Metadata attached to each Pinecone match."""
    title: Optional[str] = Field(None, description="Title or slug of the document/blog")
    chunk: Optional[str] = Field(None, description="Text content chunk retrieved from Pinecone")
    content: Optional[str] = Field(None, description="Full content (if available)")
    branch: Optional[str] = Field(None, description="FES branch name for contact entries")
    address: Optional[str] = Field(None, description="Branch address")
    intro: Optional[str] = Field(None, description="Short intro or description")
    phone: Optional[List[str] | str] = Field(None, description="Phone number(s) for contact")
    email: Optional[str] = Field(None, description="Email address for contact")
    link: Optional[str] = Field(None, description="Website or contact link")
    slug: Optional[str] = Field(None, description="Slug for blog/university page")


class Match(BaseModel):
    """Single Pinecone match record."""
    id: str
    score: float
    metadata: Optional[Metadata] = None


# --- Chat Models ---
class ChatRequest(BaseModel):
    """Incoming user query."""
    query: str = Field(..., description="User's message or question for Mentora")


class ChatResponse(BaseModel):
    """Standardized chatbot response."""
    response: str
    matches: Optional[List[Match]] = None
    elapsed_time: Optional[float] = None


class ErrorResponse(BaseModel):
    """Error structure returned by API."""
    error: str


class StreamEvent(BaseModel):
    """Represents a single SSE event."""
    event: str
    data: str
