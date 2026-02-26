# Linkwarden

Bookmark manager with full-page archiving. Save links with a local snapshot so they
remain accessible even if the original page goes offline.

## Ports

| Port | Purpose |
|------|---------|
| 3000 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `LINKWARDEN_DB_PASSWORD` | PostgreSQL database password |
| `LINKWARDEN_SECRET` | NextAuth secret key (generate a random string) |
| `LINKWARDEN_URL` | Public URL of your Linkwarden instance |
| `MEDIA_PATH` | Path where archived page snapshots are stored |

## Notes

- Each saved link gets a full-page screenshot and HTML archive stored locally.
- Browser extension available for quick saves from any page.
- Collections and tags for organisation.
- Uses PostgreSQL for the database (included in the same compose stack).
- **Official docs**: https://docs.linkwarden.app/
