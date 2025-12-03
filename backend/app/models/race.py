"""Race data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class RaceResultEntry(BaseModel):
    """A single result entry in a race."""
    rank: int
    rider_name: str
    rider_url: Optional[str] = None
    team: Optional[str] = None
    team_url: Optional[str] = None
    time: Optional[str] = None
    gap: Optional[str] = None
    points: Optional[int] = None


class RaceStageResult(BaseModel):
    """Stage race result."""
    stage_number: int
    stage_name: Optional[str] = None
    date: Optional[str] = None
    distance: Optional[float] = None
    stage_type: Optional[str] = None
    winner: Optional[str] = None
    results: Optional[List[RaceResultEntry]] = None


class RaceResult(BaseModel):
    """Full race result information."""
    name: str
    slug: Optional[str] = None
    year: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category: Optional[str] = None
    distance: Optional[float] = None
    stages: Optional[int] = None
    winner: Optional[str] = None
    gc_results: Optional[List[RaceResultEntry]] = None
    stage_results: Optional[List[RaceStageResult]] = None
    raw_data: Optional[Dict[str, Any]] = None


class RaceStartlistEntry(BaseModel):
    """Entry in a race startlist."""
    bib_number: Optional[int] = None
    rider_name: str
    rider_url: Optional[str] = None
    team: str
    team_url: Optional[str] = None
    nationality: Optional[str] = None
