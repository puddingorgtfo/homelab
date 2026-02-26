# Infrastructure

Core networking, access, and management services. These run first — most other services
depend on NPM for proxying and Pi-hole for DNS.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [Nginx Proxy Manager](nginx-proxy-manager/) | Reverse proxy with automatic SSL via Let's Encrypt | 80, 81 (admin), 443 |
| [Pi-hole](pihole/) | Network-wide DNS server and ad blocker | 53 (DNS), 8081 (web UI) |
| [Portainer](portainer/) | Docker container management web UI | 9443 |
| [Cloudflare Tunnel](cloudflared/) | Exposes services externally without opening router ports | — |
| [Tailscale](tailscale/) | VPN mesh for remote access from any device | — |
| [Homepage](homepage/) | Customisable service dashboard | 3000 |
| [Uptime Kuma](uptime-kuma/) | Service uptime monitoring with alerting | 3001 |
| [Speedtest Tracker](speedtest-tracker/) | Scheduled internet speed tests with history graphs | 80 |

## Dependencies

```
Internet → Cloudflare Tunnel → NPM → internal services
LAN      → Pi-hole DNS        → NPM → internal services
Remote   → Tailscale VPN      → direct container access
```

Pi-hole handles local DNS resolution. Internal subdomains (e.g. `service.home.lan`) resolve
to the NPM container IP, which then proxies the request to the correct backend service.

If Pi-hole goes down, local DNS breaks. Most services will still be reachable by IP but
browser-based access via subdomains will fail.
