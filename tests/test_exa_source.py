"""Tests for the Exa adapter: API response -> SearchResult mapping.

The Exa client is mocked at the system boundary (the Exa SDK class).
"""

from types import SimpleNamespace

import pytest

from search_cli.sources import exa_source
from search_cli.sources.exa_source import ExaSource


def _install_fake_exa(monkeypatch, results):
    """Replace the Exa SDK class with a stub returning canned results."""

    fake_response = SimpleNamespace(results=results)

    class FakeExa:
        def __init__(self, api_key=None):
            pass

        def search(self, query, num_results=None, contents=None):
            return fake_response

    monkeypatch.setattr(exa_source, "Exa", FakeExa)


def test_search_maps_exa_hit_to_search_result(monkeypatch):
    _install_fake_exa(
        monkeypatch,
        [
            SimpleNamespace(
                url="https://example.com/post",
                title="Rust async runtimes",
                text="  A comparison of tokio, async-std, and smol.  ",
                published_date="2024-05-01",
                score=0.91,
            )
        ],
    )
    source = ExaSource(api_key="test-key")
    results = source.search("rust async runtime", 5)

    assert len(results) == 1
    r = results[0]
    assert r.title == "Rust async runtimes"
    assert r.url == "https://example.com/post"
    assert r.snippet == "A comparison of tokio, async-std, and smol."
    assert r.published_date == "2024-05-01"
    assert r.score == 0.91
    assert r.extra == {"source": "exa"}


def test_search_snippet_falls_back_to_highlighted_text(monkeypatch):
    _install_fake_exa(
        monkeypatch,
        [SimpleNamespace(url="https://example.com", highlighted_text="  hit  ")],
    )
    source = ExaSource(api_key="test-key")
    results = source.search("query", 1)

    assert results[0].snippet == "hit"
    assert results[0].title == ""


def test_search_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="EXA_API_KEY"):
        ExaSource()
