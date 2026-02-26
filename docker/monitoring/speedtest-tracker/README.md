# Speedtest Tracker

Runs scheduled internet speed tests using Ookla Speedtest and logs the results.
Shows graphs of download speed, upload speed, and ping over time.

## Ports

| Port | Purpose |
|------|---------|
| 80 | Web UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `APP_KEY` | Laravel app encryption key — generate with `echo "base64:$(openssl rand -base64 32)"` |
| `TZ` | Timezone |

## Notes

- Test schedule is configurable in the UI (default is hourly).
- Results are stored in SQLite.
- Useful for spotting ISP throttling or confirming degraded performance during reported outages.
- **Official docs**: https://docs.speedtest-tracker.dev/
