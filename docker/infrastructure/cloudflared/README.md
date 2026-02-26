# Cloudflare Tunnel (cloudflared)

Exposes selected local services to the internet without opening any ports on your router.
Traffic flows: Internet → Cloudflare edge → encrypted tunnel → this container → NPM → service.

## How It Works

1. You create a tunnel in the Cloudflare Zero Trust dashboard
2. Cloudflare gives you a tunnel token
3. The `cloudflared` container connects outbound to Cloudflare using that token
4. You configure which public hostnames map to which backend services in the dashboard
5. Cloudflare routes HTTPS traffic to your home server via the persistent tunnel

No port forwarding. No dynamic DNS. Your home IP is never exposed.

## Configuration

| Variable | Description |
|----------|-------------|
| `CLOUDFLARED_TUNNEL_TOKEN` | Tunnel token from Cloudflare Zero Trust dashboard |

## Setup

1. Log into [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. Networks → Tunnels → Create a tunnel
3. Copy the token into your `.env` file
4. In the tunnel's Public Hostname settings, add routes like:
   - `service.yourdomain.com` → `http://nginx-proxy-manager:80`
5. NPM handles internal routing from there

## Notes

- Your domain must be managed by Cloudflare (nameservers pointing to Cloudflare) for
  this to work.
- Cloudflare Access policies can be added to require authentication before reaching
  any tunneled service.
- The `/webhook/` path can be excluded from Access auth (needed for n8n webhooks and
  Telegram bot callbacks).
- **Official docs**: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
