# Prowlarr

Indexer manager for the Arr stack. Manages torrent and usenet indexer configurations in
one place and syncs them to Sonarr, Radarr, and Readarr automatically.

## Ports

| Port | Purpose |
|------|---------|
| 9696 | Web UI |

## Notes

- Add indexers under Indexers in the UI. Prowlarr will push them to connected Arr apps.
- Connect Sonarr/Radarr/Readarr under Settings → Apps — they'll sync automatically.
- FlareSolverr (in `tools/`) can be added as a proxy under Settings → Indexers for
  indexers that require Cloudflare bypass.
- **Official docs**: https://wiki.servarr.com/prowlarr
