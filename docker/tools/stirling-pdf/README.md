# Stirling PDF

Browser-based PDF manipulation toolkit. Merge, split, rotate, compress, convert, add
watermarks, OCR, and more — all locally, no data leaves your server.

## Ports

| Port | Purpose |
|------|---------|
| 8080 | Web UI |

## Notes

- No login required by default (`DOCKER_ENABLE_SECURITY=false`).
  Add authentication or put it behind NPM access control if needed.
- OCR (making scanned PDFs text-searchable) is built in via Tesseract.
- Supports many operations that would otherwise require Acrobat Pro.
- **Official docs**: https://github.com/Stirling-Tools/Stirling-PDF
