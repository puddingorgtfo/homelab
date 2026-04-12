# Storage Configuration

## Physical Disks (Proxmox Host)

| Device | Size | Type | Role |
|--------|------|------|------|
| sda | 232GB | SSD | Proxmox host OS boot disk |
| nvme0n1 | 4TB | NVMe | VM storage pool (`nvme-data`) |

### 232GB SSD — Proxmox Boot

```
sda (232GB SSD)
├── sda1 (1MB)     — BIOS boot
├── sda2 (1GB)     — EFI System Partition (/boot/efi)
└── sda3 (231GB)   — LVM
    ├── pve-swap (8GB)
    ├── pve-root (68GB)  → Proxmox OS /
    └── pve-data (137GB) → LVM-thin pool (local-lvm)
        └── vm-104-disk-0 (8GB) — Tailscale LXC
```

### 4TB NVMe — VM Storage Pool (`nvme-data`)

LVM-thin pool across the full 4TB NVMe. Approximate allocations:

| Allocation | Size | VM | Purpose |
|-----------|------|----|---------|
| vm-100-disk-0 | 270GB | VM 100 | Ubuntu boot disk (migrated from local-lvm, Mar 2026) |
| vm-100-disk-1 | 1TB | VM 100 | Data disk → `/mnt/nvme` inside VM |
| vm-110-disk-0 | 32GB | VM 110 | TrueNAS OS disk |
| vm-110-disk-1 | ~1MB | VM 110 | TrueNAS EFI disk |
| (unallocated) | ~2.7TB | — | Available for future VMs/backups |

> VM 100's boot disk was migrated to `nvme-data` after the Jan 2026 power surge destroyed
> the original 3.6TB NVMe. The 4TB NVMe was installed as a replacement. The `local-lvm`
> pool on the 232GB SSD now only hosts the Tailscale LXC disk.

---

## Proxmox Storage Pools

| Name | Type | Location | Size | Purpose |
|------|------|----------|------|---------|
| local | Directory | 232GB SSD | 68GB | ISOs, snippets, VM backups |
| local-lvm | LVM-thin | 232GB SSD | 137GB | CT boot disks (Tailscale only) |
| nvme-data | LVM-thin | 4TB NVMe | 4TB | VM boot + data disks |
| qnap-nfs | NFS | QNAP NAS | ~26TB | Shared media, backups, ISOs |

---

## VM Disk Assignments

| VM | Boot Disk | Data Disk | Notes |
|----|-----------|-----------|-------|
| 100 (main-ubuntu) | nvme-data: 270GB | nvme-data: 1TB | Boot migrated from local-lvm Mar 2026 |
| 101 (windows11) | lost (disk failure) | — | Stopped |
| 102 (cachyos) | lost (disk failure) | — | Stopped |
| 103 (windows) | lost (disk failure) | — | Stopped |
| 104 (tailscale) | local-lvm: 8GB | — | LXC |
| 110 (truenas) | nvme-data: 32GB | — | PERC H710 PCIe passthrough for drives |

---

## VM 100 Storage (Inside the VM)

| Device | Size | UUID | Mount | Used For |
|--------|------|------|-------|----------|
| /dev/sda2 | 270GB | 2d6d985f-951e-4b8a-b680-6f95a4cb2885 | `/` | OS, Docker configs |
| /dev/sdb | 1TB | 67173c60-aa3b-4f47-a97b-e9936a795ae8 | `/mnt/nvme` | n8n data, content media |

**NFS Mounts on VM 100:**

| Source | Mount | Used For |
|--------|-------|----------|
| 192.168.0.13:/Jesse | /mnt/nas | QNAP NAS (Docker volumes, media) |
| 192.168.0.28:/mnt/tank | /mnt/truenas | TrueNAS tank pool |
| 192.168.0.28:/mnt/storage/data | /mnt/truenas_storage | TrueNAS storage pool |

---

## NFS Mount (QNAP NAS)

The QNAP NAS provides ~26TB of storage via NFS, used for:
- Media library (movies, TV shows, music, audiobooks)
- VM backups and ISOs
- Proxmox shared storage pool (`qnap-nfs`)
- Mounted on VM 100 at `/mnt/nas` for Docker containers

---

## History

| Date | Event |
|------|-------|
| Jan 2026 | Power surge killed original 3.6TB NVMe (UUID f92a1abd-…). VM 100 data migrated to QNAP NAS. |
| Mar 2026 | 4TB NVMe installed. `nvme-data` LVM-thin pool created. VM 100 boot disk migrated from local-lvm (100GB → 270GB on nvme-data). 1TB data disk provisioned as VM 100's /mnt/nvme replacement. |
