# Homelab Project — Claude Instructions

## Credentials
All credentials are in:
  /home/beanz/.claude/projects/-home-beanz/memory/credentials.md

Read that file before doing anything that needs a password, API key, or URL.

## Repo Structure

This repo has two remotes:
- `origin` → public GitHub: https://github.com/puddingorgtfo/homelab (sanitized, no secrets)
- `private` → private GitHub: https://github.com/puddingorgtfo/homelab-private (git-crypt encrypted)

**Current working branch is `public`.** The `private/master` branch has real .env files.

To access encrypted .env files:
```bash
git checkout private/master
git-crypt unlock /home/beanz/homelab-private-git-crypt.key
# read .env files, then switch back:
git checkout public
```

## GITHUB PUSH SAFETY — MANDATORY

Before ANY `git push` to either remote, run a pre-flight check:

**NEVER push to `origin` (public) if any file contains:**
- Passwords, tokens, API keys, secrets
- Real IPs (192.168.x.x, 10.x.x.x, 172.x.x.x)
- Real domain names tied to the homelab (burnhamandsons.com and subdomains)
- Real usernames (beanz, puddingorgtfo, jesseburnham, etc.)
- WireGuard keys, private keys, .pem/.key files
- Any value from credentials.md

**Pushing to `private` remote is OK for encrypted .env files (git-crypt handles it).**

**Quick scan before push:**
```bash
# Scan staged files for secrets before committing
git diff --cached | grep -iE "(password|passwd|secret|token|api.?key|private.?key|apikey|bearer|192\.168\.|10\.\d+\.\d+\.|burnhamandsons\.com|abLounge|sk-ant|sk-or|sk-proj|xai-|GOCSPX|eyJhbG)"
```
If any hits — STOP, sanitize first.

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
  ai/               (AI/LLM services)
  automation/       (automation services)
```

Each service has:
- `compose.yml` — the Docker Compose file
- `.env` — secrets (encrypted on private/master, .env.example on public branch)

## Network & Domains

| What | Value |
|------|-------|
| Domain | burnhamandsons.com |
| Docker host (VM 100) | 192.168.0.78 |
| Proxmox | 192.168.0.188:8006 |
| QNAP NAS | 192.168.0.13 |
| Dashboard | https://home.burnhamandsons.com |
| NPM | http://192.168.0.78:81 |

All services exposed at `*.burnhamandsons.com` via Cloudflare Tunnel → NPM.

## Key Paths (on the running host)

| What | Path |
|------|------|
| Docker configs on NAS | /mnt/nas/docker-configs/ |
| Home Assistant config | /opt/homeassistant/config |
| NAS media | /mnt/nas/movies, /mnt/nas/Tv Shows, /mnt/nas/books |
| NAS data | /mnt/nas/immich/upload, /mnt/nas/paperless/, /mnt/nas/nextcloud/data, /mnt/nas/vaultwarden/data, /mnt/nas/downloads |
| n8n workflows | /home/beanz/n8n-workflows/ |
| NVMe mount (VM 100) | /mnt/nvme — 984GB ext4, UUID f92a1abd-..., n8n data + content media |

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

- Non-secret configs (compose.yml, docs) → commit and push to `origin` (public)
- .env files with real secrets → commit and push to `private` remote ONLY
- NEVER push secrets to `origin`
- Run the pre-flight scan above before every push
