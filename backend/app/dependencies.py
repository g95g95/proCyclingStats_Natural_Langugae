"""Dependency injection for FastAPI."""

from fastapi import Request

from app.services.pcs_scraper import PCSScraperService
from app.services.cache_service import CacheService


def get_cache(request: Request) -> CacheService:
    """Get cache service from app state."""
    return request.app.state.cache


def get_scraper(request: Request) -> PCSScraperService:
    """Get PCS scraper service with cache."""
    cache = get_cache(request)
    return PCSScraperService(cache)
