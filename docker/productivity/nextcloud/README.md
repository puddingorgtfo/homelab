# Nextcloud

Self-hosted file sync, sharing, calendar, contacts, and collaboration suite. The closest
self-hosted equivalent to Google Drive + Google Docs + Google Calendar.

## Ports

| Port | Purpose |
|------|---------|
| 80 | Web UI (proxied via NPM to HTTPS) |

## Configuration

| Variable | Description |
|----------|-------------|
| `NEXTCLOUD_DB_PASSWORD` | Database password |
| `NEXTCLOUD_ADMIN_USER` | Initial admin username |
| `NEXTCLOUD_ADMIN_PASSWORD` | Initial admin password |
| `NEXTCLOUD_TRUSTED_DOMAINS` | Comma-separated list of allowed hostnames |
| `NEXTCLOUD_DATA_DIR` | Where user files are stored (point to NAS) |

## Notes

- Client apps available for Windows, macOS, Linux, iOS, and Android — files sync
  automatically across all devices.
- Enable the Calendar and Contacts apps in the Nextcloud app store for CalDAV/CardDAV
  sync with phones and desktop calendar apps.
- Large file uploads require adjusting PHP memory limits and upload size in Nextcloud config.
- **Official docs**: https://docs.nextcloud.com/
