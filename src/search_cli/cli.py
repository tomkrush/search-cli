"""search-cli: search the web with a pluggable set of index sources."""

from __future__ import annotations

import sys

import click

from .sources import SOURCES, get_source
from .sources.base import SearchResult


def _print_results(results: list[SearchResult]) -> None:
    if not results:
        click.echo("No results.")
        return
    for i, r in enumerate(results, start=1):
        header = f"{i}. {r.display_title}"
        click.echo(click.style(header, bold=True))
        click.echo(f"   {r.url}")
        if r.snippet:
            click.echo(f"   {r.snippet}")
        if r.published_date:
            click.echo(f"   published: {r.published_date}")
        click.echo()


class SearchGroup(click.Group):
    """Group that treats `search-cli QUERY ...` as `search-cli search QUERY ...`."""

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        if args and not args[0].startswith("-") and args[0] not in self.commands:
            args = ["search", *args]
        return super().parse_args(ctx, args)


@click.group(cls=SearchGroup)
def main() -> None:
    """Simple CLI search tool with pluggable index sources.

    QUERY is the search term: one or more words, quoted if it contains
    spaces. It is sent to the selected source and the top results are
    printed with title, URL, snippet, and publish date when available.

    `search-cli QUERY ...` is shorthand for `search-cli search QUERY ...`.

    \b
    OPTIONS (search):
      -n, --num-results N   Number of results to return (default: 5)
      -s, --source NAME     Search index source (default: exa;
                            run `search-cli sources` to list)

    \b
    EXAMPLES:
      search-cli "rust async runtime"        5 results from exa
      search-cli "exa.ai" -n 10 -s exa       10 results, explicit source
      search-cli sources                     list available sources
    """


@main.command()
@click.argument("query")
@click.option(
    "-n", "--num-results", default=5, show_default=True,
    help="Number of results to return.",
)
@click.option(
    "-s", "--source", default="exa", show_default=True,
    type=click.Choice(sorted(SOURCES)),
    help="Search index source to use.",
)
def search(query: str, num_results: int, source: str) -> None:
    """Search for QUERY and print the top results.

    QUERY is one or more words. Each result is printed as a numbered
    list with title, URL, snippet, and publish date when available.
    """""
    try:
        backend = get_source(source)
    except Exception as e:  # e.g. missing API key
        click.echo(f"error: {e}", err=True)
        sys.exit(1)
    try:
        results = backend.search(query, num_results)
    except Exception as e:
        click.echo(f"search failed: {e}", err=True)
        sys.exit(1)
    finally:
        backend.close()
    _print_results(results)


@main.command("sources")
def sources_cmd() -> None:
    """List available search sources."""
    for name in sorted(SOURCES):
        click.echo(f"{name:12} {SOURCES[name].description}")


if __name__ == "__main__":
    main()
