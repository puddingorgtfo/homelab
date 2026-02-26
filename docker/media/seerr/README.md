# Seerr

Media request portal. Users can search for and request movies or TV shows — requests go
directly to Sonarr or Radarr for automatic download.

## Ports

| Port | Purpose |
|------|---------|
| 5055 | Web UI |

## Notes

- Connects to Sonarr and Radarr via their APIs — configure under Settings → Services.
- Also integrates with Plex/Jellyfin to show what's already available vs what's being
  requested.
- Users can sign in with their Plex account (no separate registration needed).
- Seerr is a fork of Overseerr — see the [Overseerr](../overseerr/) directory if you
  prefer the original.
- **Official docs**: https://github.com/seerr-team/seerr
