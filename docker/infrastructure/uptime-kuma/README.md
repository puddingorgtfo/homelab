# Uptime Kuma

Uptime monitoring with a clean web UI. Checks HTTP endpoints, TCP ports, DNS, Docker
containers, and more. Sends alerts when things go down.

## Ports

| Port | Purpose |
|------|---------|
| 3001 | Web UI |

## Notes

- No config file needed — everything is configured through the web UI and stored in the
  data volume.
- Supports alerts via Telegram, email, Slack, Discord, webhooks, and many more.
- The n8n automation system (`docker/automation/n8n/`) handles auto-remediation; Uptime
  Kuma is a useful complementary alert layer for real-time notification between the
  5-minute n8n check cycles.
- **Official docs**: https://github.com/louislam/uptime-kuma/wiki
