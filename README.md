# Homelab Infrastructure

Self-hosted services running on Proxmox with Docker containers on an Ubuntu 24.04 VM.

## Architecture

```
Proxmox VE 9.1 (2x Xeon E5-2640 v2, 128GB RAM)
├── VM 100 - Ubuntu 24.04 (Primary Docker host)
│   ├── 45+ Docker containers (see Services below)
│   ├── Nginx Proxy Manager (reverse proxy + SSL)
│   ├── Pi-hole (DNS + ad blocking)
│   ├── Cloudflare Tunnel (external access)
│   ├── GPU passthrough (PCIe)
│   └── NFS mount to QNAP NAS (26TB media storage)
├── VM 101 - Windows 11 (UEFI + TPM, stopped)
├── VM 102 - CachyOS (stopped)
├── VM 103 - Windows (stopped)
├── CT 104 - Tailscale Bridge (LXC, always-on)
└── Storage: 232GB SSD boot + 26TB NAS
```

See [proxmox/](proxmox/) for detailed host configuration, VM inventory, storage, and network docs.

## Automation & Monitoring

An always-on monitoring and auto-remediation system built on n8n watches all services,
automatically restarts failures, and provides a Telegram chat bot for on-demand control.

See [docker/automation/n8n/README.md](docker/automation/n8n/README.md) for full documentation
including what the Telegram bot can do and example conversations.

## Services

### Media & Entertainment

Full media server stack with automated TV and movie management. Downloads route through
Mullvad VPN. See [docker/media/](docker/media/) for the full stack overview.

| Service | Description | Port |
|---------|-------------|------|
| [Plex](docker/media/plex/) | Media server | 32400 |
| [Jellyfin](docker/media/jellyfin/) | Open-source media server | 8096 |
| [Sonarr](docker/media/sonarr/) | TV series automation | 8989 |
| [Radarr](docker/media/radarr/) | Movie automation | 7878 |
| [Prowlarr](docker/media/prowlarr/) | Indexer manager | 9696 |
| [Seerr](docker/media/seerr/) | Media request portal | 5055 |
| [Readarr](docker/media/readarr/) | E-book automation | 8787 |
| [Audiobookshelf](docker/media/audiobookshelf/) | Audiobook and podcast server | 13378 |
| [Calibre](docker/media/calibre/) | E-book management & format conversion | - |
| [qBittorrent + Gluetun VPN](docker/media/qbittorrent/) | Torrent client inside Mullvad VPN | 8080 |

### Photos

| Service | Description | Port |
|---------|-------------|------|
| [Immich](docker/photos/immich/) | Photo & video management — Google Photos alternative with mobile app | 2283 |

### Smart Home

Home Assistant as the hub, with Mosquitto (MQTT broker) and Zigbee2MQTT for Zigbee devices.
See [docker/smart-home/](docker/smart-home/) for stack details.

| Service | Description | Port |
|---------|-------------|------|
| [Home Assistant](docker/smart-home/homeassistant/) | Home automation hub | 8123 |
| [Zigbee2MQTT](docker/smart-home/zigbee2mqtt/) | Zigbee to MQTT bridge | 8080 |
| [Mosquitto](docker/smart-home/mosquitto/) | MQTT broker | 1883 |

### Productivity

| Service | Description | Port |
|---------|-------------|------|
| [Nextcloud](docker/productivity/nextcloud/) | File sync & collaboration — self-hosted Google Drive | 80 |
| [Paperless-NGX](docker/productivity/paperless-ngx/) | Document management with OCR | 8010 |
| [Vaultwarden](docker/productivity/vaultwarden/) | Password manager (Bitwarden compatible) | 8080 |
| [WordPress](docker/productivity/wordpress/) | Website / blog | 8088 |
| [Mealie](docker/productivity/mealie/) | Recipe manager & meal planner | 9000 |
| [Linkwarden](docker/productivity/linkwarden/) | Bookmark manager with page archiving | 3000 |
| [Trilium](docker/productivity/trilium/) | Hierarchical note-taking | 8080 |

### Search

| Service | Description | Port |
|---------|-------------|------|
| [SearXNG](docker/search/searxng/) | Privacy-focused meta search engine | 8082 |

### Infrastructure

Core networking and access services. See [docker/infrastructure/](docker/infrastructure/) for details.

| Service | Description | Port |
|---------|-------------|------|
| [Nginx Proxy Manager](docker/infrastructure/nginx-proxy-manager/) | Reverse proxy + SSL certs | 80, 81, 443 |
| [Pi-hole](docker/infrastructure/pihole/) | DNS + ad blocking | 53, 8081 |
| [Portainer](docker/infrastructure/portainer/) | Docker management UI | 9443 |
| [Cloudflare Tunnel](docker/infrastructure/cloudflared/) | External access without port forwarding | - |
| [Tailscale](docker/infrastructure/tailscale/) | VPN mesh for remote access | - |
| [Homepage](docker/infrastructure/homepage/) | Service dashboard | 3000 |
| [Uptime Kuma](docker/infrastructure/uptime-kuma/) | Service uptime monitoring | 3001 |
| [Speedtest Tracker](docker/infrastructure/speedtest-tracker/) | Network speed history & graphs | 80 |

### Tools & Automation

| Service | Description | Port |
|---------|-------------|------|
| [n8n](docker/automation/n8n/) | Workflow automation + [AI monitoring & Telegram bot](docker/automation/n8n/README.md) | 5678 |
| [Stirling PDF](docker/tools/stirling-pdf/) | PDF manipulation & conversion | 8080 |
| [IT Tools](docker/tools/it-tools/) | 100+ developer utilities | 80 |
| [FlareSolverr](docker/tools/flaresolverr/) | Cloudflare challenge solver (used by Prowlarr) | 8191 |
| [Dumbpad](docker/tools/dumbpad/) | Simple shared notepad | 3000 |

### Monitoring

| Service | Description | Port |
|---------|-------------|------|
| [Uptime Kuma](docker/monitoring/uptime-kuma/) | Service uptime monitoring | 3001 |
| [Speedtest Tracker](docker/monitoring/speedtest-tracker/) | Network speed history & graphs | 80 |

### AI

| Service | Description | Port |
|---------|-------------|------|
| [Ollama + Open WebUI](docker/ai/ollama/) | Local LLM inference with GPU + chat UI | 11434 (API), 8080 (UI) |

### Gaming

| Service | Description | Port |
|---------|-------------|------|
| [RomM](docker/gaming/romm/) | ROM manager with metadata scraping and artwork | 8085 |

## Storage

- **Boot disk**: 232GB SSD
- **NAS**: NFS mount at `/mnt/nas` — 26TB QNAP for media, Docker configs, and shared data

## Network

- **Reverse Proxy**: Nginx Proxy Manager handles SSL termination and routing
- **DNS**: Pi-hole for local DNS and ad blocking
- **External Access**: Cloudflare Tunnel for select services (no port forwarding required)
- **VPN**: Gluetun container routes torrent traffic through Mullvad VPN
- **Remote Access**: Tailscale VPN mesh

## Getting Started

1. Clone this repository
2. Copy `.env.example` to `.env` in each service directory and fill in your values
3. Run with `docker compose up -d` or import into Portainer
4. See the README in each service directory for configuration notes

## Security Notes

All sensitive values (passwords, API keys, tokens) have been replaced with placeholders.
Search for `your-`, `change-me`, or `CHANGE_ME` to find values you need to set.
