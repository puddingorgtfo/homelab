# qBittorrent + Gluetun VPN

Torrent client running inside a Mullvad VPN container. All qBittorrent traffic is routed
through the VPN — if the VPN drops, Gluetun's kill switch cuts internet access entirely,
preventing IP leaks.

## Ports

| Port | Purpose |
|------|---------|
| 8080 | qBittorrent web UI (exposed via Gluetun's port forwarding) |

## How It Works

qBittorrent runs inside Gluetun's network namespace (`network_mode: service:gluetun`).
It has no direct internet access — all traffic is routed through the VPN. Gluetun exposes
the WebUI port to the host, so you can still access the UI at `http://<host>:8080`.

```
Host → Gluetun (VPN) → Mullvad → Internet
          ↑
     qBittorrent (no direct network access)
```

## Configuration

| Variable | Description |
|----------|-------------|
| `VPN_SERVICE_PROVIDER` | VPN provider (e.g. `mullvad`) |
| `VPN_TYPE` | `openvpn` or `wireguard` |
| `OPENVPN_USER` / `OPENVPN_PASSWORD` | VPN credentials |
| `VPN_SERVER_COUNTRIES` | Country to connect to (e.g. `US`) |
| `QBIT_PORT` | Torrent port (6881 by default) |
| `WEBUI_PORT` | qBittorrent WebUI port (8080 by default) |
| `DOWNLOADS_PATH` | Where completed downloads are saved |
| `PUID` / `PGID` | User/group ID for file permissions |
| `TZ` | Timezone |

## Notes

- The default qBittorrent login is `admin` / `adminadmin` — change this immediately on
  first login.
- VPN kill switch is enabled by default (`VPN_FIREWALL=on`). If the VPN can't connect,
  there will be no internet access for qBittorrent.
- Sonarr and Radarr connect to qBittorrent at `http://gluetun:8080` (internal Docker network).
- **Gluetun docs**: https://github.com/qdm12/gluetun/wiki
- **qBittorrent docs**: https://github.com/qbittorrent/qBittorrent/wiki
