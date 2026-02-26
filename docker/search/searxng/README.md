# SearXNG

Privacy-focused meta-search engine. Aggregates results from Google, Bing, DuckDuckGo,
Brave, Wikipedia, and many others — without tracking you or building a profile.

## Ports

| Port | Purpose |
|------|---------|
| 8082 | Web UI |

## Notes

- Results come from multiple engines simultaneously — you can configure which engines are
  enabled in the admin settings.
- **Browser integration**: Visit SearXNG in your browser and add it as a custom search engine
  via the browser's settings.
- The admin panel (`/preferences`) lets you customise themes, engines, and result categories.
- Rate limiting and bot protection can be configured to prevent abuse if the instance is
  publicly accessible.
- **Official docs**: https://docs.searxng.org/
