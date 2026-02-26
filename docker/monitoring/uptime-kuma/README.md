# Uptime Kuma

Uptime monitoring with a clean web UI. Checks HTTP endpoints, TCP ports, DNS records,
Docker containers, and more on a configurable schedule. Sends alerts when things go down.

## Ports

| Port | Purpose |
|------|---------|
| 3001 | Web UI |

## Notes

- Configured entirely through the web UI — no config files needed.
- Alert channels: Telegram, email, Slack, Discord, ntfy, webhooks, and many more.
- Supports status page publishing (public or password-protected).
- Monitors can check response content as well as just connectivity.
- Works well alongside the n8n automation system — Uptime Kuma provides real-time alerting
  while n8n handles auto-remediation.
- **Official docs**: https://github.com/louislam/uptime-kuma/wiki
