# Search

Privacy-focused web search.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [SearXNG](searxng/) | Meta-search engine — aggregates results from Google, Bing, DuckDuckGo, and others without tracking you | 8082 |

## Notes

- SearXNG acts as a proxy between you and search engines. Your queries don't go to Google
  directly — they go to your SearXNG instance, which forwards them anonymously.
- Can be set as the default search engine in Firefox/Chrome by visiting the SearXNG URL
  and adding it via browser settings.
- Engine selection, result formatting, and UI theme are all configurable in the SearXNG admin.
