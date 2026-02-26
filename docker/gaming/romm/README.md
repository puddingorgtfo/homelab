# RomM

ROM manager with metadata scraping, artwork, and multi-platform support. Organises your
ROM library with cover art, descriptions, and game details pulled from online databases.

## Ports

| Port | Purpose |
|------|---------|
| 8085 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `ROMM_DB_USER` | MariaDB username |
| `ROMM_DB_PASSWORD` | MariaDB password |
| `MYSQL_ROOT_PASSWORD` | MariaDB root password |
| `ROMM_AUTH_SECRET_KEY` | Secret key for session signing — use a long random string |

## Notes

- ROMs are stored on the NAS and mounted at `/romm/library`. Organise them by platform:
  ```
  /romm/library/
  ├── nes/
  ├── snes/
  ├── n64/
  ├── gba/
  ├── ps1/
  └── ...
  ```
- On first startup, RomM scans the library and scrapes metadata from IGDB and
  MobyGames automatically.
- IGDB API credentials (optional but recommended for metadata quality) are configurable
  in the web UI under Settings.
- Uses MariaDB for storing metadata (the `romm-db` service in the same compose stack).
- **Official docs**: https://romm.app/docs
