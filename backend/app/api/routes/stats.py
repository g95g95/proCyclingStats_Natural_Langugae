"""Statistics API endpoints."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/summary")
async def get_stats_summary(request: Request):
    """Get general statistics summary."""
    cache = request.app.state.cache

    return {
        "total_races": 892,
        "active_riders": 2847,
        "worldtour_teams": 18,
        "race_days": 342,
        "active_season": 2024,
        "cache_stats": cache.stats()
    }


@router.get("/cache")
async def get_cache_stats(request: Request):
    """Get cache statistics (admin endpoint)."""
    cache = request.app.state.cache
    return cache.stats()


@router.delete("/cache")
async def clear_cache(request: Request):
    """Clear all cached data (admin endpoint)."""
    cache = request.app.state.cache
    await cache.clear()
    return {"message": "Cache cleared", "stats": cache.stats()}
