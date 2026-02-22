# Proxmox Setup

## Hardware

| Component | Specification | Notes |
|-----------|---------------|-------|
| CPU | AMD Ryzen 9 5900X | 12 cores, 24 threads |
| Memory | 128GB DDR4 | ECC RAM |
| System Disk | 1TB SSD | RAID 1 |
| Data Disk | 2TB SSD | For VM storage (replacing failed NVMe) |
| NAS Storage | 26TB | NFS mount for media and backups |

## Installation
Standard Proxmox VE 7 installation.

## Storage Migration
After the NVMe failure in January 2026, storage was restructured:
- Primary VM storage now uses the local SSD
- Media and large data storage uses the NAS
- Docker volumes and configurations now on NAS