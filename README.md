# Homelab Setup

This repository contains configuration files and documentation for my homelab setup.

## Hardware Specifications

- **CPU**: Intel i7-9700K
- **RAM**: 64GB DDR4
- **System disk**: 512GB SSD
- **Data storage**: NAS mounted at `/mnt/nas`

## Architecture

```
Proxmox VE 9.1 (2x Xeon E5-2640 v2, 128GB RAM)
├── VM 100 - Ubuntu 24.04 (Primary Docker host)
│   ├── 40+ Docker containers (see Services below)
│   ├── Nginx Proxy Manager (reverse proxy + SSL)
│   ├── Pi-hole (DNS + ad blocking)
│   ├── Cloudflare Tunnel (external access)
│   ├── GPU passthrough (PCIe)
│   └── NFS mount to QNAP NAS (26TB media storage)
├── VM 101 - Windows 11 (UEFI + TPM, stopped - disk lost)
├── VM 102 - CachyOS (stopped - disk lost)
├── VM 103 - Windows (stopped - disk lost)
├── CT 104 - Tailscale Bridge (LXC, always-on)
└── Storage: 232GB SSD boot + 26TB NAS
```

**Note:** The 3.6TB NVMe died in a power surge (Jan 2026). VMs 101-103 had boot disks on it and are unrecoverable without reinstall. All Docker configs were recovered and migrated to NAS.

## Services

Various services running on the homelab, including:

- Media: Plex, Jellyfin, Sonarr, Radarr, etc.
- Infrastructure: Nginx Proxy Manager, Pi-hole, Portainer
- Photos: Immich
- Productivity: Nextcloud, Paperless-NGX, Vaultwarden
- And more...

## Security Best Practices

This repository is designed with security in mind. Here are some key practices to follow:

### Environment Variables
- Never commit `.env` files to this repository
- Use the provided `.env.example` files as templates
- Copy `.env.example` to `.env` and fill in your values
- Consider using a password manager to generate strong passwords

### Sensitive Information
- This repository uses environment variables for all sensitive data
- Avoid hardcoding IP addresses, credentials, or API keys in Docker compose files
- Use the .gitignore file to prevent accidentally committing sensitive files

### Recommended Setup
1. Initialize your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```
2. For each service, check for a service-specific .env.example:
   ```bash
   # For example with vaultwarden:
   cp docker/productivity/vaultwarden/.env.example docker/productivity/vaultwarden/.env
   # Edit with your values
   ```
3. Start services with Docker Compose:
   ```bash
   cd docker/service-folder
   docker-compose up -d
   ```

### Updates and Maintenance
- When updating services, check for any new environment variables
- Regularly review docker-compose files for hardcoded values
- Keep your .env files backed up securely outside of git