"""Race API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.pcs_scraper import PCSScraperService
from app.dependencies import get_scraper

router = APIRouter()


@router.get("/{race_slug}")
async def get_race_results(
    race_slug: str,
    year: int = Query(..., description="Race year"),
    stage: Optional[int] = Query(None, description="Stage number"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Get race results.

    Examples:
    - /api/races/tour-de-france?year=2024
    - /api/races/tour-de-france?year=2024&stage=1
    """
    try:
        data = await scraper.get_race_results(race_slug, year, stage)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{race_slug}/startlist")
async def get_race_startlist(
    race_slug: str,
    year: int = Query(..., description="Race year"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Get race startlist."""
    try:
        data = await scraper.get_race_startlist(race_slug, year)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
