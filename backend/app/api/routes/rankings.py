"""Rankings API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.pcs_scraper import PCSScraperService
from app.dependencies import get_scraper

router = APIRouter()


@router.get("/individual")
async def get_individual_ranking(
    limit: int = Query(50, ge=1, le=500, description="Number of riders"),
    category: str = Query("me", description="Category: me=men elite, we=women elite"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Get individual rider rankings."""
    try:
        data = await scraper.get_ranking("individual", category)
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])

        # Limit results
        if "ranking" in data and isinstance(data["ranking"], list):
            data["ranking"] = data["ranking"][:limit]

        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams")
async def get_team_ranking(
    limit: int = Query(20, ge=1, le=100, description="Number of teams"),
    category: str = Query("me", description="Category: me=men elite, we=women elite"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Get team rankings."""
    try:
        data = await scraper.get_ranking("teams", category)
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])

        # Limit results
        if "ranking" in data and isinstance(data["ranking"], list):
            data["ranking"] = data["ranking"][:limit]

        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nations")
async def get_nation_ranking(
    limit: int = Query(30, ge=1, le=100, description="Number of nations"),
    category: str = Query("me", description="Category: me=men elite, we=women elite"),
    scraper: PCSScraperService = Depends(get_scraper)
):
    """Get nation rankings."""
    try:
        data = await scraper.get_ranking("nations", category)
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])

        # Limit results
        if "ranking" in data and isinstance(data["ranking"], list):
            data["ranking"] = data["ranking"][:limit]

        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
