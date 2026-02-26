# Tools

Developer utilities and workflow automation.

## Services

| Service | Description | Port |
|---------|-------------|------|
| [n8n](n8n/) | Visual workflow automation | 5678 |
| [Stirling PDF](stirling-pdf/) | PDF manipulation — merge, split, convert, OCR | 8080 |
| [IT Tools](it-tools/) | 100+ developer utilities in a browser — UUID, base64, JWT, hashing, etc. | 80 |
| [FlareSolverr](flaresolverr/) | Proxy server that bypasses Cloudflare challenges (used by Prowlarr) | 8191 |
| [Dumbpad](dumbpad/) | Minimal shared notepad — no login, just a URL and a text box | 3000 |

## Notes

- **n8n** is also where the homelab automation system lives — see
  [docker/automation/n8n/README.md](../automation/n8n/README.md) for full documentation
  of the monitoring workflows and Telegram chat bot.
- **FlareSolverr** isn't accessed directly by users — it's configured in Prowlarr as a
  proxy for indexers that use Cloudflare protection.
- **Stirling PDF** has no authentication by default (`DOCKER_ENABLE_SECURITY=false`).
  Either add auth or keep it behind NPM access control if you don't want it public-facing.
