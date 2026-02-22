# Storage Configuration

| Name | Type | Path | Content |
|------|------|------|---------|
| local-lvm | LVM | /dev/pve/data | VM disks |
| local | Directory | /var/lib/pve/local | ISO images, containers |
| ssd-data | Directory | /mnt/data | VM disks, backups |
| nas-storage | NFS | /mnt/nas | Media storage, backups |

## Performance
The SSD storage provides good performance for VMs with routine IO operations.
The NAS provides redundant storage for media and larger backups.

## Snapshots
Regular ZFS snapshots are configured for SSD and NAS storage.
