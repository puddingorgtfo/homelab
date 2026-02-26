# Productivity

Personal and office tools for file sync, document management, passwords, notes, and more.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Nextcloud](nextcloud/) | File sync, calendar, contacts — self-hosted Google Drive/Docs alternative | 80 |
| [Paperless-NGX](paperless-ngx/) | Document management with OCR — scan, tag, and search all your documents | 8010 |
| [Vaultwarden](vaultwarden/) | Password manager — Bitwarden-compatible server | 8080 |
| [WordPress](wordpress/) | Website / blog | 8088 |
| [Mealie](mealie/) | Recipe manager and meal planner with shopping lists | 9000 |
| [Linkwarden](linkwarden/) | Bookmark manager with full-page archiving | 3000 |
| [Trilium](trilium/) | Hierarchical note-taking application | 8080 |

## Notes

- **Vaultwarden** works with all standard Bitwarden apps (browser extension, mobile app,
  desktop app). Point them at your Vaultwarden URL instead of `bitwarden.com`.
- **Nextcloud** can replace Google Drive, Google Calendar, and Google Contacts. Clients
  available for Windows, macOS, Linux, iOS, and Android.
- **Paperless-NGX** includes a consumption directory — drop PDFs there and it auto-imports,
  OCRs, and tags them. Configure your scanner to send to that directory.
- **Linkwarden** stores local snapshots of bookmarked pages so links don't go dead.
