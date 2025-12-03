# CLAUDE.md - PCS Assistant Project Blueprint


# Best Practice
1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them.
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made.
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the todo.md file with a summary of the changes you made and any other relevant information.
8. DO NOT BE LAZY. NEVER BE LAZY. IF THERE IS A BUG FIND THE ROOT CAUSE AND FIX IT. NO TEMPORARY FIXES. YOU ARE A SENIOR DEVELOPER. NEVER BE LAZY.
9. MAKE ALL FIXES AND CODE CHANGES AS SIMPLE AS HUMANLY POSSIBLE. THEY SHOULD ONLY IMPACT NECESSARY CODE RELEVANT TO THE TASK AND NOTHING ELSE. IT SHOULD IMPACT AS LITTLE CODE AS POSSIBLE. YOUR GOAL IS TO NOT INTRODUCE ANY BUGS. IT'S ALL ABOUT SIMPLICITY.
## 🎯 Project Overview

**PCS Assistant** is a real-time cycling statistics application that:
1. Scrapes data from ProCyclingStats.com on-demand
2. Provides an AI-powered natural language interface for querying cycling data
3. Displays interactive dashboards and charts
4. Updates in real-time via WebSockets

### Tech Stack
- **Frontend**: React 18+ with TypeScript, Tailwind CSS, Recharts/Plotly
- **Backend**: FastAPI (Python 3.11+)
- **Scraping**: `procyclingstats` library (pip install procyclingstats)
- **AI**: Claude API (Anthropic)
- **Real-time**: WebSockets (FastAPI + React)
- **Caching**: Redis or in-memory (Python dict with TTL)

---

## 📁 Project Structure

```
pcs-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Settings and env vars
│   │   ├── dependencies.py         # Dependency injection
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat.py         # AI chat endpoints
│   │   │   │   ├── riders.py       # Rider data endpoints
│   │   │   │   ├── races.py        # Race data endpoints
│   │   │   │   ├── teams.py        # Team data endpoints
│   │   │   │   ├── rankings.py     # Rankings endpoints
│   │   │   │   └── stats.py        # Statistics endpoints
│   │   │   └── websocket.py        # WebSocket handlers
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── pcs_scraper.py      # ProCyclingStats scraping service
│   │   │   ├── ai_service.py       # Claude AI integration
│   │   │   ├── cache_service.py    # Caching layer
│   │   │   ├── entity_resolver.py  # Name → slug resolution
│   │   │   └── query_planner.py    # Intent classification & query planning
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── rider.py            # Rider data models
│   │   │   ├── race.py             # Race data models
│   │   │   ├── team.py             # Team data models
│   │   │   ├── chat.py             # Chat message models
│   │   │   └── stats.py            # Statistics models
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── slug_utils.py       # URL slug utilities
│   │       └── date_utils.py       # Date parsing utilities
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_scraper.py
│   │   ├── test_ai_service.py
│   │   └── test_api.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatBox.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   ├── ChatInput.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── DashboardLayout.tsx
│   │   │   │   ├── WidgetContainer.tsx
│   │   │   │   ├── widgets/
│   │   │   │   │   ├── RankingWidget.tsx
│   │   │   │   │   ├── VictoriesWidget.tsx
│   │   │   │   │   ├── UpcomingRacesWidget.tsx
│   │   │   │   │   ├── RiderComparisonWidget.tsx
│   │   │   │   │   └── TrendChartWidget.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── charts/
│   │   │   │   ├── BarChart.tsx
│   │   │   │   ├── LineChart.tsx
│   │   │   │   ├── RadarChart.tsx
│   │   │   │   ├── PieChart.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── LoadingSpinner.tsx
│   │   │   │   ├── ErrorBoundary.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   └── rider/
│   │   │       ├── RiderCard.tsx
│   │   │       ├── RiderProfile.tsx
│   │   │       ├── RiderStats.tsx
│   │   │       └── index.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useChat.ts
│   │   │   ├── useRiderData.ts
│   │   │   ├── useRankings.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts              # Axios/fetch wrapper
│   │   │   ├── websocket.ts        # WebSocket client
│   │   │   └── index.ts
│   │   │
│   │   ├── store/
│   │   │   ├── index.ts            # Zustand or Context store
│   │   │   ├── chatStore.ts
│   │   │   ├── dashboardStore.ts
│   │   │   └── settingsStore.ts
│   │   │
│   │   ├── types/
│   │   │   ├── rider.ts
│   │   │   ├── race.ts
│   │   │   ├── team.ts
│   │   │   ├── chat.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── formatters.ts
│   │   │   ├── constants.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── RiderPage.tsx
│   │   │   ├── RacePage.tsx
│   │   │   ├── RankingsPage.tsx
│   │   │   └── ComparePage.tsx
│   │   │
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── _redirects              # SPA routing for Render Static Site
│
├── render.yaml                 # Render Blueprint (Infrastructure as Code)
├── README.md
└── CLAUDE.md (this file)
```

---

## 🔧 Backend Implementation Details

### 1. Main FastAPI Application (`backend/app/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import chat, riders, races, teams, rankings, stats
from app.api.websocket import websocket_router
from app.services.cache_service import CacheService
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize cache
    app.state.cache = CacheService()
    yield
    # Shutdown: Cleanup
    await app.state.cache.close()

app = FastAPI(
    title="PCS Assistant API",
    description="AI-powered cycling statistics assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(riders.router, prefix="/api/riders", tags=["Riders"])
app.include_router(races.router, prefix="/api/races", tags=["Races"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(rankings.router, prefix="/api/rankings", tags=["Rankings"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 2. PCS Scraper Service (`backend/app/services/pcs_scraper.py`)

```python
"""
ProCyclingStats Scraper Service

Uses the procyclingstats library to fetch data from procyclingstats.com
Implements caching to avoid rate limiting and improve performance.
"""

from typing import Optional, Dict, Any, List
from procyclingstats import Rider, Race, RaceStartlist, Stage, Team, Ranking
import asyncio
from concurrent.futures import ThreadPoolExecutor

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
            rider = Rider(f"rider/{slug}")
            return rider.parse()
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)
        
        # Cache for 15 minutes
        await self.cache.set(cache_key, data, ttl=900)
        return data
    
    async def get_rider_victories(
        self, 
        name_or_slug: str, 
        year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get rider victories, optionally filtered by year."""
        slug = await self.entity_resolver.resolve_rider(name_or_slug)
        cache_key = f"rider_victories:{slug}:{year or 'all'}"
        
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        def _scrape():
            url = f"rider/{slug}/statistics/wins"
            rider = Rider(url)
            # Parse victories - implementation depends on procyclingstats version
            return rider.parse()
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)
        
        # Filter by year if specified
        if year and 'victories' in data:
            data['victories'] = [
                v for v in data['victories'] 
                if v.get('year') == year or str(year) in v.get('date', '')
            ]
        
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
        if stage:
            url = f"race/{race_slug}/{year}/stage-{stage}"
            cache_key = f"race:{race_slug}:{year}:stage-{stage}"
        else:
            url = f"race/{race_slug}/{year}"
            cache_key = f"race:{race_slug}:{year}:gc"
        
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        def _scrape():
            if stage:
                scraper = Stage(url)
            else:
                scraper = Race(url)
            return scraper.parse()
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)
        
        await self.cache.set(cache_key, data, ttl=900)
        return data
    
    async def get_race_startlist(
        self, 
        race_slug: str, 
        year: int
    ) -> List[Dict[str, Any]]:
        """Get race startlist."""
        url = f"race/{race_slug}/{year}/startlist"
        cache_key = f"startlist:{race_slug}:{year}"
        
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        def _scrape():
            startlist = RaceStartlist(url)
            return startlist.startlist()
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)
        
        await self.cache.set(cache_key, data, ttl=1800)  # 30 min
        return data
    
    async def get_team(self, team_slug: str, year: int) -> Dict[str, Any]:
        """Get team roster and info."""
        url = f"team/{team_slug}-{year}"
        cache_key = f"team:{team_slug}:{year}"
        
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        def _scrape():
            team = Team(url)
            return team.parse()
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)
        
        await self.cache.set(cache_key, data, ttl=3600)  # 1 hour
        return data
    
    async def get_ranking(
        self, 
        ranking_type: str = "individual",
        category: str = "me"  # me = men elite
    ) -> List[Dict[str, Any]]:
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
            ranking = Ranking(url)
            if ranking_type == "individual":
                return ranking.individual_ranking()
            elif ranking_type == "teams":
                return ranking.team_ranking()
            else:
                return ranking.parse()
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(self.executor, _scrape)
        
        await self.cache.set(cache_key, data, ttl=600)  # 10 min
        return data
    
    async def search_riders(self, query: str) -> List[Dict[str, Any]]:
        """Search for riders by name."""
        return await self.entity_resolver.search_riders(query)
```

### 3. AI Service (`backend/app/services/ai_service.py`)

```python
"""
AI Service for natural language processing using Claude API.

Handles:
- Intent classification
- Query planning
- Natural language response generation
"""

from typing import Dict, Any, List, Optional
from anthropic import Anthropic
import json

from app.config import settings
from app.services.pcs_scraper import PCSScraperService

class AIService:
    """Claude AI integration for natural language cycling queries."""
    
    SYSTEM_PROMPT = """You are PCS Assistant, an expert AI assistant for professional cycling statistics.
You have access to real-time data from ProCyclingStats.com.

Your capabilities:
1. Answer questions about riders (stats, victories, career, team)
2. Provide race results and classifications
3. Compare riders head-to-head
4. Show rankings (UCI, PCS)
5. Generate data for charts and visualizations

When the user asks a question:
1. First, analyze what data is needed
2. Use the available functions to fetch data
3. Provide a clear, informative response
4. When appropriate, suggest visualizations

Always be precise with statistics and cite the data source (ProCyclingStats).
Use cycling terminology appropriately.
Format numbers nicely (e.g., "25 victories" not "25 wins").

For Italian users, respond in Italian. Match the user's language.
"""

    QUERY_PLANNING_PROMPT = """Analyze this cycling question and determine what data to fetch.

Question: {question}

Return a JSON object with:
{{
    "intent": "rider_info|rider_victories|rider_results|race_results|race_startlist|team_info|ranking|comparison|statistics",
    "entities": {{
        "riders": ["slug1", "slug2"],  // if applicable
        "races": ["race-slug"],         // if applicable
        "teams": ["team-slug"],         // if applicable
        "year": 2024,                   // if applicable
        "stage": null                   // if applicable
    }},
    "filters": {{
        "year": 2024,
        "race_type": null,
        "limit": 10
    }},
    "visualization": "bar_chart|line_chart|radar_chart|table|none",
    "comparison_mode": false
}}

Only return valid JSON, no explanation."""

    def __init__(self, scraper: PCSScraperService):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.scraper = scraper
        self.model = "claude-sonnet-4-20250514"
    
    async def plan_query(self, question: str) -> Dict[str, Any]:
        """
        Analyze user question and create a query plan.
        
        Returns structured plan for data fetching.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": self.QUERY_PLANNING_PROMPT.format(question=question)
                }
            ]
        )
        
        try:
            plan = json.loads(response.content[0].text)
            return plan
        except json.JSONDecodeError:
            # Fallback to basic intent
            return {
                "intent": "general",
                "entities": {},
                "filters": {},
                "visualization": "none",
                "comparison_mode": False
            }
    
    async def execute_query(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the query plan and fetch required data.
        """
        intent = plan.get("intent", "general")
        entities = plan.get("entities", {})
        filters = plan.get("filters", {})
        
        data = {}
        
        if intent == "rider_info" and entities.get("riders"):
            for rider_slug in entities["riders"]:
                data[rider_slug] = await self.scraper.get_rider(rider_slug)
        
        elif intent == "rider_victories" and entities.get("riders"):
            year = filters.get("year")
            for rider_slug in entities["riders"]:
                data[rider_slug] = await self.scraper.get_rider_victories(
                    rider_slug, year
                )
        
        elif intent == "race_results" and entities.get("races"):
            year = filters.get("year", 2024)
            stage = entities.get("stage")
            for race_slug in entities["races"]:
                data[race_slug] = await self.scraper.get_race_results(
                    race_slug, year, stage
                )
        
        elif intent == "ranking":
            ranking_type = filters.get("ranking_type", "individual")
            data["ranking"] = await self.scraper.get_ranking(ranking_type)
        
        elif intent == "comparison" and len(entities.get("riders", [])) >= 2:
            for rider_slug in entities["riders"]:
                data[rider_slug] = await self.scraper.get_rider(rider_slug)
        
        elif intent == "team_info" and entities.get("teams"):
            year = filters.get("year", 2024)
            for team_slug in entities["teams"]:
                data[team_slug] = await self.scraper.get_team(team_slug, year)
        
        return data
    
    async def generate_response(
        self, 
        question: str, 
        data: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate natural language response with optional visualization data.
        """
        # Build context from fetched data
        data_context = json.dumps(data, indent=2, default=str)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"""Question: {question}

Data fetched from ProCyclingStats:
```json
{data_context}
```

Query plan: {json.dumps(plan)}

Provide a helpful response. If visualization was requested, also provide the data in a format suitable for charting."""
                }
            ]
        )
        
        response_text = response.content[0].text
        
        # Build response object
        result = {
            "message": response_text,
            "data": data,
            "visualization": None
        }
        
        # Add visualization data if appropriate
        if plan.get("visualization") != "none":
            result["visualization"] = {
                "type": plan.get("visualization"),
                "data": self._prepare_chart_data(data, plan)
            }
        
        return result
    
    def _prepare_chart_data(
        self, 
        data: Dict[str, Any], 
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Transform raw data into chart-ready format."""
        viz_type = plan.get("visualization")
        intent = plan.get("intent")
        
        if viz_type == "bar_chart" and intent == "rider_victories":
            # Format for victories bar chart
            chart_data = []
            for rider, rider_data in data.items():
                victories = rider_data.get("victories", [])
                chart_data.append({
                    "name": rider_data.get("name", rider),
                    "victories": len(victories)
                })
            return {"series": chart_data, "xKey": "name", "yKey": "victories"}
        
        elif viz_type == "line_chart":
            # Format for trend line chart
            return {"series": [], "xKey": "year", "yKey": "value"}
        
        elif viz_type == "radar_chart" and intent == "comparison":
            # Format for rider comparison radar
            chart_data = []
            for rider, rider_data in data.items():
                specialties = rider_data.get("specialties", {})
                chart_data.append({
                    "name": rider_data.get("name", rider),
                    "gc": specialties.get("gc", 0),
                    "tt": specialties.get("time_trial", 0),
                    "sprint": specialties.get("sprint", 0),
                    "climber": specialties.get("climber", 0),
                    "one_day": specialties.get("one_day_races", 0)
                })
            return {"series": chart_data}
        
        return {}
    
    async def chat(self, question: str) -> Dict[str, Any]:
        """
        Main entry point for chat interactions.
        
        Orchestrates: plan → fetch → respond
        """
        # 1. Plan the query
        plan = await self.plan_query(question)
        
        # 2. Execute and fetch data
        data = await self.execute_query(plan)
        
        # 3. Generate response
        response = await self.generate_response(question, data, plan)
        
        return response
```

### 4. Entity Resolver (`backend/app/services/entity_resolver.py`)

```python
"""
Entity Resolver Service

Resolves natural language names to PCS URL slugs.
Examples:
- "Pogacar" → "tadej-pogacar"
- "Tour de France" → "tour-de-france"
- "UAE Team Emirates" → "uae-team-emirates"
"""

from typing import Optional, List, Dict, Any
import re
from unidecode import unidecode

class EntityResolver:
    """Resolves entity names to ProCyclingStats slugs."""
    
    # Common rider aliases
    RIDER_ALIASES = {
        "pogacar": "tadej-pogacar",
        "pogi": "tadej-pogacar",
        "vingegaard": "jonas-vingegaard",
        "jonas": "jonas-vingegaard",
        "evenepoel": "remco-evenepoel",
        "remco": "remco-evenepoel",
        "wva": "wout-van-aert",
        "van aert": "wout-van-aert",
        "mvdp": "mathieu-van-der-poel",
        "van der poel": "mathieu-van-der-poel",
        "roglic": "primoz-roglic",
        "ganna": "filippo-ganna",
        "cavendish": "mark-cavendish",
        "cav": "mark-cavendish",
        "alaphilippe": "julian-alaphilippe",
        "ala": "julian-alaphilippe",
    }
    
    # Common race aliases
    RACE_ALIASES = {
        "tour": "tour-de-france",
        "tdf": "tour-de-france",
        "tour de france": "tour-de-france",
        "giro": "giro-d-italia",
        "giro d'italia": "giro-d-italia",
        "vuelta": "vuelta-a-espana",
        "vuelta a espana": "vuelta-a-espana",
        "roubaix": "paris-roubaix",
        "paris-roubaix": "paris-roubaix",
        "fiandre": "tour-of-flanders",
        "ronde": "tour-of-flanders",
        "tour of flanders": "tour-of-flanders",
        "sanremo": "milano-sanremo",
        "milan-sanremo": "milano-sanremo",
        "lombardia": "giro-di-lombardia",
        "il lombardia": "giro-di-lombardia",
        "liegi": "liege-bastogne-liege",
        "liege": "liege-bastogne-liege",
        "freccia vallone": "la-fleche-wallonne",
        "fleche wallonne": "la-fleche-wallonne",
        "strade bianche": "strade-bianche",
        "tirreno": "tirreno-adriatico",
        "uae tour": "uae-tour",
    }
    
    # Team aliases
    TEAM_ALIASES = {
        "uae": "uae-team-emirates",
        "visma": "team-visma-lease-a-bike",
        "jumbo": "team-visma-lease-a-bike",
        "ineos": "ineos-grenadiers",
        "quick step": "soudal-quick-step",
        "quickstep": "soudal-quick-step",
        "soudal": "soudal-quick-step",
        "bora": "red-bull-bora-hansgrohe",
        "red bull": "red-bull-bora-hansgrohe",
        "lidl trek": "lidl-trek",
        "trek": "lidl-trek",
        "alpecin": "alpecin-deceuninck",
        "ef": "ef-education-easypost",
        "bahrain": "bahrain-victorious",
        "movistar": "movistar-team",
        "jayco": "team-jayco-alula",
    }
    
    async def resolve_rider(self, name: str) -> str:
        """
        Resolve rider name to PCS slug.
        
        Args:
            name: Rider name in any format
            
        Returns:
            PCS-compatible slug
        """
        # Normalize input
        normalized = self._normalize(name)
        
        # Check aliases first
        if normalized in self.RIDER_ALIASES:
            return self.RIDER_ALIASES[normalized]
        
        # Try to create slug from name
        return self._name_to_slug(name)
    
    async def resolve_race(self, name: str) -> str:
        """Resolve race name to PCS slug."""
        normalized = self._normalize(name)
        
        if normalized in self.RACE_ALIASES:
            return self.RACE_ALIASES[normalized]
        
        return self._name_to_slug(name)
    
    async def resolve_team(self, name: str, year: int = 2024) -> str:
        """Resolve team name to PCS slug."""
        normalized = self._normalize(name)
        
        if normalized in self.TEAM_ALIASES:
            return f"{self.TEAM_ALIASES[normalized]}-{year}"
        
        return f"{self._name_to_slug(name)}-{year}"
    
    async def search_riders(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for riders matching query.
        
        In a full implementation, this would search the PCS database.
        For now, returns matches from aliases.
        """
        normalized = self._normalize(query)
        results = []
        
        for alias, slug in self.RIDER_ALIASES.items():
            if normalized in alias or alias in normalized:
                results.append({
                    "name": self._slug_to_name(slug),
                    "slug": slug,
                    "match_type": "alias"
                })
        
        return results
    
    def _normalize(self, text: str) -> str:
        """Normalize text for matching."""
        # Remove accents, lowercase, strip
        text = unidecode(text).lower().strip()
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _name_to_slug(self, name: str) -> str:
        """Convert name to URL slug."""
        # Handle "Firstname Lastname" format
        slug = unidecode(name).lower().strip()
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        # Remove non-alphanumeric except hyphens
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        return slug
    
    def _slug_to_name(self, slug: str) -> str:
        """Convert slug back to readable name."""
        parts = slug.split('-')
        return ' '.join(part.capitalize() for part in parts)
```

### 5. Cache Service (`backend/app/services/cache_service.py`)

```python
"""
Cache Service

In-memory caching with TTL support.
Can be replaced with Redis for production.
"""

from typing import Any, Optional, Dict
import asyncio
from datetime import datetime, timedelta
import json

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
```

### 6. Chat API Route (`backend/app/api/routes/chat.py`)

```python
"""
Chat API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.services.ai_service import AIService
from app.services.pcs_scraper import PCSScraperService
from app.dependencies import get_scraper, get_cache

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
    visualization: Optional[Dict[str, Any]] = None

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Process a chat message and return AI response with optional data.
    """
    try:
        ai_service = AIService(scraper)
        response = await ai_service.chat(request.message)
        
        return ChatResponse(
            message=response["message"],
            data=response.get("data"),
            visualization=response.get("visualization")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick")
async def quick_query(
    query: str,
    scraper: PCSScraperService = Depends(get_scraper)
):
    """
    Quick query endpoint for simple questions.
    Returns structured data without full AI processing.
    """
    ai_service = AIService(scraper)
    plan = await ai_service.plan_query(query)
    data = await ai_service.execute_query(plan)
    
    return {
        "plan": plan,
        "data": data
    }
```

### 7. WebSocket Handler (`backend/app/api/websocket.py`)

```python
"""
WebSocket handlers for real-time updates.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import json

router = APIRouter()

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        # Remove from all subscriptions
        for topic in self.subscriptions:
            self.subscriptions[topic].discard(websocket)
    
    async def subscribe(self, websocket: WebSocket, topic: str):
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        self.subscriptions[topic].add(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass
    
    async def broadcast_to_topic(self, topic: str, message: dict):
        """Broadcast to clients subscribed to a topic."""
        if topic in self.subscriptions:
            for connection in self.subscriptions[topic]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle subscription requests
            if data.get("type") == "subscribe":
                topic = data.get("topic")
                if topic:
                    await manager.subscribe(websocket, topic)
                    await websocket.send_json({
                        "type": "subscribed",
                        "topic": topic
                    })
            
            # Handle ping
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to broadcast ranking updates
async def broadcast_ranking_updates():
    """Periodically fetch and broadcast ranking updates."""
    while True:
        await asyncio.sleep(300)  # Every 5 minutes
        
        # Fetch latest ranking
        # ranking = await scraper.get_ranking()
        
        await manager.broadcast_to_topic("rankings", {
            "type": "ranking_update",
            "data": {}  # ranking data
        })
```

### 8. Configuration (`backend/app/config.py`)

```python
"""
Application configuration.
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Claude API
    ANTHROPIC_API_KEY: str
    
    # Cache
    CACHE_TTL_DEFAULT: int = 300  # 5 minutes
    CACHE_TTL_RANKINGS: int = 600  # 10 minutes
    CACHE_TTL_RIDER: int = 900  # 15 minutes
    
    # Rate limiting
    RATE_LIMIT_PCS: int = 10  # requests per minute to PCS
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 9. Requirements (`backend/requirements.txt`)

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
anthropic>=0.18.0
procyclingstats>=0.2.3
httpx>=0.26.0
python-multipart>=0.0.6
websockets>=12.0
unidecode>=1.3.8
pytest>=7.4.0
pytest-asyncio>=0.23.0
```

---

## 🎨 Frontend Implementation Details

### 1. API Service (`frontend/src/services/api.ts`)

```typescript
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  message: string;
  data?: Record<string, unknown>;
  visualization?: {
    type: 'bar_chart' | 'line_chart' | 'radar_chart' | 'pie_chart' | 'table';
    data: Record<string, unknown>;
  };
}

export interface RiderData {
  name: string;
  nationality: string;
  birthdate: string;
  height?: number;
  weight?: number;
  team?: string;
  specialties?: Record<string, number>;
}

export interface RankingEntry {
  rank: number;
  prev_rank: number;
  rider_name: string;
  rider_url: string;
  team_name: string;
  nationality: string;
  points: number;
}

// API Functions
export const chatApi = {
  sendMessage: async (message: string, history: ChatMessage[] = []): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat/', {
      message,
      conversation_history: history,
    });
    return response.data;
  },

  quickQuery: async (query: string) => {
    const response = await api.post('/chat/quick', null, { params: { query } });
    return response.data;
  },
};

export const ridersApi = {
  getProfile: async (slug: string): Promise<RiderData> => {
    const response = await api.get<RiderData>(`/riders/${slug}`);
    return response.data;
  },

  getVictories: async (slug: string, year?: number) => {
    const response = await api.get(`/riders/${slug}/victories`, {
      params: year ? { year } : {},
    });
    return response.data;
  },

  search: async (query: string) => {
    const response = await api.get('/riders/search', { params: { q: query } });
    return response.data;
  },
};

export const rankingsApi = {
  getIndividual: async (limit = 50): Promise<RankingEntry[]> => {
    const response = await api.get<RankingEntry[]>('/rankings/individual', {
      params: { limit },
    });
    return response.data;
  },

  getTeams: async (limit = 20) => {
    const response = await api.get('/rankings/teams', { params: { limit } });
    return response.data;
  },
};

export const racesApi = {
  getResults: async (raceSlug: string, year: number, stage?: number) => {
    const params: Record<string, unknown> = { year };
    if (stage) params.stage = stage;
    
    const response = await api.get(`/races/${raceSlug}`, { params });
    return response.data;
  },

  getStartlist: async (raceSlug: string, year: number) => {
    const response = await api.get(`/races/${raceSlug}/startlist`, {
      params: { year },
    });
    return response.data;
  },
};

export default api;
```

### 2. WebSocket Hook (`frontend/src/hooks/useWebSocket.ts`)

```typescript
import { useEffect, useRef, useCallback, useState } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live';

interface WebSocketMessage {
  type: string;
  topic?: string;
  data?: unknown;
}

interface UseWebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  autoReconnect?: boolean;
  reconnectInterval?: number;
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const {
    onMessage,
    onConnect,
    onDisconnect,
    autoReconnect = true,
    reconnectInterval = 5000,
  } = options;

  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      setIsConnected(true);
      onConnect?.();
      
      // Start ping interval
      const pingInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'ping' }));
        }
      }, 30000);

      ws.onclose = () => {
        clearInterval(pingInterval);
      };
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data) as WebSocketMessage;
        setLastMessage(message);
        onMessage?.(message);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      onDisconnect?.();
      
      if (autoReconnect) {
        reconnectTimeoutRef.current = setTimeout(connect, reconnectInterval);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    wsRef.current = ws;
  }, [onMessage, onConnect, onDisconnect, autoReconnect, reconnectInterval]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    wsRef.current?.close();
  }, []);

  const subscribe = useCallback((topic: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'subscribe', topic }));
    }
  }, []);

  const send = useCallback((message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    subscribe,
    send,
    connect,
    disconnect,
  };
}
```

### 3. Chat Hook (`frontend/src/hooks/useChat.ts`)

```typescript
import { useState, useCallback } from 'react';
import { chatApi, ChatMessage, ChatResponse } from '../services/api';

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  lastVisualization: ChatResponse['visualization'] | null;
  lastData: Record<string, unknown> | null;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastVisualization, setLastVisualization] = useState<ChatResponse['visualization'] | null>(null);
  const [lastData, setLastData] = useState<Record<string, unknown> | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const userMessage: ChatMessage = { role: 'user', content };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage(content, messages);
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
      if (response.visualization) {
        setLastVisualization(response.visualization);
      }
      
      if (response.data) {
        setLastData(response.data);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      
      // Add error message to chat
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `Sorry, there was an error: ${errorMessage}. Please try again.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setLastVisualization(null);
    setLastData(null);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    lastVisualization,
    lastData,
    sendMessage,
    clearMessages,
  };
}
```

### 4. ChatBox Component (`frontend/src/components/chat/ChatBox.tsx`)

```tsx
import React, { useState, useRef, useEffect } from 'react';
import { useChat } from '../../hooks/useChat';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { DynamicChart } from '../charts/DynamicChart';

export const ChatBox: React.FC = () => {
  const {
    messages,
    isLoading,
    lastVisualization,
    sendMessage,
    clearMessages,
  } = useChat();
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-white rounded-xl shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🚴</span>
          <h2 className="text-lg font-semibold text-gray-800">PCS Assistant</h2>
        </div>
        <button
          onClick={clearMessages}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          Clear chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">👋 Ciao! Sono il tuo assistente ciclismo.</p>
            <p className="text-sm">Chiedimi qualsiasi cosa su ciclisti, corse, classifiche...</p>
            <div className="mt-4 space-y-2">
              <p className="text-xs text-gray-400">Esempi:</p>
              <button
                onClick={() => sendMessage("Quante vittorie ha Pogačar nel 2024?")}
                className="block mx-auto text-sm text-blue-500 hover:underline"
              >
                "Quante vittorie ha Pogačar nel 2024?"
              </button>
              <button
                onClick={() => sendMessage("Chi ha vinto il Tour de France 2024?")}
                className="block mx-auto text-sm text-blue-500 hover:underline"
              >
                "Chi ha vinto il Tour de France 2024?"
              </button>
              <button
                onClick={() => sendMessage("Confronta Pogačar e Vingegaard")}
                className="block mx-auto text-sm text-blue-500 hover:underline"
              >
                "Confronta Pogačar e Vingegaard"
              </button>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}

        {/* Show visualization after last assistant message */}
        {lastVisualization && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <DynamicChart
              type={lastVisualization.type}
              data={lastVisualization.data}
            />
          </div>
        )}

        {isLoading && (
          <div className="flex items-center gap-2 text-gray-500">
            <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full" />
            <span>Sto cercando...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
};
```

### 5. ChatMessage Component (`frontend/src/components/chat/ChatMessage.tsx`)

```tsx
import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ChatMessage as ChatMessageType } from '../../services/api';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2 ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-md'
            : 'bg-gray-100 text-gray-800 rounded-bl-md'
        }`}
      >
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown
            className="prose prose-sm max-w-none"
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({ children }) => <ul className="list-disc ml-4 mb-2">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal ml-4 mb-2">{children}</ol>,
              li: ({ children }) => <li className="mb-1">{children}</li>,
              strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
};
```

### 6. ChatInput Component (`frontend/src/components/chat/ChatInput.tsx`)

```tsx
import React, { useState, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, disabled }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4 border-t">
      <div className="flex items-end gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Chiedi qualcosa sul ciclismo..."
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="p-2 rounded-xl bg-blue-500 text-white hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};
```

### 7. Dynamic Chart Component (`frontend/src/components/charts/DynamicChart.tsx`)

```tsx
import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface ChartData {
  series?: Array<Record<string, unknown>>;
  xKey?: string;
  yKey?: string;
  [key: string]: unknown;
}

interface DynamicChartProps {
  type: 'bar_chart' | 'line_chart' | 'radar_chart' | 'pie_chart' | 'table';
  data: ChartData;
  title?: string;
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

export const DynamicChart: React.FC<DynamicChartProps> = ({ type, data, title }) => {
  const series = data.series || [];
  const xKey = data.xKey || 'name';
  const yKey = data.yKey || 'value';

  if (series.length === 0) {
    return <p className="text-gray-500 text-center">No data available</p>;
  }

  const renderChart = () => {
    switch (type) {
      case 'bar_chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={series}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={yKey} fill="#3B82F6" radius={[4, 4, 0, 0]}>
                {series.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        );

      case 'line_chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={series}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey={yKey}
                stroke="#3B82F6"
                strokeWidth={2}
                dot={{ fill: '#3B82F6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'pie_chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={series}
                dataKey={yKey}
                nameKey={xKey}
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {series.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'radar_chart':
        // Radar chart for rider comparison
        const categories = ['gc', 'tt', 'sprint', 'climber', 'one_day'];
        return (
          <ResponsiveContainer width="100%" height={350}>
            <RadarChart data={categories.map(cat => ({
              category: cat.toUpperCase(),
              ...series.reduce((acc, rider) => ({
                ...acc,
                [rider.name as string]: (rider[cat] as number) || 0,
              }), {}),
            }))}>
              <PolarGrid />
              <PolarAngleAxis dataKey="category" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              {series.map((rider, index) => (
                <Radar
                  key={rider.name as string}
                  name={rider.name as string}
                  dataKey={rider.name as string}
                  stroke={COLORS[index % COLORS.length]}
                  fill={COLORS[index % COLORS.length]}
                  fillOpacity={0.3}
                />
              ))}
              <Legend />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        );

      case 'table':
        return (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {Object.keys(series[0] || {}).map((key) => (
                    <th
                      key={key}
                      className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {series.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((value, j) => (
                      <td key={j} className="px-4 py-2 text-sm text-gray-900">
                        {String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );

      default:
        return <p>Unsupported chart type</p>;
    }
  };

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      )}
      {renderChart()}
    </div>
  );
};
```

### 8. Ranking Widget (`frontend/src/components/dashboard/widgets/RankingWidget.tsx`)

```tsx
import React, { useEffect, useState } from 'react';
import { rankingsApi, RankingEntry } from '../../../services/api';
import { useWebSocket } from '../../../hooks/useWebSocket';

interface RankingWidgetProps {
  limit?: number;
  title?: string;
}

export const RankingWidget: React.FC<RankingWidgetProps> = ({
  limit = 10,
  title = 'UCI Ranking',
}) => {
  const [rankings, setRankings] = useState<RankingEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  const { subscribe, lastMessage, isConnected } = useWebSocket({
    onMessage: (msg) => {
      if (msg.type === 'ranking_update' && msg.data) {
        setRankings(msg.data as RankingEntry[]);
        setLastUpdate(new Date());
      }
    },
  });

  useEffect(() => {
    const fetchRankings = async () => {
      try {
        const data = await rankingsApi.getIndividual(limit);
        setRankings(data);
        setLastUpdate(new Date());
      } catch (error) {
        console.error('Failed to fetch rankings:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchRankings();
    
    // Subscribe to live updates
    if (isConnected) {
      subscribe('rankings');
    }
  }, [limit, isConnected, subscribe]);

  const getRankChange = (entry: RankingEntry) => {
    const change = entry.prev_rank - entry.rank;
    if (change > 0) return { symbol: '▲', class: 'text-green-500', value: change };
    if (change < 0) return { symbol: '▼', class: 'text-red-500', value: Math.abs(change) };
    return { symbol: '–', class: 'text-gray-400', value: 0 };
  };

  const getFlagEmoji = (nationality: string) => {
    const flags: Record<string, string> = {
      SI: '🇸🇮', BE: '🇧🇪', DK: '🇩🇰', NL: '🇳🇱', GB: '🇬🇧',
      FR: '🇫🇷', IT: '🇮🇹', ES: '🇪🇸', CO: '🇨🇴', US: '🇺🇸',
      DE: '🇩🇪', AU: '🇦🇺', EC: '🇪🇨', PL: '🇵🇱', PT: '🇵🇹',
    };
    return flags[nationality] || '🏳️';
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow p-4 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/2 mb-4" />
        {[...Array(limit)].map((_, i) => (
          <div key={i} className="h-8 bg-gray-100 rounded mb-2" />
        ))}
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow">
      <div className="p-4 border-b flex items-center justify-between">
        <h3 className="font-semibold text-gray-800">{title}</h3>
        <div className="flex items-center gap-2">
          {isConnected && (
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          )}
          {lastUpdate && (
            <span className="text-xs text-gray-500">
              {lastUpdate.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>
      
      <div className="divide-y">
        {rankings.map((entry) => {
          const change = getRankChange(entry);
          return (
            <div
              key={entry.rank}
              className="flex items-center p-3 hover:bg-gray-50 transition-colors"
            >
              <span className="w-8 text-lg font-bold text-gray-400">
                {entry.rank}
              </span>
              
              <span className={`w-8 text-sm ${change.class}`}>
                {change.symbol}
                {change.value > 0 && change.value}
              </span>
              
              <span className="text-xl mr-2">
                {getFlagEmoji(entry.nationality)}
              </span>
              
              <div className="flex-1">
                <p className="font-medium text-gray-800">{entry.rider_name}</p>
                <p className="text-xs text-gray-500">{entry.team_name}</p>
              </div>
              
              <span className="font-semibold text-blue-600">
                {entry.points.toLocaleString()}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
```

### 9. Dashboard Layout (`frontend/src/components/dashboard/DashboardLayout.tsx`)

```tsx
import React from 'react';
import { ChatBox } from '../chat/ChatBox';
import { RankingWidget } from './widgets/RankingWidget';
import { VictoriesWidget } from './widgets/VictoriesWidget';
import { UpcomingRacesWidget } from './widgets/UpcomingRacesWidget';

export const DashboardLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🚴</span>
            <h1 className="text-2xl font-bold text-gray-800">PCS Assistant</h1>
          </div>
          <nav className="flex items-center gap-4">
            <a href="/" className="text-gray-600 hover:text-gray-800">Dashboard</a>
            <a href="/riders" className="text-gray-600 hover:text-gray-800">Riders</a>
            <a href="/races" className="text-gray-600 hover:text-gray-800">Races</a>
            <a href="/rankings" className="text-gray-600 hover:text-gray-800">Rankings</a>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6">
          {/* Chat Section - 5 columns */}
          <div className="col-span-12 lg:col-span-5">
            <div className="h-[calc(100vh-200px)] sticky top-6">
              <ChatBox />
            </div>
          </div>

          {/* Dashboard Widgets - 7 columns */}
          <div className="col-span-12 lg:col-span-7 space-y-6">
            {/* Top Row */}
            <div className="grid grid-cols-2 gap-6">
              <RankingWidget limit={10} title="🏆 PCS Ranking" />
              <VictoriesWidget year={2024} title="🎯 Top Victories 2024" />
            </div>

            {/* Bottom Row */}
            <UpcomingRacesWidget limit={5} title="📅 Upcoming Races" />

            {/* Quick Stats */}
            <div className="grid grid-cols-4 gap-4">
              <StatCard
                title="Total Races"
                value="892"
                change="+12"
                icon="🏁"
              />
              <StatCard
                title="Active Riders"
                value="2,847"
                change="+45"
                icon="🚴"
              />
              <StatCard
                title="WorldTour Teams"
                value="18"
                change="0"
                icon="👥"
              />
              <StatCard
                title="Race Days"
                value="342"
                change="-3"
                icon="📆"
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

interface StatCardProps {
  title: string;
  value: string;
  change: string;
  icon: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, change, icon }) => {
  const isPositive = change.startsWith('+');
  const isNeutral = change === '0';
  
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        <span
          className={`text-sm font-medium ${
            isNeutral
              ? 'text-gray-500'
              : isPositive
              ? 'text-green-500'
              : 'text-red-500'
          }`}
        >
          {change}
        </span>
      </div>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      <p className="text-sm text-gray-500">{title}</p>
    </div>
  );
};
```

### 10. App Entry Point (`frontend/src/App.tsx`)

```tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { DashboardLayout } from './components/dashboard/DashboardLayout';
import { RiderPage } from './pages/RiderPage';
import { RacePage } from './pages/RacePage';
import { RankingsPage } from './pages/RankingsPage';
import { ComparePage } from './pages/ComparePage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />} />
        <Route path="/rider/:slug" element={<RiderPage />} />
        <Route path="/race/:slug/:year" element={<RacePage />} />
        <Route path="/rankings" element={<RankingsPage />} />
        <Route path="/compare" element={<ComparePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

## 🚀 Render Deployment Configuration

### Project Structure for Render

```
pcs-assistant/
├── backend/
│   ├── app/
│   │   └── ... (all backend code)
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   └── ... (all frontend code)
│   ├── package.json
│   ├── vite.config.ts
│   └── _redirects              # For SPA routing on Render Static Site
│
├── render.yaml                 # Render Blueprint (Infrastructure as Code)
└── README.md
```

### render.yaml (Root of Repository)

```yaml
# Render Blueprint - Infrastructure as Code
# Deploy both services with: Connect repo → Select "render.yaml"

services:
  # ===================
  # BACKEND - Web Service
  # ===================
  - type: web
    name: pcs-assistant-api
    runtime: python
    region: frankfurt  # or: oregon, ohio, singapore
    plan: free  # free | starter | standard | pro
    
    # Build Configuration
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    
    # Health Check
    healthCheckPath: /health
    
    # Environment Variables
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ANTHROPIC_API_KEY
        sync: false  # Manual input required in Render Dashboard
      - key: ALLOWED_ORIGINS
        value: https://pcs-assistant.onrender.com,http://localhost:5173
      - key: DEBUG
        value: false
      - key: CACHE_TTL_DEFAULT
        value: 300
      - key: CACHE_TTL_RANKINGS
        value: 600

    # Auto-deploy on push to main
    autoDeploy: true

  # ===================
  # FRONTEND - Static Site
  # ===================
  - type: web
    name: pcs-assistant
    runtime: static
    region: frankfurt
    plan: free
    
    # Build Configuration
    rootDir: frontend
    buildCommand: npm ci && npm run build
    staticPublishPath: dist
    
    # Environment Variables (Build-time)
    envVars:
      - key: VITE_API_URL
        value: https://pcs-assistant-api.onrender.com
      - key: VITE_WS_URL
        value: wss://pcs-assistant-api.onrender.com/ws/live
    
    # SPA Routing - Redirect all paths to index.html
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    
    # Headers for security and caching
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
      - path: /assets/*
        name: Cache-Control
        value: public, max-age=31536000, immutable

    autoDeploy: true

  # ===================
  # OPTIONAL: Redis Cache
  # ===================
  # Uncomment for production caching
  # - type: redis
  #   name: pcs-assistant-cache
  #   plan: free  # 25MB limit on free
  #   ipAllowList: []  # Allow all IPs (restrict in production)
```

### Backend Configuration for Render

#### requirements.txt (Updated for Render)

```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
anthropic>=0.18.0
procyclingstats>=0.2.3
httpx>=0.26.0
python-multipart>=0.0.6
websockets>=12.0
unidecode>=1.3.8
gunicorn>=21.2.0

# Testing (optional, exclude if needed)
pytest>=7.4.0
pytest-asyncio>=0.23.0
```

#### config.py (Updated for Render)

```python
"""
Application configuration - Render compatible.
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
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
    
    # Claude API
    ANTHROPIC_API_KEY: str
    
    # Cache
    CACHE_TTL_DEFAULT: int = 300
    CACHE_TTL_RANKINGS: int = 600
    CACHE_TTL_RIDER: int = 900
    
    # Redis (optional - for Render Redis)
    REDIS_URL: str | None = None
    
    # Rate limiting
    RATE_LIMIT_PCS: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

#### main.py (Updated for Render)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.api.routes import chat, riders, races, teams, rankings, stats
from app.api.websocket import websocket_router
from app.services.cache_service import CacheService
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.cache = CacheService()
    await app.state.cache.start()
    yield
    # Shutdown
    await app.state.cache.close()

app = FastAPI(
    title="PCS Assistant API",
    description="AI-powered cycling statistics assistant",
    version="1.0.0",
    lifespan=lifespan,
    # Render health checks
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS - Critical for Render deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(riders.router, prefix="/api/riders", tags=["Riders"])
app.include_router(races.router, prefix="/api/races", tags=["Races"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(rankings.router, prefix="/api/rankings", tags=["Rankings"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])

@app.get("/health")
async def health_check():
    """Health check endpoint for Render."""
    return {
        "status": "healthy",
        "service": "pcs-assistant-api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PCS Assistant API",
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
        "health": "/health"
    }
```

### Frontend Configuration for Render

#### vite.config.ts (Updated for Render)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  
  // Build optimization for production
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts'],
        },
      },
    },
  },
  
  // Environment variables
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL),
    'import.meta.env.VITE_WS_URL': JSON.stringify(process.env.VITE_WS_URL),
  },
});
```

#### frontend/_redirects (For SPA Routing)

```
/* /index.html 200
```

#### frontend/src/services/api.ts (Updated for Render)

```typescript
import axios, { AxiosInstance } from 'axios';

// Render URLs - fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live';

// Export for WebSocket hook
export const getWebSocketUrl = () => WS_BASE_URL;

const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  // Important for CORS with credentials
  withCredentials: false,
});

// ... rest of the API code remains the same
```

#### frontend/src/hooks/useWebSocket.ts (Updated for Render)

```typescript
import { useEffect, useRef, useCallback, useState } from 'react';
import { getWebSocketUrl } from '../services/api';

// Use the exported function to get WebSocket URL
const WS_URL = getWebSocketUrl();

// ... rest of the hook code remains the same
```

### Environment Variables on Render

#### Backend (Web Service)

| Variable | Value | Notes |
|----------|-------|-------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | **Secret** - Add manually in dashboard |
| `PYTHON_VERSION` | `3.11.0` | Python runtime version |
| `ALLOWED_ORIGINS` | `https://pcs-assistant.onrender.com` | Your frontend URL |
| `DEBUG` | `false` | Disable in production |
| `CACHE_TTL_DEFAULT` | `300` | Cache TTL in seconds |
| `REDIS_URL` | (auto-linked) | If using Render Redis |

#### Frontend (Static Site)

| Variable | Value | Notes |
|----------|-------|-------|
| `VITE_API_URL` | `https://pcs-assistant-api.onrender.com` | Backend URL |
| `VITE_WS_URL` | `wss://pcs-assistant-api.onrender.com/ws/live` | WebSocket URL (wss:// for HTTPS) |

### Deployment Steps on Render

#### Option 1: Using render.yaml (Recommended)

1. **Push code to GitHub/GitLab**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com) → Dashboard
   - Click **"New"** → **"Blueprint"**
   - Connect your GitHub/GitLab repo
   - Render auto-detects `render.yaml`
   - Review services and click **"Apply"**

3. **Add Secret Environment Variables**
   - Go to Backend service → Environment
   - Add `ANTHROPIC_API_KEY` manually (marked as secret)

4. **Wait for Deploy**
   - First deploy takes ~5-10 minutes
   - Backend: `https://pcs-assistant-api.onrender.com`
   - Frontend: `https://pcs-assistant.onrender.com`

#### Option 2: Manual Setup

**Backend (Web Service):**
```
Name: pcs-assistant-api
Region: Frankfurt (EU) / Oregon (US)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Frontend (Static Site):**
```
Name: pcs-assistant
Region: Frankfurt (EU) / Oregon (US)  
Branch: main
Root Directory: frontend
Build Command: npm ci && npm run build
Publish Directory: dist
```

### WebSocket on Render

Render supports WebSockets on Web Services. Key points:

1. **Use `wss://`** for production (HTTPS)
2. **Ping/pong** to keep connection alive (Render timeout: 60s idle)
3. **Reconnection logic** in frontend is essential

```typescript
// Updated WebSocket hook with Render-friendly keepalive
const PING_INTERVAL = 30000; // 30 seconds - keep under Render's 60s timeout

// Inside useWebSocket hook:
ws.onopen = () => {
  setIsConnected(true);
  
  // Keep connection alive for Render
  const pingInterval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'ping' }));
    }
  }, PING_INTERVAL);

  ws.onclose = () => {
    clearInterval(pingInterval);
    // ... reconnection logic
  };
};
```

### Free Tier Limitations

| Service | Free Tier Limit | Notes |
|---------|-----------------|-------|
| Web Service | 750 hours/month | Sleeps after 15min inactivity |
| Static Site | Unlimited | No sleep, always available |
| Redis | 25MB | Shared instance |
| Bandwidth | 100GB/month | Across all services |

**Cold Start Warning:** Free tier web services sleep after inactivity. First request after sleep takes ~30-60 seconds. Solutions:
- Upgrade to Starter ($7/month) for always-on
- Use external cron to ping `/health` every 14 minutes
- Accept cold starts for hobby projects

### Monitoring on Render

1. **Logs**: Dashboard → Service → Logs (real-time)
2. **Metrics**: Dashboard → Service → Metrics (CPU, Memory, Requests)
3. **Alerts**: Settings → Notifications (deploy success/failure)

### Custom Domain (Optional)

1. Go to Service → Settings → Custom Domains
2. Add your domain (e.g., `api.pcs-assistant.com`)
3. Configure DNS:
   ```
   CNAME: api.pcs-assistant.com → pcs-assistant-api.onrender.com
   ```
4. Render auto-provisions SSL certificate

---

## 📋 Implementation Checklist

### Phase 1: Backend Core ✓
- [ ] FastAPI setup with CORS
- [ ] PCS Scraper service with procyclingstats
- [ ] Cache service (in-memory)
- [ ] Entity resolver (names → slugs)
- [ ] Basic API routes (riders, races, rankings)

### Phase 2: AI Integration ✓
- [ ] Claude API integration
- [ ] Query planning (intent classification)
- [ ] Natural language response generation
- [ ] Visualization data preparation

### Phase 3: Frontend Core ✓
- [ ] React + Vite + TypeScript setup
- [ ] API service layer
- [ ] Chat components (ChatBox, ChatMessage, ChatInput)
- [ ] Basic routing

### Phase 4: Dashboard & Charts ✓
- [ ] Dashboard layout
- [ ] Ranking widget with live updates
- [ ] Victories chart widget
- [ ] Dynamic chart component (bar, line, radar, pie)
- [ ] Upcoming races widget

### Phase 5: Real-time Features ✓
- [ ] WebSocket server (FastAPI)
- [ ] WebSocket client hook (React)
- [ ] Live ranking updates
- [ ] Connection status indicator

### Phase 6: Polish & Deploy
- [ ] Error handling and loading states
- [ ] Responsive design
- [ ] Render configuration (render.yaml)
- [ ] Environment variables
- [ ] Documentation

---

## 🚀 Quick Start Commands

### Local Development

```bash
# Clone and setup
git clone <repo>
cd pcs-assistant

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env  # Add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Deploy to Render

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main

# 2. Go to render.com
#    - New → Blueprint
#    - Connect your repo
#    - Render detects render.yaml automatically
#    - Add ANTHROPIC_API_KEY in dashboard
#    - Deploy!

# Your URLs will be:
# Backend: https://pcs-assistant-api.onrender.com
# Frontend: https://pcs-assistant.onrender.com
```

---

## 📝 Notes for Claude

When generating code for this project:

1. **Use TypeScript** for frontend, **Python 3.11+** for backend
2. **Follow the folder structure** exactly as specified
3. **Use async/await** consistently
4. **Add proper error handling** with user-friendly messages
5. **Include loading states** for all async operations
6. **Use Tailwind CSS** for styling (no custom CSS files)
7. **Keep components small** and focused
8. **Add JSDoc/docstrings** for all functions
9. **Use Pydantic models** for API request/response validation
10. **Implement proper caching** to avoid rate limiting from PCS

### Render-Specific Considerations:

11. **Use environment variables** for all config (never hardcode URLs)
12. **Use `$PORT`** for backend port (Render provides this)
13. **Use `wss://`** for WebSocket in production (not `ws://`)
14. **Implement reconnection logic** for WebSocket (Render has idle timeout)
15. **Keep WebSocket alive** with ping/pong every 30 seconds
16. **Add `/health` endpoint** for Render health checks
17. **Configure CORS** to allow your Render frontend URL

When the user asks to generate specific parts:
- Generate complete, working code
- Include all imports
- Add proper TypeScript types
- Include error handling
- Add comments for complex logic
- Ensure Render compatibility (env vars, ports, CORS)
