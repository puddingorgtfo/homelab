# Proxmox Host

## Hardware

| Component | Specification |
|-----------|--------------|
| CPU | 2x Intel Xeon E5-2640 v2 @ 2.00GHz (16 cores / 32 threads) |
| RAM | 128GB DDR3 ECC |
| Boot Disk | 232GB SSD (Proxmox OS: 68GB root + 8GB swap + 137GB LVM-thin for CTs) |
| NVMe | 4TB NVMe (`nvme-data` LVM-thin pool — VM boot + data disks) |
| NAS | QNAP NFS share (~26TB, `qnap-nfs` pool) |
| GPU | PCIe passthrough to VM 100 (slot `0000:42:00`) |

## Software

- **Proxmox VE**: 9.1.4
- **Kernel**: 6.17.4-2-pve
- **QEMU/KVM**: 10.1.2

## Network

Single bridge (`vmbr0`) with DHCP, VLAN-aware (VIDs 2-4094). Four physical NICs available (nic0-nic3), nic0 bridged.

See [network.md](network.md) for full interface config.

## VMs & Containers

| VMID | Name | Type | Status | Resources |
|------|------|------|--------|-----------|
| 100 | main-ubuntu-desktop | KVM | Running | 6 cores, 32GB RAM, 270GB boot + 1TB data (nvme-data) |
| 101 | windows11 | KVM | Stopped | 8 cores, 32GB RAM, 500GB |
| 102 | cachyos | KVM | Stopped | 8 cores, 16GB RAM, 499GB |
| 103 | windows | KVM | Stopped | 8 cores, 32GB RAM, 500GB |
| 104 | tailscale-bridge | LXC | Running | 1 core, 512MB RAM, 8GB |
| 105 | main-ubuntu-desktop (template) | KVM | Template | 6 cores, 16GB RAM, 100GB |

See [vm-inventory.md](vm-inventory.md) for detailed VM configurations.
