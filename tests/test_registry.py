"""Tests for the source registry."""

import pytest

from search_cli.sources import SOURCES, get_source
from search_cli.sources.base import SearchSource


def test_get_source_returns_instance_for_known_name(monkeypatch):
    monkeypatch.setenv("EXA_API_KEY", "test-key")
    source = get_source("exa")
    assert isinstance(source, SearchSource)
    assert source.name == "exa"


def test_get_source_raises_with_available_names_for_unknown():
    with pytest.raises(ValueError, match="Unknown source 'nope'"):
        get_source("nope")


def test_sources_registry_exposes_exa():
    assert "exa" in SOURCES
