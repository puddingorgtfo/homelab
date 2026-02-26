# Homelab Automation System

An always-on monitoring, auto-remediation, and conversational control system built on n8n.
It watches 45+ Docker containers and infrastructure components, automatically restarts
failures, escalates to an AI-generated Telegram alert when it can't fix something, and
provides a Telegram chat bot you can talk to for on-demand status queries and actions.

## Architecture

```
Proxmox Hypervisor
└── VM 100 (Docker host)
    ├── n8n  ─── Workflow A (monitor, every 5 min) ──► auto-restart containers
    │        ├── Workflow B (AI alert, on escalation) ──► Telegram
    │        ├── Workflow C (self-watchdog, every 1 min)
    │        └── Workflow D (chat agent, on Telegram message) ◄──► you
    └── cron ─── n8n-watchdog.sh (every 1 min) ──► Telegram (independent of n8n)
```

## Components

| Component | Trigger | What it does |
|-----------|---------|-------------|
| **Workflow A** — Container & Infrastructure Monitor | Every 5 min | Checks all containers + Proxmox VM, NAS HTTP, internet; auto-restarts failures; tracks retry state in shared JSON file |
| **Workflow B** — AI Diagnosis & Alert | Called by A when max retries hit | Fetches container logs via SSH, sends to Claude AI, formats and sends Telegram alert with diagnosis |
| **Workflow C** — n8n Self-Watchdog | Every 1 min | Monitors n8n's own `/healthz` endpoint; SSH-restarts the container if unhealthy |
| **Workflow D** — Telegram Chat Agent | Incoming Telegram message | Conversational AI bot — query status, restart services, get logs, control the VM |
| **`scripts/n8n-watchdog.sh`** | cron every 1 min | Belt-and-suspenders host watchdog; runs independently of n8n via system cron |

## Telegram Bot — What It Can Do

- **"what's broken?"** / **"show active incidents"** — list services currently down with retry count and time since first failure
- **"restart [service]"** — issue `docker compose restart` for that service
- **"pull and recreate [service]"** — pull latest image and recreate container
- **"[service] logs"** — show last 30 lines of container logs
- **"is the internet working?"** / **"infrastructure status"** — check internet, NAS, Proxmox VM
- **"check VM status"** / **"restart the VM"** / **"start the VM"** — Proxmox API control of VM 100
- **"how much space is left on the NAS?"** — disk usage summary
- **"stop monitoring [service] for now"** — clear it from the incident state so Workflow A stops retrying

### Example Conversations

```
you:  is plex down?
bot:  plex is running (Up 4 hours 12 minutes)

you:  restart sonarr
bot:  Restarting sonarr... done. Container is now running (Up 3 seconds)

you:  what's broken?
bot:  1 active incident:
      sonarr — down 14 min, 2 restart attempts. Waiting for manual fix.

you:  get sonarr logs
bot:  [ERROR] NzbDrone.Core.Indexers.RssParser - XML parse error
      [WARN]  NzbDrone.Core.Download - No available download client
      ... (last 30 lines)

you:  restart the VM
bot:  Warning: n8n will go offline for ~60 seconds while the VM reboots.
      Sending reboot command to Proxmox... done.

you:  how much space is left on the NAS?
bot:  NAS (/mnt/nas): 18.2TB used of 26TB (70%)
      Root (/): 48GB used of 232GB (21%)

you:  stop monitoring sonarr for now, i'll fix it manually
bot:  Cleared sonarr from active incidents. Workflow A will no longer retry it
      until the next time it detects it as down.
```

## Monitored Services

### Critical (max 2 retries before alert)
| Container | Purpose |
|-----------|---------|
| `npm-app-1` | Nginx Proxy Manager — external/internal access |
| `pihole` | DNS — everything breaks if this goes down |
| `cloudflared-tunnel` | External tunnel to Cloudflare |
| `n8n` | This automation system itself |

### Important (max 3 retries before alert)
| Container | Purpose |
|-----------|---------|
| `homeassistant` | Home automation hub |
| `nextcloud-app` | File sync and sharing |
| `immich-immich-server-1` | Photo management |
| `portainer` | Docker management UI |
| `vaultwarden` | Password manager |
| `mosquitto` | MQTT broker for smart home |

### Media / Best-effort (max 1 retry)
`plex`, `jellyfin`, `sonarr`, `radarr`, `prowlarr`, `qbittorrent`, `readarr`, `paperless-web`

## Auto-Remediation Logic

1. **Service goes down** → Workflow A detects it on next 5-min cycle, logs incident
2. **Retry 1** → `docker compose restart`
3. **Retry 2+** → `docker compose pull && docker compose up -d` (fresh image)
4. **Max retries reached** → Workflow B runs: fetches logs, asks Claude AI for diagnosis, sends Telegram alert
5. **Alert sent** → Workflow A stops retrying (status = `awaiting_user`), won't alert again for the same incident
6. **Service recovers** → Workflow A detects it healthy, sends "✅ AUTO-RESOLVED" Telegram, clears incident

Claude AI is invoked **once per incident**, only after retries are exhausted — not on every cycle.

## Infrastructure Checks (beyond containers)

| Check | How | Auto-fix |
|-------|-----|---------|
| Proxmox VM 100 status | Proxmox REST API | Start VM if stopped (max 2 attempts) |
| NAS availability | HTTP to NAS web UI | Alert only (can't fix hardware) |
| NFS mount | `mountpoint -q /mnt/nas` | `sudo mount -a` (max 2 attempts) |
| Internet | HTTPS to cloudflare.com | Alert only |
| Local network | HTTP to NPM on this host | Alert only |

## Shared State

Workflows A and D both read/write `/mnt/nas/n8n/homelab-state.json` — a JSON file on the
NAS mount. This keeps incident state across n8n restarts and makes it available to both
the background monitor and the interactive chat bot.

```json
{
  "incidents": {
    "sonarr": {
      "retries": 2,
      "firstSeen": "2026-02-25T03:00:00Z",
      "status": "awaiting_user"
    }
  },
  "nfs": { "retries": 0, "status": "ok" }
}
```

## Setup

### n8n compose.yml requirements

These are already configured in [compose.yml](compose.yml):

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock   # Docker API access
  - /mnt/nas/n8n:/mnt/nas/n8n                   # Shared state file
group_add:
  - "984"                                         # docker group (for socket access)
environment:
  - NODE_FUNCTION_ALLOW_BUILTIN=*               # Allow http/https/fs in Code nodes
  - NODE_FUNCTION_ALLOW_EXTERNAL=node-ssh       # Allow SSH library in Code nodes
```

### n8n credentials (configured in the n8n UI, not env vars)

| Credential | Used by | What to set |
|------------|---------|-------------|
| SSH credential | All workflows | Host IP, username, password/key for Docker host |
| Telegram Bot API | Workflows B, C, D | Bot token from BotFather |
| Anthropic / OpenRouter | Workflow B | API key for Claude AI |

### Environment variables

For `.env` (used by this compose.yml):

| Variable | Description |
|----------|-------------|
| `N8N_PORT` | n8n HTTP port (default: 5678) |
| `N8N_HOST` | Hostname n8n listens on |
| `N8N_PROTOCOL` | `http` or `https` |
| `N8N_SECURE_COOKIE` | `false` for HTTP |
| `N8N_DATA_DIR` | Persistent data directory (e.g. `/mnt/nas/n8n/data`) |
| `N8N_API_KEY` | n8n API key (for MCP/external access) |
| `WEBHOOK_URL` | Public URL for webhook callbacks (e.g. `https://n8n.yourdomain.com`) |
| `TZ` | Timezone (e.g. `America/New_York`) |

### Host watchdog script

See [scripts/n8n-watchdog.sh](../../scripts/n8n-watchdog.sh) for the host-level cron script.

```bash
chmod +x scripts/n8n-watchdog.sh

# Add to crontab (with env vars inline or exported in your shell profile)
(crontab -l 2>/dev/null; echo "* * * * * TELEGRAM_BOT_TOKEN=<your-token> TELEGRAM_CHAT_ID=<your-chat-id> /home/user/homelab/scripts/n8n-watchdog.sh") | crontab -
```

The host watchdog runs completely independently of n8n — if the container dies and n8n
can't restart itself, the cron script will restart it and send a Telegram alert via raw `curl`.

### State file initialisation

```bash
mkdir -p /mnt/nas/n8n
echo '{"incidents":{},"nfs":{"retries":0,"status":"ok"}}' > /mnt/nas/n8n/homelab-state.json
```
