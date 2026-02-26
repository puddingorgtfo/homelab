# Nginx Proxy Manager

Reverse proxy with a web GUI. Routes external/internal traffic to backend services and
handles SSL certificate issuance and renewal via Let's Encrypt automatically.

## Ports

| Port | Purpose |
|------|---------|
| 80 | HTTP (redirect to HTTPS) |
| 81 | Admin web UI |
| 443 | HTTPS |

## Configuration

| Variable | Description |
|----------|-------------|
| `NPM_DB_PASSWORD` | MariaDB password for NPM's internal database |
| `NPM_ROOT_PASSWORD` | MariaDB root password |

## Notes

- After first boot, open `:81` to complete initial setup (create admin account).
- All other services in this repo use `expose:` (not `ports:`) and connect via the
  `npm_default` Docker network — NPM proxies them without publishing ports to the host.
- SSL certs are auto-renewed by NPM. Each proxy host can have HTTP/2, WebSockets,
  custom headers, and access lists configured via the UI.
- See [proxy-hosts.md](proxy-hosts.md) for the full list of configured proxy hosts.
- **Official docs**: https://nginxproxymanager.com/guide/
