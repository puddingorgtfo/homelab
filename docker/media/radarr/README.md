# Radarr

Automatic movie management. Same concept as Sonarr but for movies — monitors for releases,
grabs them via qBittorrent, and organises them into your library.

## Ports

| Port | Purpose |
|------|---------|
| 7878 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `PUID` / `PGID` | User/group ID for file permissions |
| `TZ` | Timezone |

## Notes

- Requires Prowlarr (indexers) and qBittorrent (download client) to be configured first.
- Setup is the same as Sonarr — add Prowlarr as indexer source, add qBittorrent as download client.
- **Official docs**: https://wiki.servarr.com/radarr
