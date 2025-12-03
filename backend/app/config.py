"""
Application configuration - Render compatible.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API - Render provides PORT automatically
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = False

    # CORS - Update with your Render URLs
    ALLOWED_ORIGINS: List[str] = [
        "https://pcs-assistant.onrender.com",
        "http://localhost:5173",
        "http://localhost:3000"
    ]

    # AI Configuration - supports both OpenAI and Anthropic
    AI_MODEL: str = "gpt-4o"  # e.g., "gpt-4o", "gpt-3.5-turbo", "claude-sonnet-4-20250514"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Cache
    CACHE_TTL_DEFAULT: int = 300  # 5 minutes
    CACHE_TTL_RANKINGS: int = 600  # 10 minutes
    CACHE_TTL_RIDER: int = 900  # 15 minutes

    # Redis (optional - for Render Redis)
    REDIS_URL: str | None = None

    # Rate limiting
    RATE_LIMIT_PCS: int = 10  # requests per minute to PCS

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
