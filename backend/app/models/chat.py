"""Chat message models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str  # "user" or "assistant"
    content: str


class VisualizationData(BaseModel):
    """Data for visualization rendering."""
    type: str  # "bar_chart", "line_chart", "radar_chart", "pie_chart", "table"
    data: Dict[str, Any]
    title: Optional[str] = None


class ChatRequest(BaseModel):
    """Request to send a chat message."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""
    message: str
    data: Optional[Dict[str, Any]] = None
    visualization: Optional[VisualizationData] = None
