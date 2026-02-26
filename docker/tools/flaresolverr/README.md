# FlareSolverr

Proxy server that bypasses Cloudflare and DDoS-GUARD challenges. Used by Prowlarr to
access torrent indexers that are protected by Cloudflare's bot detection.

## Ports

| Port | Purpose |
|------|---------|
| 8191 | Proxy API |

## Notes

- Not accessed directly by users — it's configured in Prowlarr as a proxy.
- In Prowlarr: Settings → Indexers → Add → FlareSolverr → URL: `http://flaresolverr:8191`
- Only assign FlareSolverr to indexers that actually need it (Cloudflare-protected ones).
  Using it for all indexers is slower and unnecessary.
- **Official docs**: https://github.com/FlareSolverr/FlareSolverr
