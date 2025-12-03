"""Statistics and ranking models."""

from typing import Optional, List
from pydantic import BaseModel


class RankingEntry(BaseModel):
    """A single entry in rankings."""
    rank: int
    prev_rank: Optional[int] = None
    rider_name: Optional[str] = None
    rider_url: Optional[str] = None
    team_name: Optional[str] = None
    team_url: Optional[str] = None
    nationality: Optional[str] = None
    points: int
    change: Optional[int] = None


class TeamRankingEntry(BaseModel):
    """A single team ranking entry."""
    rank: int
    prev_rank: Optional[int] = None
    team_name: str
    team_url: Optional[str] = None
    nationality: Optional[str] = None
    points: int


class StatsSummary(BaseModel):
    """Summary statistics."""
    total_races: Optional[int] = None
    total_riders: Optional[int] = None
    total_teams: Optional[int] = None
    worldtour_races: Optional[int] = None
    active_season: Optional[int] = None
