# Pi-hole

Network-wide DNS server and ad blocker. All devices on the LAN use Pi-hole as their DNS
server (configured via router DHCP). Local subdomains resolve to Nginx Proxy Manager.

## Ports

| Port | Purpose |
|------|---------|
| 53 | DNS (TCP + UDP) |
| 8081 | Web admin UI |

## Configuration

| Variable | Description |
|----------|-------------|
| `PIHOLE_WEBPASSWORD` | Admin UI password |
| `PIHOLE_PORT` | Web UI port (default: 8081) |
| `TZ` | Timezone |

## Notes

- Local DNS records (e.g. `service.home → 192.168.x.x`) are added under
  Local DNS → DNS Records in the admin UI.
- Add NPM's IP as the target for all local subdomains — NPM handles the final routing.
- Blocklists are managed under Group Management → Adlists.
- If Pi-hole goes down, local DNS breaks. Services are still reachable by IP but
  hostname-based access will fail until Pi-hole is back up.
- **Official docs**: https://docs.pi-hole.net/
