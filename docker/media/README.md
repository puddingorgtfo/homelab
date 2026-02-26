# Media

Full media server stack with the Arr suite for automated TV and movie management.
All downloads route through a Mullvad VPN via Gluetun.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Plex](plex/) | Primary media server | 32400 |
| [Jellyfin](jellyfin/) | Open-source media server (Plex alternative) | 8096 |
| [Sonarr](sonarr/) | TV series automation — monitors RSS, grabs episodes | 8989 |
| [Radarr](radarr/) | Movie automation — same as Sonarr but for films | 7878 |
| [Prowlarr](prowlarr/) | Indexer manager — feeds trackers to Sonarr/Radarr | 9696 |
| [qBittorrent + Gluetun](qbittorrent/) | Torrent client running inside Mullvad VPN | 8080 (WebUI via VPN) |
| [Readarr](readarr/) | E-book and audiobook automation | 8787 |
| [Seerr](seerr/) | Media request portal — users can request movies/shows | 5055 |
| [Overseerr](overseerr/) | Alternative media request portal | 5055 |
| [Audiobookshelf](audiobookshelf/) | Audiobook and podcast server | 13378 |
| [Calibre](calibre/) | E-book management and format conversion | 8080 (desktop GUI) |

## How the Arr Stack Works

```
Seerr (requests) → Sonarr/Radarr → Prowlarr (find trackers) → qBittorrent (download via VPN)
                                                                      ↓
                                                              Plex / Jellyfin (serve media)
```

1. User requests media via Seerr
2. Sonarr (TV) or Radarr (movies) searches for it using Prowlarr's indexers
3. Download task is sent to qBittorrent, which routes all traffic through Gluetun VPN
4. Once downloaded, Plex and Jellyfin pick up the new file automatically

## Notes

- qBittorrent has no direct internet access — all traffic goes through the Gluetun VPN
  container. If the VPN disconnects, Gluetun's kill switch cuts the connection entirely.
- Calibre's desktop GUI (port 8080) is the book management interface; Calibre-Web (if running)
  provides a read-only web UI for browsing.
- FlareSolverr (in `tools/`) is used by Prowlarr to bypass Cloudflare challenges on some indexers.
