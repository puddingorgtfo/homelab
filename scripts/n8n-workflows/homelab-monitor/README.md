# Homelab Monitor — n8n Workflows

Four n8n workflows that form a unified homelab monitoring, auto-remediation, and chat agent system.

## Workflows

| File | n8n Name | ID | Active |
|------|----------|----|--------|
| `workflow-health-monitor.json` | Homelab - Health Monitor & Auto-Remediation | `iva9epNCdQabPoMJ` | Yes |
| `workflow-ai-diagnosis.json` | Homelab - AI Diagnosis & Alert | `aG2R53gpq1vCD1NR` | Yes |
| `workflow-watchdog.json` | Homelab - n8n Self-Watchdog | `dD4x4o9c7BKkA8p9` | Yes |
| `workflow-chat-agent.json` | Homelab - Chat Agent | `fcn82ak01ioQQadC` | Yes |

---

## Architecture

```
                    ┌─────────────────────────────────────────────────┐
                    │  Homelab - Health Monitor & Auto-Remediation     │
                    │  (runs every 5 min on schedule)                  │
                    │                                                   │
                    │  1. SSH snapshot: container status, NFS, state   │
                    │  2. HTTP checks: Proxmox, VM100, NAS, internet,  │
                    │     router, NPM, Pi-hole, n8n                    │
                    │  3. Evaluate health & compare to prior state      │
                    │  4. SSH: write state to /mnt/nas/n8n/state.json  │
                    │  5. Branch:                                       │
                    │     a) Docker/NFS issues → SSH remediation        │
                    │     b) Proxmox issues → HTTP: start VM           │
                    │     c) Escalations → calls AI Diagnosis workflow  │ ─────────────────┐
                    │     d) Recoveries → Telegram recovery message     │                  │
                    └─────────────────────────────────────────────────┘                  │
                                                                                          │
                    ┌─────────────────────────────────────────────────┐                  │
                    │  Homelab - AI Diagnosis & Alert (sub-workflow)   │ ◄────────────────┘
                    │                                                   │
                    │  1. Split escalated services into items           │
                    │  2. SSH: fetch last 40 lines of container logs   │
                    │  3. Claude Haiku: diagnose cause + fix steps     │
                    │  4. Telegram: send formatted alert to you        │
                    └─────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────────────────┐
                    │  Homelab - n8n Self-Watchdog                     │
                    │  (runs every 1 min independently)                │
                    │                                                   │
                    │  1. HTTP: check n8n /healthz endpoint            │
                    │  2. If healthy → clear fail counter              │
                    │  3. If unhealthy:                                │
                    │     - Attempts 1-2: SSH restart n8n + Telegram  │
                    │     - Attempt 3+: Telegram max-retries alert    │
                    └─────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────────────────┐
                    │  Homelab - Chat Agent (the Claude bot)           │
                    │  (always-on Telegram webhook)                    │
                    │                                                   │
                    │  Telegram Trigger → Homelab AI Agent             │
                    │  (Claude Sonnet via OpenRouter)                   │
                    │                                                   │
                    │  Tools available to the agent:                   │
                    │  • get_homelab_status — all containers + incidents│
                    │  • get_container_logs — last 30 lines via Docker  │
                    │  • restart_container — via Docker socket          │
                    │  • check_infrastructure — disk, memory, internet  │
                    │  • manage_incidents — list/clear alert state      │
                    │  • proxmox_vm_action — status/reboot/start/stop  │
                    └─────────────────────────────────────────────────┘
```

---

## Prerequisites

### Credentials needed in n8n

| Credential | Type | Used by |
|------------|------|---------|
| SSH Password account | sshPassword | Health Monitor, AI Diagnosis, Watchdog |
| Telegram Bot (Claude) | telegramApi | AI Diagnosis, Chat Agent |
| Anthropic | anthropicApi | AI Diagnosis (Claude Haiku) |
| OpenRouter | openRouterApi | Chat Agent (Claude Sonnet) |

### Infrastructure requirements

- Docker socket mounted at `/var/run/docker.sock` in the n8n container
- NAS NFS mounted at `/mnt/nas` on the Docker host
- State file location: `/mnt/nas/n8n/homelab-state.json` (auto-created)
- SSH access from n8n host to Docker host
- Proxmox API reachable at `https://YOUR_PROXMOX_IP:8006`

---

## Setup Notes

### Importing workflows

1. In n8n: **Settings → Import Workflow** → select each JSON file
2. Set credentials on each node that has `YOUR_CREDENTIAL_ID`
3. Replace all placeholder values:
   - `YOUR_PROXMOX_IP` → your Proxmox host IP
   - `YOUR_SERVER_IP` → your Docker host IP
   - `YOUR_NAS_IP` → your NAS IP
   - `YOUR_ROUTER_IP` → your router/gateway IP
   - `YOUR_CHAT_ID` → your Telegram chat ID
   - `YOUR_PASSWORD` → your Proxmox root password
   - `YOUR_TELEGRAM_BOT_TOKEN` → your Telegram bot token (in the Watchdog HTTP nodes)

### Critical: Health Monitor → AI Diagnosis link

The Health Monitor's `Execute Workflow B` node calls the AI Diagnosis workflow by ID. After importing, update that node with the new ID assigned to `workflow-ai-diagnosis.json`.

### Chat Agent Docker socket

The n8n container needs the Docker socket mounted to use the status/logs/restart tools:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

### Watchdog uses raw HTTP (not Telegram node)

The Self-Watchdog sends alerts via direct Telegram Bot API HTTP calls (not the n8n Telegram node). This is intentional — if n8n is unhealthy, it still needs to be able to fire a Telegram alert without depending on n8n credentials.

---

## State file format

The health monitor reads and writes `/mnt/nas/n8n/homelab-state.json`:
```json
{
  "incidents": {
    "container-name": {
      "status": "down",
      "retries": 2,
      "firstSeen": "2026-02-25T03:00:00.000Z",
      "tier": "critical",
      "composePath": "/home/beanz/homelab/docker/infrastructure/nginx-proxy-manager"
    }
  }
}
```

Use the Chat Agent's `manage_incidents` tool (say "clear incident for sonarr") to reset an incident and let the monitor retry.
