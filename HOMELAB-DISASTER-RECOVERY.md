# Homelab Disaster Recovery Guide

**Last Updated:** 2026-02-15
**Critical Information for Complete System Rebuild**

---

## 🚨 Emergency Access

If everything is down and you need to rebuild:

### 1. Critical Files You Need
- **Git-crypt key**: `~/homelab-private-git-crypt.key` (also in Vaultwarden)
- **Private repo**: `https://github.com/<YOUR_GITHUB_USERNAME>/homelab-private`
- **Public repo**: `https://github.com/<YOUR_GITHUB_USERNAME>/homelab`
- **This file**: Keep a copy in Vaultwarden and on a USB drive

### 2. Quick Recovery Steps
```bash
# 1. Clone the private repo
git clone git@github.com:<YOUR_GITHUB_USERNAME>/homelab-private.git
cd homelab-private

# 2. Unlock encrypted files
sudo apt install git-crypt
git-crypt unlock ~/homelab-private-git-crypt.key

# 3. All your compose files and secrets are now readable
ls -R docker/
```

---

## 📋 Complete Infrastructure Inventory

### Proxmox Host
- **Hostname**: beanz-Standard-PC-Q35-ICH9-2009
- **CPU**: 2x Xeon E5-2640 v2
- **RAM**: 128GB
- **Version**: Proxmox VE 9.1

### Primary VM (VM 100 - Ubuntu 24.04)
- **Role**: Docker host for all services
- **OS**: Ubuntu 24.04 LTS
- **Running Containers**: 40+
- **GPU**: PCIe passthrough enabled
- **Storage**:
  - Boot: 232GB SSD
  - NAS: 26TB NFS from <NAS_IP>:/<NAS_EXPORT> mounted at `/mnt/nas`
  - ~~3.6TB NVMe~~ (DEAD - power surge Jan 2026, configs migrated to NAS)

### Network
- **Router/Gateway**: <ROUTER_IP>
- **DNS**: Pi-hole (on Docker host)
- **Reverse Proxy**: Nginx Proxy Manager
- **External Access**: Cloudflare Tunnel
- **VPN**: Tailscale (CT 104 - always-on LXC container)

### NAS (QNAP)
- **IP**: <NAS_IP>
- **Export**: /<NAS_EXPORT>
- **Mount**: /mnt/nas on Docker host
- **Size**: 26TB total, ~6.7TB used
- **Critical Data**:
  - Docker configs: `/mnt/nas/docker-configs/` (migrated from dead NVMe)
  - Immich photos: `/mnt/nas/immich/upload`
  - Media: `/mnt/nas/movies`, `/mnt/nas/Tv Shows`, `/mnt/nas/books`
  - Paperless documents: `/mnt/nas/paperless/`
  - Vaultwarden: `/mnt/nas/vaultwarden/data`
  - Nextcloud data: `/mnt/nas/nextcloud/data`
  - Downloads: `/mnt/nas/downloads`

---

## 🔐 Secrets & Credentials

### Master Passwords
- **Sudo password**: `<YOUR_SUDO_PASSWORD>`
- **Common DB password**: `<YOUR_DB_PASSWORD>`
- **All other secrets**: Encrypted in git-crypt protected .env files

### Git-Crypt Key Locations
1. **Primary**: `/home/beanz/homelab-private-git-crypt.key`
2. **Backup in Vaultwarden**: Search for "homelab git-crypt key"
3. **This file includes a base64-encoded backup** (see bottom of this file)

### GitHub Access
- **Account**: <YOUR_GITHUB_USERNAME>
- **Private repo**: https://github.com/<YOUR_GITHUB_USERNAME>/homelab-private
- **Public repo**: https://github.com/<YOUR_GITHUB_USERNAME>/homelab

### Cloudflare
- **Account email**: your-email@yourdomain.com
- **Domain**: yourdomain.com
- **Tunnel**: Configured for photos.yourdomain.com
- **Zero Trust**: Wildcard Access policy with Immich bypass

### Mullvad VPN
- **Account**: <MULLVAD_ACCOUNT_ID>
- **WireGuard Device**: Rare Fly
- **IP Address**: <WIREGUARD_IP>
- **Endpoint**: <VPN_ENDPOINT>

---

## 🐳 All Running Services (40+ containers)

### Infrastructure (8)
| Service | Port | Domain |
|---------|------|--------|
| Nginx Proxy Manager | 81 | npm.yourdomain.com |
| Pi-hole | 8081 | pihole.yourdomain.com |
| Portainer | 9443 | portainer.yourdomain.com |
| Cloudflare Tunnel | - | - |
| Homepage | 3000 | home.yourdomain.com |
| Gluetun VPN | - | - |
| Uptime Kuma | 3001 | status.yourdomain.com |
| Speedtest Tracker | 80 | speedtest.yourdomain.com |

### Media (11)
| Service | Port | Domain |
|---------|------|--------|
| Plex | 32400 | plex.yourdomain.com |
| Jellyfin | 8096 | jellyfin.yourdomain.com |
| Sonarr | 8989 | sonarr.yourdomain.com |
| Radarr | 7878 | radarr.yourdomain.com |
| Prowlarr | 9696 | prowlarr.yourdomain.com |
| Seerr | 5055 | oversee.yourdomain.com |
| qBittorrent | 8080 | qbit.yourdomain.com |
| Audiobookshelf | 13378 | audiobooks.yourdomain.com |
| Calibre | 3000-3001 | calibre.yourdomain.com |
| Readarr | 8787 | readarr.yourdomain.com |
| FlareSolverr | 8191 | - |

### Photos (1)
| Service | Port | Domain |
|---------|------|--------|
| Immich | 2283 | photos.yourdomain.com |

### Productivity (6)
| Service | Port | Domain |
|---------|------|--------|
| Nextcloud | 443 | cloud.yourdomain.com |
| Paperless-NGX | 8010 | paperless.yourdomain.com |
| Vaultwarden | 8080 | vault.yourdomain.com |
| WordPress | 8088 | wordpress.yourdomain.com |
| Stirling PDF | 8080 | pdf.yourdomain.com |
| IT-Tools | 80 | tools.yourdomain.com |

### Smart Home (3)
| Service | Port | Domain |
|---------|------|--------|
| Home Assistant | 8123 | homeassistant.yourdomain.com |
| Zigbee2MQTT | 8080 | zigbee.yourdomain.com |
| Mosquitto | 1883 | - |

### Search (1)
| Service | Port | Domain |
|---------|------|--------|
| SearXNG | 8082 | searxng.yourdomain.com |

### Tools (1)
| Service | Port | Domain |
|---------|------|--------|
| Dumbpad | 3000 | dumbpad.yourdomain.com |

### Gaming (1)
| Service | Port | Domain |
|---------|------|--------|
| RomM | - | - |

---

## 🔧 Critical System Configs

### NFS Mount (/etc/fstab)
```
<NAS_IP>:/<NAS_EXPORT> /mnt/nas nfs defaults,_netdev 0 0
```

### Docker Networks
- `npm_default` - Shared network for NPM and services
- Individual bridge networks per stack

### System Users
- **Main user**: beanz
- **UID/GID**: 1000:1000 (used by most containers)

---

## 📝 Rebuild Procedure

### From Scratch (Proxmox Failed)
1. Install Proxmox VE 9.1
2. Create Ubuntu 24.04 VM (VM 100)
3. Install Docker: `curl -fsSL https://get.docker.com | sh`
4. Install git-crypt: `sudo apt install git-crypt`
5. Clone private repo and unlock
6. Mount NAS: Add fstab entry and `mount -a`
7. Create local config dirs: `mkdir -p /opt/homeassistant/config /docker/homepage/config`
8. Deploy all stacks from `docker/` directories via Portainer or `docker compose up -d`

### From VM Backup (VM intact, data lost)
1. Clone homelab-private repo
2. Unlock with git-crypt key
3. Redeploy all stacks
4. Restore data from NAS (still intact)

### From VM Failure (Hardware OK)
1. Restore VM from Proxmox backup
2. Verify NFS mount: `df -h /mnt/nas`
3. Restart containers: `docker compose up -d` in each stack directory

---

## ✅ Regular Maintenance

### Weekly
- [ ] Check Proxmox backup status
- [ ] Verify NAS capacity: `df -h /mnt/nas`
- [ ] Check gluetun VPN connection: `docker logs gluetun --tail 20`

### Monthly
- [ ] Test git-crypt unlock on a different machine
- [ ] Update this disaster recovery doc
- [ ] Verify all 38 containers are running: `docker ps`
- [ ] Check for Docker image updates in Portainer

### Quarterly
- [ ] Export full Portainer stack configs
- [ ] Test complete recovery from private repo
- [ ] Update compose files in repo if changes were made in Portainer

---

## 🆘 Common Recovery Scenarios

### "I lost the git-crypt key"
- Check Vaultwarden (search "homelab git-crypt")
- Check USB backup drive
- Check base64-encoded backup at bottom of this file

### "Cloudflare Access is blocking my service"
- Log into Cloudflare Zero Trust
- Check Access > Applications
- Verify bypass rules for specific subdomains

### "Gluetun VPN won't connect"
- Check Mullvad account is active: https://mullvad.net/en/account
- Verify WireGuard keys haven't expired
- Download new config if needed from account page
- Update .env file with new private key

### "Immich mobile app can't connect"
- Verify photos.yourdomain.com resolves
- Check Cloudflare Access bypass is in place
- Verify `IMMICH_PUBLIC_URL=https://photos.yourdomain.com` in compose

### "NAS mount is gone"
- Check NAS is online: `ping <NAS_IP>`
- Remount: `sudo mount -a`
- Check fstab entry is correct
- Restart affected containers after mount: `docker restart immich-immich-server-1`

---

## 📦 Backup Strategy

### What's Backed Up
- ✅ **All compose files** → homelab-private repo
- ✅ **All secrets** → Encrypted .env files in repo
- ✅ **System configs** → homelab-private/system/
- ✅ **NPM proxy configs** → homelab-private/docker/infrastructure/nginx-proxy-manager/proxy-hosts/
- ✅ **Home Assistant config** → homelab-private/configs/homeassistant/
- ✅ **Critical data** → NAS (/mnt/nas) - Immich photos, Paperless docs, Vaultwarden vault

### What's NOT Backed Up (Rebuilds from config)
- Docker volumes (NPM Let's Encrypt certs, Nextcloud data, WordPress, Jellyfin metadata)
- Plex metadata (large, rebuilds automatically)
- Application caches

---

## 🔑 Git-Crypt Key Backup (Base64-Encoded)

**To restore:**
```bash
# Decode and save the key
echo "<base64-string-below>" | base64 -d > ~/homelab-private-git-crypt.key
chmod 600 ~/homelab-private-git-crypt.key
```

**Base64-encoded key:**
```
