# Plex

Primary media server. Streams movies, TV, music, and photos to any device.

## Ports

| Port | Purpose |
|------|---------|
| 32400 | Plex web UI and API |

## Configuration

| Variable | Description |
|----------|-------------|
| `PLEX_CLAIM` | Claim token from plex.tv/claim — links the server to your Plex account (one-time setup) |
| `PUID` / `PGID` | User/group ID for file permissions |
| `TZ` | Timezone |

## Notes

- Media files are served from the NAS mount. Add libraries in Plex pointing to the
  relevant NAS paths.
- Hardware transcoding requires passing through the GPU or iGPU device to the container.
  Add `devices: - /dev/dri:/dev/dri` for Intel Quick Sync.
- After initial setup, `PLEX_CLAIM` is no longer needed and can be removed from `.env`.
- **Official docs**: https://support.plex.tv/
