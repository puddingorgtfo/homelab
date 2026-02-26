# n8n

Visual workflow automation. Build workflows that connect APIs, run scheduled tasks,
process data, and trigger actions — without writing a full application.

## Ports

| Port | Purpose |
|------|---------|
| 5678 | Web UI and webhook endpoint |

## Homelab Automation System

This repo includes a full homelab monitoring, auto-remediation, and Telegram chat bot
system built on n8n. See the dedicated documentation in
[docker/automation/n8n/README.md](../../automation/n8n/README.md) for:

- How the monitoring workflows work
- What the Telegram bot can do (with example conversations)
- Setup requirements and configuration

## Configuration

| Variable | Description |
|----------|-------------|
| `N8N_PORT` | Port to listen on (default: 5678) |
| `N8N_HOST` | Hostname n8n binds to |
| `N8N_PROTOCOL` | `http` or `https` |
| `N8N_DATA_DIR` | Persistent data directory |
| `N8N_API_KEY` | API key for programmatic access |
| `WEBHOOK_URL` | Public-facing URL for webhooks |
| `TZ` | Timezone |

## Notes

- `NODE_FUNCTION_ALLOW_BUILTIN=*` enables all Node.js built-in modules (http, fs, etc.)
  in Code nodes — required for the automation workflows.
- `NODE_FUNCTION_ALLOW_EXTERNAL=node-ssh` enables the SSH library for container management.
- The Docker socket mount (`/var/run/docker.sock`) allows workflows to interact with Docker.
- **Official docs**: https://docs.n8n.io/
