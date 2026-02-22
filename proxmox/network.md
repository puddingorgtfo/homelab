# Network Configuration

## Network Layout

| VLAN ID | Purpose | Subnet | Notes |
|---------|---------|--------|-------|
| 1 | Management | YOUR_MGMT_SUBNET/24 | Proxmox host, infrastructure |
| 10 | Services | YOUR_SERVICES_SUBNET/24 | VMs, Docker services |
| 20 | IoT | YOUR_IOT_SUBNET/24 | Smart home devices |

## NFS Shares

The following NFS shares are available:

* /mnt/nas/media - Media library for Plex
* /mnt/nas/backups - VM backups
* /mnt/nas/docker-configs - Docker configuration files

## Storage Access

All critical services access the NAS storage via the NFS mounts.