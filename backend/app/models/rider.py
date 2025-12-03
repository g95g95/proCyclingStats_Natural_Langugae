"""Rider data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class RiderSpecialties(BaseModel):
    """Rider specialty scores."""
    gc: Optional[int] = None
    time_trial: Optional[int] = None
    sprint: Optional[int] = None
    climber: Optional[int] = None
    one_day_races: Optional[int] = None


class RiderVictory(BaseModel):
    """A single victory record."""
    date: Optional[str] = None
    race: str
    race_url: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None


class RiderProfile(BaseModel):
    """Rider profile information."""
    name: str
    slug: Optional[str] = None
    nationality: Optional[str] = None
    nationality_code: Optional[str] = None
    birthdate: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    team: Optional[str] = None
    team_url: Optional[str] = None
    pcs_points: Optional[int] = None
    uci_points: Optional[int] = None
    rank: Optional[int] = None
    specialties: Optional[RiderSpecialties] = None
    victories_count: Optional[int] = None
    victories: Optional[List[RiderVictory]] = None
    photo_url: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


class RiderSearchResult(BaseModel):
    """Search result for rider lookup."""
    name: str
    slug: str
    team: Optional[str] = None
    nationality: Optional[str] = None
    match_type: str = "exact"
