# Tailscale

VPN mesh network for secure remote access. Every device with Tailscale installed gets a
stable `100.x.x.x` address and can reach other Tailscale devices directly, regardless of
firewalls or NAT.

## Notes

- Tailscale is not run as a Docker container here — it runs as an LXC container on
  Proxmox (CT 104: tailscale-bridge), keeping it isolated from the Docker host but
  always on.
- Once connected via Tailscale, you can reach any service on this host by its Tailscale
  IP address, bypassing Cloudflare Tunnel and NPM entirely.
- Tailscale key auth: add `TS_AUTHKEY` from the Tailscale admin console for headless login.
- **Official docs**: https://tailscale.com/kb/
