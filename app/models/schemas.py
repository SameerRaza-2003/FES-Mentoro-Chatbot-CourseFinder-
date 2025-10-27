from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


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


class ChatRequest(BaseModel):
    """Schema for chatbot input query."""
    query: str = Field(..., description="User's question or message for Mentora")


class ChatResponse(BaseModel):
    """Standardized non-streaming chatbot response."""
    response: str = Field(..., description="Final chatbot message")
    matches: Optional[List[Match]] = Field(
        None, description="Retrieved Pinecone matches that informed the answer"
    )
    elapsed_time: Optional[float] = Field(
        None, description="Processing time (seconds)"
    )


class ErrorResponse(BaseModel):
    """Schema for API error messages."""
    error: str = Field(..., description="Description of what went wrong")


class StreamEvent(BaseModel):
    """Represents a single SSE event in the /stream endpoint."""
    event: str = Field(..., description="Event type (usually 'message' or '[DONE]')")
    data: str = Field(..., description="Chunk of generated content or system info")
