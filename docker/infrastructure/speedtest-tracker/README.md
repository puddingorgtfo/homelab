# Speedtest Tracker

Runs scheduled internet speed tests using Ookla Speedtest and stores the results. Shows
graphs of download speed, upload speed, and ping over time.

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

- Tests run automatically on a schedule (configurable in the UI — default is hourly).
- Results stored in SQLite database in the config volume.
- Useful for spotting ISP throttling patterns or confirming speeds during outages.
- **Official docs**: https://docs.speedtest-tracker.dev/
