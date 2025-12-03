"""Team data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class TeamRider(BaseModel):
    """Rider in a team roster."""
    name: str
    rider_url: Optional[str] = None
    nationality: Optional[str] = None
    birthdate: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None


class TeamInfo(BaseModel):
    """Team information."""
    name: str
    slug: Optional[str] = None
    year: int
    category: Optional[str] = None
    nationality: Optional[str] = None
    bike: Optional[str] = None
    jersey: Optional[str] = None
    manager: Optional[str] = None
    roster: Optional[List[TeamRider]] = None
    wins_count: Optional[int] = None
    ranking: Optional[int] = None
    points: Optional[int] = None
    raw_data: Optional[Dict[str, Any]] = None
