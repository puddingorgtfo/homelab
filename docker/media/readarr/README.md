# Readarr

Automatic e-book and audiobook management. Monitors for new releases, grabs them via
qBittorrent, and organises them into your Calibre library.

## Ports

| Port | Purpose |
|------|---------|
| 8787 | Web UI |

## Notes

- Set up Prowlarr as the indexer source and qBittorrent as the download client.
- Root folder should point to your Calibre library path on the NAS.
- Can work alongside Calibre for a fully automated book pipeline: Readarr grabs books →
  imports into Calibre → available in Audiobookshelf or Calibre-Web for reading.
- **Official docs**: https://wiki.servarr.com/readarr
