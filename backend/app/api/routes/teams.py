"""Team API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.pcs_scraper import PCSScraperService
from app.dependencies import get_scraper

router = APIRouter()


@router.get("/{team_slug}")
async def get_team_info(
    team_slug: str,
    year: int = Query(2024, description="Team year"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Get team information and roster.

    Examples:
    - /api/teams/uae-team-emirates?year=2024
    - /api/teams/visma?year=2024
    """
    try:
        data = await scraper.get_team(team_slug, year)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
