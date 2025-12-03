"""
AI Service for natural language processing.

Supports both OpenAI and Anthropic APIs based on configuration.

Handles:
- Intent classification
- Query planning
- Natural language response generation
"""

from typing import Dict, Any, Optional
import json
import re

from app.config import settings
from app.services.pcs_scraper import PCSScraperService


class AIService:
    """AI integration for natural language cycling queries."""

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
Keep responses concise but informative."""

    QUERY_PLANNING_PROMPT = """Analyze this cycling question and determine what data to fetch.

Question: {question}

Return a JSON object with:
{{
    "intent": "rider_info|rider_victories|rider_results|race_results|race_startlist|team_info|ranking|comparison|statistics|general",
    "entities": {{
        "riders": ["slug1", "slug2"],
        "races": ["race-slug"],
        "teams": ["team-slug"],
        "year": 2024,
        "stage": null
    }},
    "filters": {{
        "year": 2024,
        "race_type": null,
        "limit": 10
    }},
    "visualization": "bar_chart|line_chart|radar_chart|table|none",
    "comparison_mode": false
}}

Common rider slugs:
- Tadej Pogacar: tadej-pogacar
- Jonas Vingegaard: jonas-vingegaard
- Remco Evenepoel: remco-evenepoel
- Wout van Aert: wout-van-aert
- Mathieu van der Poel: mathieu-van-der-poel
- Primoz Roglic: primoz-roglic

Common race slugs:
- Tour de France: tour-de-france
- Giro d'Italia: giro-d-italia
- Vuelta a Espana: vuelta-a-espana
- Paris-Roubaix: paris-roubaix
- Tour of Flanders: tour-of-flanders
- Milano-Sanremo: milano-sanremo

Only return valid JSON, no explanation."""

    def __init__(self, scraper: PCSScraperService):
        self.scraper = scraper
        self.model = settings.AI_MODEL
        self.is_anthropic = self.model.startswith("claude")

        # Initialize the appropriate client
        if self.is_anthropic:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _call_llm(self, messages: list, max_tokens: int = 1000, system: str = None) -> str:
        """Call the LLM with the appropriate API format."""
        if self.is_anthropic:
            # Anthropic API format
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages
            }
            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        else:
            # OpenAI API format
            openai_messages = []
            if system:
                openai_messages.append({"role": "system", "content": system})
            openai_messages.extend(messages)

            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=openai_messages
            )
            return response.choices[0].message.content

    async def plan_query(self, question: str) -> Dict[str, Any]:
        """
        Analyze user question and create a query plan.

        Returns structured plan for data fetching.
        """
        try:
            response_text = self._call_llm(
                messages=[{
                    "role": "user",
                    "content": self.QUERY_PLANNING_PROMPT.format(question=question)
                }],
                max_tokens=1000
            ).strip()

            # Try to find JSON in the response
            if response_text.startswith("{"):
                plan = json.loads(response_text)
            else:
                # Try to extract JSON from markdown code block
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group(1))
                else:
                    plan = json.loads(response_text)

            return plan

        except (json.JSONDecodeError, Exception):
            # Fallback to basic intent
            return {
                "intent": "general",
                "entities": {},
                "filters": {},
                "visualization": "none",
                "comparison_mode": False
            }

    async def execute_query(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the query plan and fetch required data."""
        intent = plan.get("intent", "general")
        entities = plan.get("entities", {})
        filters = plan.get("filters", {})

        data = {}

        try:
            if intent == "rider_info" and entities.get("riders"):
                for rider_slug in entities["riders"][:3]:
                    rider_data = await self.scraper.get_rider(rider_slug)
                    data[rider_slug] = rider_data

            elif intent == "rider_victories" and entities.get("riders"):
                year = filters.get("year")
                for rider_slug in entities["riders"][:3]:
                    rider_data = await self.scraper.get_rider_victories(rider_slug, year)
                    data[rider_slug] = rider_data

            elif intent == "race_results" and entities.get("races"):
                year = filters.get("year") or entities.get("year") or 2024
                stage = entities.get("stage")
                for race_slug in entities["races"][:3]:
                    race_data = await self.scraper.get_race_results(race_slug, year, stage)
                    data[race_slug] = race_data

            elif intent == "race_startlist" and entities.get("races"):
                year = filters.get("year") or entities.get("year") or 2024
                for race_slug in entities["races"][:3]:
                    startlist_data = await self.scraper.get_race_startlist(race_slug, year)
                    data[race_slug] = startlist_data

            elif intent == "ranking":
                ranking_type = filters.get("ranking_type", "individual")
                ranking_data = await self.scraper.get_ranking(ranking_type)
                data["ranking"] = ranking_data

            elif intent == "comparison" and len(entities.get("riders", [])) >= 2:
                for rider_slug in entities["riders"][:4]:
                    rider_data = await self.scraper.get_rider(rider_slug)
                    data[rider_slug] = rider_data

            elif intent == "team_info" and entities.get("teams"):
                year = filters.get("year") or 2024
                for team_slug in entities["teams"][:3]:
                    team_data = await self.scraper.get_team(team_slug, year)
                    data[team_slug] = team_data

        except Exception as e:
            data["error"] = str(e)

        return data

    async def generate_response(
        self,
        question: str,
        data: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate natural language response with optional visualization data."""
        data_context = json.dumps(data, indent=2, default=str)

        try:
            response_text = self._call_llm(
                messages=[{
                    "role": "user",
                    "content": f"""Question: {question}

Data fetched from ProCyclingStats:
```json
{data_context}
```

Query plan: {json.dumps(plan)}

Provide a helpful response based on this data. Be concise and informative.
If there's an error in the data, explain what went wrong."""
                }],
                max_tokens=2000,
                system=self.SYSTEM_PROMPT
            )

        except Exception as e:
            response_text = f"Mi dispiace, si è verificato un errore: {str(e)}"

        result = {
            "message": response_text,
            "data": data,
            "visualization": None
        }

        if plan.get("visualization") != "none" and not data.get("error"):
            viz_data = self._prepare_chart_data(data, plan)
            if viz_data:
                result["visualization"] = {
                    "type": plan.get("visualization"),
                    "data": viz_data
                }

        return result

    def _prepare_chart_data(
        self,
        data: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Transform raw data into chart-ready format."""
        viz_type = plan.get("visualization")
        intent = plan.get("intent")

        if not data or "error" in data:
            return None

        try:
            if viz_type == "bar_chart" and intent in ["rider_victories", "rider_info"]:
                chart_data = []
                for rider, rider_data in data.items():
                    if isinstance(rider_data, dict) and "error" not in rider_data:
                        victories = rider_data.get("victories", [])
                        if isinstance(victories, list):
                            chart_data.append({
                                "name": rider_data.get("name", rider),
                                "victories": len(victories)
                            })
                        elif isinstance(victories, int):
                            chart_data.append({
                                "name": rider_data.get("name", rider),
                                "victories": victories
                            })
                if chart_data:
                    return {"series": chart_data, "xKey": "name", "yKey": "victories"}

            elif viz_type == "radar_chart" and intent == "comparison":
                chart_data = []
                for rider, rider_data in data.items():
                    if isinstance(rider_data, dict) and "error" not in rider_data:
                        specialties = rider_data.get("specialties", {})
                        if isinstance(specialties, dict):
                            chart_data.append({
                                "name": rider_data.get("name", rider),
                                "gc": specialties.get("gc", 0) or 0,
                                "tt": specialties.get("time_trial", 0) or 0,
                                "sprint": specialties.get("sprint", 0) or 0,
                                "climber": specialties.get("climber", 0) or 0,
                                "one_day": specialties.get("one_day_races", 0) or 0
                            })
                if chart_data:
                    return {"series": chart_data}

            elif viz_type == "table" and intent == "ranking":
                ranking = data.get("ranking", {})
                if isinstance(ranking, dict):
                    ranking = ranking.get("ranking", [])
                if isinstance(ranking, list) and ranking:
                    return {"series": ranking[:20], "xKey": "rider_name", "yKey": "points"}

        except Exception:
            pass

        return None

    async def chat(self, question: str) -> Dict[str, Any]:
        """
        Main entry point for chat interactions.

        Orchestrates: plan -> fetch -> respond
        """
        plan = await self.plan_query(question)
        data = await self.execute_query(plan)
        response = await self.generate_response(question, data, plan)
        return response
