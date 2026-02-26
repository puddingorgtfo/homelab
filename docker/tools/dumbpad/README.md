# Dumbpad

Minimal shared notepad. One URL, one text box, persistent. No login, no accounts, no
formatting — just a place to paste things quickly from any device.

## Ports

| Port | Purpose |
|------|---------|
| 3000 | Web UI |

## Notes

- Multiple "pads" can be created by navigating to different paths (e.g. `/mypad`).
- Content is stored in the Docker volume and persists across restarts.
- Useful for quickly sharing text between devices or with others on the local network.
- **Official docs**: https://github.com/dumbwareio/dumbpad
