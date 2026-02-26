# Jellyfin

Open-source media server — a fully free alternative to Plex with no account or subscription required.

## Ports

| Port | Purpose |
|------|---------|
| 8096 | Web UI and API |

## Configuration

| Variable | Description |
|----------|-------------|
| `PUID` / `PGID` | User/group ID for file permissions |
| `TZ` | Timezone |

## Notes

- No Jellyfin account required — all user management is local.
- Hardware transcoding: add `devices: - /dev/dri:/dev/dri` for Intel Quick Sync or
  configure Nvidia for GPU transcoding.
- Libraries are added through the web UI on first setup.
- **Official docs**: https://jellyfin.org/docs/
