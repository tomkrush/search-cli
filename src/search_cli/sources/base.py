"""Common interface for search index sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """A single search hit, normalized across sources."""

    title: str
    url: str
    snippet: str = ""
    published_date: str | None = None
    score: float | None = None
    extra: dict = field(default_factory=dict)

    @property
    def display_title(self) -> str:
        return self.title or self.url


class SearchSource(ABC):
    """Adapter interface implemented by each search index backend."""

    #: short name used on the CLI, e.g. --source exa
    name: str = "base"
    #: human-readable description for `search-cli sources`
    description: str = ""

    @abstractmethod
    def search(self, query: str, num_results: int) -> list[SearchResult]:
        """Search the backend and return up to `num_results` hits."""
        raise NotImplementedError

    def close(self) -> None:
        """Release any resources (clients, connections). Optional."""
