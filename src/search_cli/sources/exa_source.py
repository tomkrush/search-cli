"""Adapter for the Exa.ai search API (https://exa.ai/docs/sdks/python-sdk)."""

from __future__ import annotations

import os

from exa_py import Exa

from .base import SearchSource, SearchResult


class ExaSource(SearchSource):
    name = "exa"
    description = "Exa.ai neural/keyword web search (requires EXA_API_KEY)"

    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or os.environ.get("EXA_API_KEY")
        if not key:
            raise RuntimeError(
                "EXA_API_KEY environment variable is not set. "
                "Get a key at https://exa.ai and export EXA_API_KEY=..."
            )
        self._client = Exa(api_key=key)

    def search(self, query: str, num_results: int) -> list[SearchResult]:
        response = self._client.search(
            query,
            num_results=num_results,
            contents={"text": {"max_characters": 500}},
        )
        results: list[SearchResult] = []
        for r in response.results:
            snippet = ""
            if getattr(r, "text", None):
                snippet = r.text.strip()
            elif getattr(r, "highlighted_text", None):
                snippet = r.highlighted_text.strip()
            results.append(
                SearchResult(
                    title=getattr(r, "title", None) or "",
                    url=r.url,
                    snippet=snippet,
                    published_date=getattr(r, "published_date", None),
                    score=getattr(r, "score", None),
                    extra={"source": self.name},
                )
            )
        return results

    def close(self) -> None:
        pass
