"""Date parsing utilities."""

from datetime import datetime, date
from typing import Optional
import re


def parse_date(date_string: str) -> Optional[date]:
    """
    Parse various date formats.

    Supports:
        - "2024-03-15"
        - "15/03/2024"
        - "March 15, 2024"
        - "15 Mar 2024"
    """
    if not date_string:
        return None

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%d %b %Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string.strip(), fmt).date()
        except ValueError:
            continue

    return None


def format_date(d: date, fmt: str = "%B %d, %Y") -> str:
    """
    Format a date to a readable string.

    Args:
        d: Date to format
        fmt: Format string (default: "March 15, 2024")
    """
    if not d:
        return ""
    return d.strftime(fmt)


def extract_year(date_string: str) -> Optional[int]:
    """Extract year from a date string."""
    if not date_string:
        return None

    # Try to find a 4-digit year
    match = re.search(r'\b(19|20)\d{2}\b', date_string)
    if match:
        return int(match.group())

    return None
