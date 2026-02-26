# Monitoring

Service uptime tracking and network performance history.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Uptime Kuma](uptime-kuma/) | Uptime monitor for services with status page and alerting | 3001 |
| [Speedtest Tracker](speedtest-tracker/) | Runs scheduled internet speed tests and graphs the results over time | 80 |

## Notes

- Uptime Kuma can send alerts via Telegram, email, Slack, webhooks, and many other channels.
  Useful as a real-time supplement to the n8n automation system in `docker/automation/n8n/`.
- Speedtest Tracker stores all results in a local SQLite database and shows graphs of
  download speed, upload speed, and ping over time — useful for spotting ISP issues.
