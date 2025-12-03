"""Rider API endpoints."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.pcs_scraper import PCSScraperService
from app.dependencies import get_scraper

router = APIRouter()


@router.get("/{slug}")
async def get_rider_profile(
    slug: str,
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Get rider profile by slug or name.

    Examples:
    - /api/riders/tadej-pogacar
    - /api/riders/pogacar
    """
    try:
        data = await scraper.get_rider(slug)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{slug}/victories")
async def get_rider_victories(
    slug: str,
    year: Optional[int] = Query(None, description="Filter by year"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Get rider victories, optionally filtered by year."""
    try:
        data = await scraper.get_rider_victories(slug, year)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{slug}/results")
async def get_rider_results(
    slug: str,
    year: Optional[int] = Query(None, description="Filter by year"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Get rider race results."""
    try:
        data = await scraper.get_rider_results(slug, year)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/")
async def search_riders(
    q: str = Query(..., min_length=2, description="Search query"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Search for riders by name."""
    try:
        results = await scraper.search_riders(q)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
