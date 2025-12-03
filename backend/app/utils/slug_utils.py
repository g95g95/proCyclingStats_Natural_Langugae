"""URL slug utilities."""

import re
from unidecode import unidecode


def name_to_slug(name: str) -> str:
    """
    Convert a name to a URL-friendly slug.

    Examples:
        "Tadej Pogacar" -> "tadej-pogacar"
        "Jonas Vingegaard" -> "jonas-vingegaard"
    """
    # Remove accents and lowercase
    slug = unidecode(name).lower().strip()
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove non-alphanumeric except hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def slug_to_name(slug: str) -> str:
    """
    Convert a slug back to a readable name.

    Examples:
        "tadej-pogacar" -> "Tadej Pogacar"
        "tour-de-france" -> "Tour De France"
    """
    parts = slug.split('-')
    return ' '.join(part.capitalize() for part in parts)
