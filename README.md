# search-cli

A simple CLI search tool. Provide a search term and number of results; it
returns those results. Backends are pluggable adapters — the first is
[Exa.ai](https://exa.ai/docs/sdks/python-sdk).

## Install

```bash
pip install -e .
export EXA_API_KEY=...   # get a key at https://exa.ai
```

## Usage

```bash
search-cli "rust async runtime" -n 5          # 5 results from exa (default)
search-cli "exa.ai" -n 10 -s exa              # explicit source
search-cli sources                            # list available sources
```

## Adding a new source

1. Subclass `SearchSource` in `src/search_cli/sources/` and implement
   `search(query, num_results) -> list[SearchResult]`.
2. Register it in the `SOURCES` dict in `src/search_cli/sources/__init__.py`.

It automatically becomes available as `--source <name>`.
