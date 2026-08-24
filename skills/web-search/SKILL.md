---
name: web-search
description: Search the web using the search-cli command. Use when the user asks to search the web, look up information online, find articles or documentation, or check for recent news.
---

# Web Search

Search the web using the `search-cli` command. Results are printed with title, URL, snippet, and publish date when available.

## Usage

```bash
# Basic search (default: 5 results from the "exa" source)
search-cli "rust async runtime"

# More results
search-cli "exa.ai" -n 10

# Pick a specific source
search-cli "query" -n 5 -s exa
```

Quote the query when it contains spaces.

## Options

- `-n, --num-results N` — number of results to return (default: 5).
- `-s, --source NAME` — search index source (default: `exa`).

## Listing sources

```bash
search-cli sources
```

## Tips

- Start with the default 5 results; use `-n 10` for broader coverage.
- Use multiple, more specific queries rather than one broad query.
- Prefer recent results when the user asks for current information.
