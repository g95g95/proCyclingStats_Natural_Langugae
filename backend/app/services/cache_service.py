"""
Cache Service

In-memory caching with TTL support.
Can be replaced with Redis for production.
"""

from typing import Any, Optional, Dict
import asyncio
from datetime import datetime, timedelta


class CacheService:
    """Simple in-memory cache with TTL."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cleanup_task: Optional[asyncio.Task] = None

    async def start(self):
        """Start background cleanup task."""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def close(self):
        """Stop cleanup task."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if datetime.now() > entry["expires_at"]:
            del self._cache[key]
            return None

        return entry["value"]

    async def set(self, key: str, value: Any, ttl: int = 300):
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (default 5 minutes)
        """
        self._cache[key] = {
            "value": value,
            "expires_at": datetime.now() + timedelta(seconds=ttl),
            "created_at": datetime.now()
        }

    async def delete(self, key: str):
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]

    async def clear(self):
        """Clear all cache entries."""
        self._cache.clear()

    async def _cleanup_loop(self):
        """Background task to clean expired entries."""
        while True:
            await asyncio.sleep(60)  # Run every minute
            await self._cleanup_expired()

    async def _cleanup_expired(self):
        """Remove expired entries."""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self._cache.items()
            if now > entry["expires_at"]
        ]
        for key in expired_keys:
            del self._cache[key]

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "entries": len(self._cache),
            "keys": list(self._cache.keys())
        }
