# Homelab Project — Claude Instructions

## Credentials
All credentials are in:
  /home/beanz/.claude/projects/-home-beanz/memory/credentials.md

Read that file before doing anything that needs a password, API key, or URL.

## Repo Structure

This repo has two remotes:
- `origin` → public GitHub (sanitized, no secrets)
- `private` → homelab-private GitHub (git-crypt encrypted .env files)

**Current working branch is `public`.** The `private/master` branch has real .env files.

To access encrypted .env files:
```bash
git checkout private/master
git-crypt unlock /home/beanz/homelab-private-git-crypt.key
# read .env files, then switch back:
git checkout public
```

## Docker Compose Layout

```
docker/
  infrastructure/   nginx-proxy-manager, pihole, cloudflared, homepage, tailscale
  media/            plex, jellyfin, sonarr, radarr, prowlarr, seerr, readarr,
                    audiobookshelf, calibre, qbittorrent (tunneled via gluetun)
  monitoring/       uptime-kuma, speedtest-tracker
  photos/           immich
  productivity/     nextcloud, vaultwarden, paperless-ngx, wordpress, mealie,
                    linkwarden, stirling-pdf, it-tools, dumbpad
  search/           searxng
  smart-home/       homeassistant, zigbee2mqtt, mosquitto
  tools/            n8n, flaresolverr
  gaming/           romm
```

Each service has:
- `compose.yml` — the Docker Compose file
- `.env` — secrets (encrypted on private/master, .env.example on public)

## Key Paths (on the running host)

| What | Path |
|------|------|
| Docker configs on NAS | /mnt/nas/docker-configs/ (sonarr, radarr, prowlarr, readarr, plex, qbittorrent, audiobookshelf, calibre, overseerr) |
| Home Assistant config | /opt/homeassistant/config |
| NAS media | /mnt/nas/movies, /mnt/nas/Tv Shows, /mnt/nas/books |
| NAS data | /mnt/nas/immich/upload, /mnt/nas/paperless/, /mnt/nas/nextcloud/data, /mnt/nas/vaultwarden/data, /mnt/nas/downloads |
| n8n workflows | /home/beanz/n8n-workflows/ |

## Deploying / Restarting Services

```bash
# Restart a service
docker compose -f /home/beanz/homelab/docker/<category>/<service>/compose.yml restart

# View logs
docker logs <container-name> --tail 50 -f

# All running containers
docker ps
```

## Pushing Changes

- Changes to compose files or non-secret configs → commit and push to `origin` (public)
- Changes to .env files with real secrets → commit and push to `private` remote only
- Never push secrets to `origin`

## Network & Domains

- All services exposed at `*.yourdomain.com` via Cloudflare Tunnel → NPM
- Internal access at `<DOCKER_HOST_IP>:<port>` (Docker host IP)
- Proxmox at `<PROXMOX_IP>:8006`
- NAS at `<NAS_IP>`
- NPM proxy host reference: docker/infrastructure/nginx-proxy-manager/proxy-hosts.md
