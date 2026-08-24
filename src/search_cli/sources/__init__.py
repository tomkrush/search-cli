"""Registry of available search sources.

To add a new backend:
1. Subclass SearchSource in a new module.
2. Add it to SOURCES below.
"""

from __future__ import annotations

from .base import SearchSource, SearchResult
from .exa_source import ExaSource

# name -> factory (factory lets each source decide its own config/requirements)
SOURCES: dict[str, type[SearchSource]] = {
    ExaSource.name: ExaSource,
}


def get_source(name: str) -> SearchSource:
    available = ", ".join(sorted(SOURCES))
    if name not in SOURCES:
        raise ValueError(f"Unknown source '{name}'. Available: {available}")
    return SOURCES[name]()

