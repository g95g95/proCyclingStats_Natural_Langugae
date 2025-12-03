"""
Entity Resolver Service

Resolves natural language names to PCS URL slugs.
Examples:
- "Pogacar" -> "tadej-pogacar"
- "Tour de France" -> "tour-de-france"
- "UAE Team Emirates" -> "uae-team-emirates"
"""

from typing import List, Dict, Any
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
        "pidcock": "tom-pidcock",
        "bernal": "egan-bernal",
        "kuss": "sepp-kuss",
        "yates": "adam-yates",
        "mas": "enric-mas",
        "ciccone": "giulio-ciccone",
        "bardet": "romain-bardet",
        "nibali": "vincenzo-nibali",
        "valverde": "alejandro-valverde",
        "sagan": "peter-sagan",
        "viviani": "elia-viviani",
        "philipsen": "jasper-philipsen",
        "merlier": "tim-merlier",
        "girmay": "biniam-girmay",
    }

    # Common race aliases
    RACE_ALIASES = {
        "tour": "tour-de-france",
        "tdf": "tour-de-france",
        "tour de france": "tour-de-france",
        "giro": "giro-d-italia",
        "giro d'italia": "giro-d-italia",
        "giro italia": "giro-d-italia",
        "vuelta": "vuelta-a-espana",
        "vuelta a espana": "vuelta-a-espana",
        "roubaix": "paris-roubaix",
        "paris-roubaix": "paris-roubaix",
        "fiandre": "tour-of-flanders",
        "ronde": "tour-of-flanders",
        "tour of flanders": "tour-of-flanders",
        "flanders": "tour-of-flanders",
        "sanremo": "milano-sanremo",
        "milan-sanremo": "milano-sanremo",
        "milano sanremo": "milano-sanremo",
        "lombardia": "giro-di-lombardia",
        "il lombardia": "giro-di-lombardia",
        "liegi": "liege-bastogne-liege",
        "liege": "liege-bastogne-liege",
        "freccia vallone": "la-fleche-wallonne",
        "fleche wallonne": "la-fleche-wallonne",
        "strade bianche": "strade-bianche",
        "tirreno": "tirreno-adriatico",
        "tirreno adriatico": "tirreno-adriatico",
        "uae tour": "uae-tour",
        "amstel": "amstel-gold-race",
        "amstel gold": "amstel-gold-race",
        "dauphine": "dauphine",
        "criterium dauphine": "dauphine",
        "suisse": "tour-de-suisse",
        "tour de suisse": "tour-de-suisse",
        "romandie": "tour-de-romandie",
        "tour de romandie": "tour-de-romandie",
        "basque": "itzulia-basque-country",
        "pais vasco": "itzulia-basque-country",
        "itzulia": "itzulia-basque-country",
        "catalunya": "volta-a-catalunya",
        "volta catalunya": "volta-a-catalunya",
        "worlds": "world-championship",
        "world championship": "world-championship",
        "worlds rr": "world-championship",
    }

    # Team aliases
    TEAM_ALIASES = {
        "uae": "uae-team-emirates",
        "uae emirates": "uae-team-emirates",
        "visma": "team-visma-lease-a-bike",
        "jumbo": "team-visma-lease-a-bike",
        "jumbo visma": "team-visma-lease-a-bike",
        "ineos": "ineos-grenadiers",
        "sky": "ineos-grenadiers",
        "quick step": "soudal-quick-step",
        "quickstep": "soudal-quick-step",
        "soudal": "soudal-quick-step",
        "deceuninck": "soudal-quick-step",
        "bora": "red-bull-bora-hansgrohe",
        "red bull": "red-bull-bora-hansgrohe",
        "red bull bora": "red-bull-bora-hansgrohe",
        "lidl trek": "lidl-trek",
        "trek": "lidl-trek",
        "alpecin": "alpecin-deceuninck",
        "alpecin deceuninck": "alpecin-deceuninck",
        "ef": "ef-education-easypost",
        "ef education": "ef-education-easypost",
        "education first": "ef-education-easypost",
        "bahrain": "bahrain-victorious",
        "bahrain victorious": "bahrain-victorious",
        "movistar": "movistar-team",
        "jayco": "team-jayco-alula",
        "jayco alula": "team-jayco-alula",
        "cofidis": "cofidis",
        "astana": "astana-qazaqstan-team",
        "intermarche": "intermarche-wanty",
        "lotto": "lotto-dstny",
        "lotto dstny": "lotto-dstny",
        "dsm": "team-dsm-firmenich-postnl",
        "groupama": "groupama-fdj",
        "fdj": "groupama-fdj",
        "ag2r": "decathlon-ag2r-la-mondiale-team",
        "arkea": "arkea-b-b-hotels",
        "uno-x": "uno-x-mobility",
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
            return self.TEAM_ALIASES[normalized]

        return self._name_to_slug(name)

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
