# Paperless-NGX

Document management with OCR. Scan or drop in PDFs and images — Paperless automatically
OCRs them, makes them full-text searchable, and lets you tag and archive everything.

## Ports

| Port | Purpose |
|------|---------|
| 8010 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `PAPERLESS_DB_PASSWORD` | Database password |
| `PAPERLESS_SECRET_KEY` | Django secret key (generate a random 50+ character string) |
| `PAPERLESS_URL` | Public URL of your Paperless instance |
| `PAPERLESS_ALLOWED_HOSTS` | Allowed hostnames |
| `PAPERLESS_ADMIN_USER` | Initial admin username |
| `PAPERLESS_ADMIN_PASSWORD` | Initial admin password |
| `PAPERLESS_OCR_LANGUAGE` | OCR language code (e.g. `eng` for English) |
| `TZ` | Timezone |

## Notes

- **Consumption directory**: Drop files into the consumption folder and Paperless will
  auto-import, OCR, and ingest them. Configure your scanner to scan-to-folder here.
- Documents are stored as originals plus OCR'd text — the originals are never modified.
- Tags, correspondents, and document types are all configurable and can be auto-assigned
  via matching rules.
- The web API is available for integration with other tools.
- **Official docs**: https://docs.paperless-ngx.com/
