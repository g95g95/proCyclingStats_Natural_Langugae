"""
ProCyclingStats Scraper Service

Uses the procyclingstats library to fetch data from procyclingstats.com
Implements caching to avoid rate limiting and improve performance.
"""

from typing import Optional, Dict, Any, List
import asyncio
from concurrent.futures import ThreadPoolExecutor

from procyclingstats import Rider, Race, RaceStartlist, Stage, Team, Ranking

from app.services.cache_service import CacheService
from app.services.entity_resolver import EntityResolver


class PCSScraperService:
    """Service for scraping ProCyclingStats data."""

    def __init__(self, cache: CacheService):
        self.cache = cache
        self.entity_resolver = EntityResolver()
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def get_rider(self, name_or_slug: str) -> Dict[str, Any]:
        """
        Get rider profile data.

        Args:
            name_or_slug: Rider name ("Tadej Pogacar") or slug ("tadej-pogacar")

        Returns:
            Dict with rider data including name, nationality, team, stats, etc.
        """
        slug = await self.entity_resolver.resolve_rider(name_or_slug)
        cache_key = f"rider:{slug}"

        # Check cache first
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Scrape in thread pool (procyclingstats is sync)
        def _scrape():
            try:
                rider = Rider(f"rider/{slug}")
                return rider.parse()
            except Exception as e:
                return {"error": str(e), "slug": slug}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        # Cache for 15 minutes
        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=900)

        return data

    async def get_rider_victories(
        self,
        name_or_slug: str,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get rider victories, optionally filtered by year."""
        slug = await self.entity_resolver.resolve_rider(name_or_slug)
        cache_key = f"rider_victories:{slug}:{year or 'all'}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        def _scrape():
            try:
                # Get rider main page for victories
                rider = Rider(f"rider/{slug}")
                data = rider.parse()
                return data
            except Exception as e:
                return {"error": str(e), "slug": slug}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        # Filter by year if specified and data has victories
        if year and "error" not in data:
            if "victories" in data:
                data["victories"] = [
                    v for v in data.get("victories", [])
                    if v.get("year") == year or str(year) in str(v.get("date", ""))
                ]

        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=900)

        return data

    async def get_rider_results(
        self,
        name_or_slug: str,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get rider race results."""
        slug = await self.entity_resolver.resolve_rider(name_or_slug)
        cache_key = f"rider_results:{slug}:{year or 'all'}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        def _scrape():
            try:
                rider = Rider(f"rider/{slug}")
                return rider.parse()
            except Exception as e:
                return {"error": str(e), "slug": slug}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=900)

        return data

    async def get_race_results(
        self,
        race_slug: str,
        year: int,
        stage: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get race results.

        Args:
            race_slug: Race identifier (e.g., "tour-de-france")
            year: Race year
            stage: Optional stage number (None for GC)

        Returns:
            Dict with race results
        """
        # Resolve race slug if it's a common name
        resolved_slug = await self.entity_resolver.resolve_race(race_slug)

        if stage:
            url = f"race/{resolved_slug}/{year}/stage-{stage}"
            cache_key = f"race:{resolved_slug}:{year}:stage-{stage}"
        else:
            url = f"race/{resolved_slug}/{year}"
            cache_key = f"race:{resolved_slug}:{year}:gc"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        def _scrape():
            try:
                if stage:
                    scraper = Stage(url)
                else:
                    scraper = Race(url)
                return scraper.parse()
            except Exception as e:
                return {"error": str(e), "race": resolved_slug, "year": year}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=900)

        return data

    async def get_race_startlist(
        self,
        race_slug: str,
        year: int
    ) -> Dict[str, Any]:
        """Get race startlist."""
        resolved_slug = await self.entity_resolver.resolve_race(race_slug)
        url = f"race/{resolved_slug}/{year}/startlist"
        cache_key = f"startlist:{resolved_slug}:{year}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        def _scrape():
            try:
                startlist = RaceStartlist(url)
                return {"startlist": startlist.startlist()}
            except Exception as e:
                return {"error": str(e), "race": resolved_slug, "year": year}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=1800)  # 30 min

        return data

    async def get_team(self, team_slug: str, year: int) -> Dict[str, Any]:
        """Get team roster and info."""
        resolved_slug = await self.entity_resolver.resolve_team(team_slug, year)
        url = f"team/{resolved_slug}-{year}"
        cache_key = f"team:{resolved_slug}:{year}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        def _scrape():
            try:
                team = Team(url)
                return team.parse()
            except Exception as e:
                return {"error": str(e), "team": resolved_slug, "year": year}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=3600)  # 1 hour

        return data

    async def get_ranking(
        self,
        ranking_type: str = "individual",
        category: str = "me"  # me = men elite
    ) -> Dict[str, Any]:
        """
        Get UCI/PCS rankings.

        Args:
            ranking_type: "individual", "teams", "nations"
            category: "me" (men elite), "we" (women elite), etc.
        """
        url = f"rankings/{category}/{ranking_type}"
        cache_key = f"ranking:{category}:{ranking_type}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        def _scrape():
            try:
                ranking = Ranking(url)
                if ranking_type == "individual":
                    return {"ranking": ranking.individual_ranking()}
                elif ranking_type == "teams":
                    return {"ranking": ranking.team_ranking()}
                else:
                    return ranking.parse()
            except Exception as e:
                return {"error": str(e), "ranking_type": ranking_type}

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)

        if "error" not in data:
            await self.cache.set(cache_key, data, ttl=600)  # 10 min

        return data

    async def search_riders(self, query: str) -> List[Dict[str, Any]]:
        """Search for riders by name."""
        return await self.entity_resolver.search_riders(query)
