# VM & Container Inventory

## VM 100 - main-ubuntu-desktop (Primary)

The main workhorse VM running Ubuntu 24.04 with all Docker containers.

| Setting | Value |
|---------|-------|
| Status | Running, autostart on boot |
| CPU | 6 cores, host passthrough |
| RAM | 32GB (no ballooning) |
| Machine | q35 |
| Boot Disk | 270GB on nvme-data (virtio-scsi, iothread, discard) — migrated from local-lvm Mar 2026 |
| Data Disk | 1TB on nvme-data → `/mnt/nvme` inside VM (n8n data, content media) |
| Network | virtio on vmbr0 |
| GPU | PCIe passthrough (slot 0000:42:00) |
| Guest Agent | Enabled |
| Hook Script | `local:snippets/vm100-cpupin.sh` (CPU pinning) |

## VM 101 - windows11

Windows 11 VM for occasional use.

| Setting | Value |
|---------|-------|
| Status | Stopped |
| CPU | 8 cores, x86-64-v2-AES |
| RAM | 32GB |
| BIOS | OVMF (UEFI) with Secure Boot |
| Boot Disk | lost (disk failure) |
| EFI Disk | On qnap-nfs |
| TPM | v2.0 |
| Network | virtio on vmbr0, firewall enabled |

## VM 102 - cachyos

CachyOS Linux VM.

| Setting | Value |
|---------|-------|
| Status | Stopped |
| CPU | 8 cores, x86-64-v2-AES |
| RAM | 16GB |
| Boot Disk | lost (disk failure) |
| Network | virtio on vmbr0, firewall enabled |

## VM 103 - windows

Secondary Windows VM.

| Setting | Value |
|---------|-------|
| Status | Stopped |
| CPU | 8 cores, kvm64 |
| RAM | 32GB |
| Boot Disk | lost (disk failure) |
| Network | virtio on vmbr0, firewall enabled |

## VM 105 - main-ubuntu-desktop (Template)

Template/snapshot of VM 100 for backup purposes.

| Setting | Value |
|---------|-------|
| Status | Template |
| CPU | 6 cores, host passthrough |
| RAM | 16GB (4GB balloon) |
| Boot Disk | 100GB on qnap-nfs |
| GPU | PCIe passthrough (slot 0000:42:00) |

## VM 110 - truenas

TrueNAS Scale NAS/storage server with PERC H710 PCIe passthrough.

| Setting | Value |
|---------|-------|
| Status | Running |
| CPU | 4 cores, host type |
| RAM | 16GB |
| Machine | q35 + OVMF (UEFI) |
| OS Disk | 32GB on nvme-data |
| EFI Disk | 128K on nvme-data |
| Network | virtio on vmbr0 — 192.168.0.28 |
| PCIe passthrough | 0000:05:00.0 (PERC H710 Adapter, IOMMU Group 24) |
| OS | TrueNAS SCALE 25.04.2.6 (Fangtooth) |
| Web UI | http://192.168.0.28 |

### PERC H710 Setup
- `megaraid_sas` blacklisted on Proxmox host; PERC bound to `vfio-pci`
- IOMMU enabled: `intel_iommu=on iommu=pt` in GRUB
- Single-disk RAID-0 VD created via `storcli` before TrueNAS could see the drive

### ZFS Pool
| Setting | Value |
|---------|-------|
| Pool | tank |
| Mount | /mnt/tank |
| Topology | Single disk stripe |
| Drive | WD 6TB Red (WDC WD60EFAX-68JH4N0) — Bay 0 |
| Usable | 5.46 TB |

> Note: Single-disk stripe has no redundancy. Add second drive for mirror/RAIDZ when available.

---

## CT 104 - tailscale-bridge (LXC)

Lightweight LXC container running Tailscale for remote access.

| Setting | Value |
|---------|-------|
| Status | Running, autostart on boot |
| CPU | 1 core |
| RAM | 512MB |
| Swap | 512MB |
| Root Disk | 8GB on local-lvm |
| Network | Static IP on vmbr0 |
| OS | Ubuntu |
| Special | TUN device passthrough for VPN |
