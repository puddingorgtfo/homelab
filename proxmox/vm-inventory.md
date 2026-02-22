# VM Inventory

| VM ID | Name | Description | Resources | Storage |
|-------|------|-------------|-----------|---------|
| 100   | plex | Media Server | 4 vCPU, 8GB RAM | 20GB (system), 4TB (nas-storage:/media) |
| 101   | nextcloud | File storage | 2 vCPU, 4GB RAM | 20GB (system), 100GB (nas-storage:/data) |
| 102   | pihole | DNS & Ad blocking | 1 vCPU, 1GB RAM | 10GB (ssd-data:/opt) |

## Backup Schedule
All VMs are backed up to NAS storage weekly.
