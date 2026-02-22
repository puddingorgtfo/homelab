# Network Configuration

## Network Layout

| VLAN ID | Purpose | Subnet | Notes |
|---------|---------|--------|-------|
| 1 | Management | 192.168.1.0/24 | Proxmox host, infrastructure |
| 10 | Services | 192.168.10.0/24 | VMs, Docker services |
| 20 | IoT | 192.168.20.0/24 | Smart home devices |

## NFS Shares

The following NFS shares are available:

* /mnt/nas/media - Media library for Plex
* /mnt/nas/backups - VM backups
* /mnt/nas/docker-configs - Docker configuration files

## Storage Access

All critical services access the NAS storage via the NFS mounts. The original NVMe storage paths
have been migrated to the NAS for reliability and redundancy.