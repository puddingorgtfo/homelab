# Sonarr

Automatic TV series management. Monitors RSS feeds from Prowlarr, grabs new episodes as
they release, sends downloads to qBittorrent, and renames/moves files on completion.

## Ports

| Port | Purpose |
|------|---------|
| 8989 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `PUID` / `PGID` | User/group ID for file permissions |
| `TZ` | Timezone |

## Notes

- Requires Prowlarr to be set up first (for indexers) and qBittorrent as a download client.
- Connect to Prowlarr via Settings → Indexers → Add Prowlarr as a source.
- Connect to qBittorrent via Settings → Download Clients.
- Root folders (where completed downloads are moved) should point to NAS media paths.
- **Official docs**: https://wiki.servarr.com/sonarr
