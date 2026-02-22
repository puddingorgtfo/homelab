# Homelab Infrastructure

Self-hosted services running on Proxmox with Docker containers on an Ubuntu 24.04 VM.

## Architecture

```
Proxmox VE 9.1 (2x Xeon E5-2640 v2, 128GB RAM)
├── VM 100 - Ubuntu 24.04 (Primary Docker host)
│   ├── 38+ Docker containers (see Services below)
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

## Services

### Media & Entertainment
| Service | Description | Port |
|---------|-------------|------|
| [Plex](docker/media/plex/) | Media server | 32400 |
| [Jellyfin](docker/media/jellyfin/) | Open-source media server | 8096 |
| [Sonarr](docker/media/sonarr/) | TV series automation | 8989 |
| [Radarr](docker/media/radarr/) | Movie automation | 7878 |
| [Prowlarr](docker/media/prowlarr/) | Indexer manager | 9696 |
| [Overseerr](docker/media/overseerr/) | Media request management | 5055 |
| [Readarr](docker/media/readarr/) | E-book automation | 8787 |
| [Audiobookshelf](docker/media/audiobookshelf/) | Audiobook server | 13378 |
| [Calibre](docker/media/calibre/) | E-book management | 3000-3001 |
| [qBittorrent + Gluetun VPN](docker/media/qbittorrent/) | Torrent client with VPN | - |

### Photos
| Service | Description | Port |
|---------|-------------|------|
| [Immich](docker/photos/immich/) | Photo & video management (Google Photos alternative) | 2283 |

### Smart Home
| Service | Description | Port |
|---------|-------------|------|
| [Home Assistant](docker/smart-home/homeassistant/) | Home automation | 8123 |
| [Zigbee2MQTT](docker/smart-home/zigbee2mqtt/) | Zigbee to MQTT bridge | 8080 |
| [Mosquitto](docker/smart-home/zigbee2mqtt/) | MQTT broker | 1883 |

### Productivity
| Service | Description | Port |
|---------|-------------|------|
| [Nextcloud](docker/productivity/nextcloud/) | File sync & collaboration | 80 |
| [Paperless-NGX](docker/productivity/paperless-ngx/) | Document management | 8010 |
| [Vaultwarden](docker/productivity/vaultwarden/) | Password manager (Bitwarden compatible) | 8080 |
| [WordPress](docker/productivity/wordpress/) | Website / blog | 8088 |

### Search
| Service | Description | Port |
|---------|-------------|------|
| [SearXNG](docker/search/searxng/) | Privacy-focused meta search engine | 8082 |

### Infrastructure
| Service | Description | Port |
|---------|-------------|------|
| [Nginx Proxy Manager](docker/infrastructure/nginx-proxy-manager/) | Reverse proxy + SSL certs | 80, 81, 443 |
| [Pi-hole](docker/infrastructure/pihole/) | DNS + ad blocking | 53, 8081 |
| [Portainer](docker/infrastructure/portainer/) | Docker management UI | 9443 |
| [Cloudflare Tunnel](docker/infrastructure/cloudflared/) | Secure external access | - |
| [Homepage](docker/infrastructure/homepage/) | Dashboard | 3000 |

### Tools
| Service | Description | Port |
|---------|-------------|------|
| [n8n](docker/tools/n8n/) | Workflow automation | 5678 |
| [FlareSolverr](docker/tools/flaresolverr/) | Cloudflare challenge solver | 8191 |
| [Dumbpad](docker/tools/dumbpad/) | Simple notepad | 3000 |

## Storage

- **Boot disk**: 232GB SSD
- **NAS**: NFS mount at `/mnt/nas` for media storage

## Network

- **Reverse Proxy**: Nginx Proxy Manager handles SSL termination and routing
- **DNS**: Pi-hole for local DNS and ad blocking
- **External Access**: Cloudflare Tunnel for select services
- **VPN**: Gluetun container routes torrent traffic through Mullvad VPN

## Getting Started

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in your values
3. Import compose files into Portainer or run with `docker compose up -d`
4. See individual service directories for specific configuration notes

## Security Notes

All sensitive values (passwords, API keys, tokens) have been replaced with placeholders. Search for `CHANGE_ME`, `YOUR_`, or `REPLACE` to find values you need to set.
