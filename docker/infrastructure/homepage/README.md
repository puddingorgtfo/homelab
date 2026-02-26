# Homepage

Customisable dashboard that aggregates all your self-hosted services into one page with
live status indicators, service widgets, and quick links.

## Ports

| Port | Purpose |
|------|---------|
| 3000 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `HOMEPAGE_ALLOWED_HOSTS` | Comma-separated list of allowed hostnames (e.g. `home.yourdomain.com`) |

## Notes

- Configuration lives in YAML files (services.yaml, bookmarks.yaml, settings.yaml, widgets.yaml)
  mounted from [configs/homepage/](../../../configs/homepage/).
- Homepage connects to the Docker socket (read-only) to auto-detect running containers and
  show their status.
- Service widgets (e.g. Sonarr queue count, Plex active streams) require API keys configured
  in `services.yaml`.
- **Official docs**: https://gethomepage.dev/
