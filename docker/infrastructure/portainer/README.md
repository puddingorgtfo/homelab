# Portainer

Web UI for managing Docker containers, images, volumes, networks, and stacks. Useful for
quick container restarts, log viewing, and environment inspection without SSH.

## Ports

| Port | Purpose |
|------|---------|
| 9443 | HTTPS web UI |

## Notes

- First boot creates an admin account — do this quickly (there's a 5-minute timeout).
- Portainer can manage multiple Docker environments. The local environment (this host) is
  connected via the Docker socket mount.
- Stacks in Portainer correspond to docker compose projects. You can deploy, update, and
  remove stacks from the UI.
- For production changes (modifying compose files), prefer editing files in this repo
  and running `docker compose up -d` — keeps everything in version control.
- **Official docs**: https://docs.portainer.io/
