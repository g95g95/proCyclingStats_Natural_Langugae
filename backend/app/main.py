"""
PCS Assistant API - FastAPI Application

AI-powered cycling statistics assistant using ProCyclingStats data.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import chat, riders, races, teams, rankings, stats
from app.api.websocket import websocket_router
from app.services.cache_service import CacheService
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup: Initialize cache
    app.state.cache = CacheService()
    await app.state.cache.start()
    yield
    # Shutdown: Cleanup
    await app.state.cache.close()


app = FastAPI(
    title="PCS Assistant API",
    description="AI-powered cycling statistics assistant using ProCyclingStats data",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else "/docs",
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS - Critical for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(riders.router, prefix="/api/riders", tags=["Riders"])
app.include_router(races.router, prefix="/api/races", tags=["Races"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(rankings.router, prefix="/api/rankings", tags=["Rankings"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])

# WebSocket for real-time updates
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and Render."""
    return {
        "status": "healthy",
        "service": "pcs-assistant-api",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "PCS Assistant API - Cycling Statistics",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "chat": "/api/chat",
            "riders": "/api/riders/{slug}",
            "races": "/api/races/{slug}?year=2024",
            "teams": "/api/teams/{slug}?year=2024",
            "rankings": "/api/rankings/individual",
            "websocket": "/ws/live"
        }
    }
