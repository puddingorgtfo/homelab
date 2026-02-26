# Overseerr

Media request portal — users can search for and request movies or TV shows. Requests
are forwarded automatically to Sonarr or Radarr.

## Ports

| Port | Purpose |
|------|---------|
| 5055 | Web UI |

## Notes

- Connects to Sonarr and Radarr via their APIs.
- Integrates with Plex for showing what's already in the library.
- Users can sign in with their Plex account.
- See also [Seerr](../seerr/) — a fork of Overseerr. Only one is needed.
- **Official docs**: https://docs.overseerr.dev/
