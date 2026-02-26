# Calibre

E-book management and format conversion. Maintains a library of e-books with metadata,
covers, and format conversion between EPUB, MOBI, PDF, etc.

## Notes

- The desktop GUI runs as a container with a web-accessible VNC or HTTP interface.
  Access it via NPM at the configured subdomain.
- Books library is stored on the NAS; the import directory watches for new files to add.
- Calibre can convert between formats on import (e.g. MOBI → EPUB automatically).
- Works well with Readarr — Readarr downloads books, Calibre manages and converts them.
- For a read-only web UI (browse and download, no management), consider adding
  Calibre-Web as a companion service.
- **Official docs**: https://calibre-ebook.com/help
