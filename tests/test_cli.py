"""Tests for the CLI (main entrypoint) via click's CliRunner.

Only the Exa SDK is faked; the registry and source wiring are real.
"""

from types import SimpleNamespace

from click.testing import CliRunner

from search_cli.cli import main
from search_cli.sources import exa_source

HIT = SimpleNamespace(
    url="https://example.com/post",
    title="Rust async runtimes",
    text="A comparison of tokio, async-std, and smol.",
    published_date="2024-05-01",
    score=0.91,
)


def _install_fake_exa(monkeypatch, results):
    fake_response = SimpleNamespace(results=results)

    class FakeExa:
        def __init__(self, api_key=None):
            pass

        def search(self, query, num_results=None, contents=None):
            return fake_response

    monkeypatch.setattr(exa_source, "Exa", FakeExa)
    monkeypatch.setenv("EXA_API_KEY", "test-key")


def test_search_prints_numbered_results(monkeypatch):
    _install_fake_exa(monkeypatch, [HIT])
    result = CliRunner().invoke(main, ["search", "rust async runtime"])

    assert result.exit_code == 0
    assert "1. Rust async runtimes" in result.output
    assert "https://example.com/post" in result.output
    assert "A comparison of tokio, async-std, and smol." in result.output
    assert "published: 2024-05-01" in result.output


def test_query_is_shorthand_for_search_subcommand(monkeypatch):
    _install_fake_exa(monkeypatch, [HIT])
    result = CliRunner().invoke(main, ["rust async runtime"])

    assert result.exit_code == 0
    assert "1. Rust async runtimes" in result.output


def test_search_prints_no_results_message(monkeypatch):
    _install_fake_exa(monkeypatch, [])
    result = CliRunner().invoke(main, ["search", "query"])

    assert result.exit_code == 0
    assert result.output.strip() == "No results."


def test_missing_api_key_reports_error_and_exits_nonzero(monkeypatch):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    result = CliRunner().invoke(main, ["search", "query"])

    assert result.exit_code == 1
    assert "EXA_API_KEY" in result.stderr


def test_sources_lists_registered_sources(monkeypatch):
    monkeypatch.setenv("EXA_API_KEY", "test-key")
    result = CliRunner().invoke(main, ["sources"])

    assert result.exit_code == 0
    assert "exa" in result.output
