"""Tests for SearchResult display behavior."""

from search_cli.sources.base import SearchResult


def test_display_title_uses_title_when_present():
    result = SearchResult(title="Rust async runtimes", url="https://example.com")
    assert result.display_title == "Rust async runtimes"


def test_display_title_falls_back_to_url_when_title_missing():
    result = SearchResult(title="", url="https://example.com")
    assert result.display_title == "https://example.com"
