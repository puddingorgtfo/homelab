# VM & Container Inventory

## VM 100 - main-ubuntu-desktop (Primary)

The main workhorse VM running Ubuntu 24.04 with all Docker containers.

| Setting | Value |
|---------|-------|
| Status | Running, autostart on boot |
| CPU | 6 cores, host passthrough |
| RAM | 32GB (no ballooning) |
| Machine | q35 |
| Boot Disk | 100GB on local-lvm (virtio-scsi, iothread, discard) |
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
