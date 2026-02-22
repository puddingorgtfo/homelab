# Storage Configuration

## Proxmox Storage Pools

| Name | Type | Size | Used | Purpose |
|------|------|------|------|---------|
| local | Directory | 68GB | 40% | ISOs, snippets, backups |
| local-lvm | LVM-thin | 137GB | 57% | VM/CT boot disks |
| qnap-nfs | NFS | 26TB | 26% | Media, backups, ISOs |

## Physical Disks

```
sda (232GB SSD) - Boot disk
├── sda1 (1MB)     - BIOS boot
├── sda2 (1GB)     - EFI System Partition (/boot/efi)
└── sda3 (231GB)   - LVM
    ├── pve-swap (8GB)
    ├── pve-root (68GB) → /
    └── pve-data (137GB) → LVM-thin pool
        ├── vm-100-disk-0 (100GB) - Main Ubuntu VM boot
        └── vm-104-disk-0 (8GB)   - Tailscale LXC

```

## VM Disk Assignments

| VM | Boot Disk | Data Disk |
|----|-----------|-----------|
| 100 (main-ubuntu) | local-lvm: 100GB | qnap-nfs |
| 101 (windows11) | lost (disk failure) | - |
| 102 (cachyos) | lost (disk failure) | - |
| 103 (windows) | lost (disk failure) | - |
| 104 (tailscale) | local-lvm: 8GB | - |

## NFS Mount (QNAP NAS)

The QNAP NAS provides ~26TB of storage via NFS, used for:
- Media library (movies, TV shows, music, audiobooks)
- VM backups and ISOs
- Proxmox shared storage pool (`qnap-nfs`)
- Mounted on VM 100 at `/mnt/nas` for Docker containers
