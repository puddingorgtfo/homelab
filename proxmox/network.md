# Network Configuration

## Proxmox Host Network

```
# /etc/network/interfaces

auto lo
iface lo inet loopback

# Four physical NICs available
iface nic0 inet manual
iface nic1 inet manual
iface nic2 inet manual
iface nic3 inet manual

# Main bridge - VLAN aware
auto vmbr0
iface vmbr0 inet dhcp
    bridge-ports nic0
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094
```

## Network Layout

```
Internet
  │
  ├── Router/Gateway (YOUR_ROUTER_IP)
  │     │
  │     ├── Proxmox Host (DHCP on vmbr0)
  │     │     ├── VM 100 - main-ubuntu-desktop (Docker host)
  │     │     │     ├── Pi-hole (DNS: port 53)
  │     │     │     ├── Nginx Proxy Manager (ports 80, 81, 443)
  │     │     │     ├── Cloudflare Tunnel (external access)
  │     │     │     └── 35+ other containers
  │     │     ├── CT 104 - tailscale-bridge (remote access)
  │     │     └── VMs 101-103 (stopped, on-demand)
  │     │
  │     └── QNAP NAS (NFS server)
  │           └── Mounted at /mnt/nas on VM 100
```

## Key Ports

| Port | Service | Access |
|------|---------|--------|
| 53 | Pi-hole DNS | LAN only |
| 80/443 | Nginx Proxy Manager | LAN + Cloudflare Tunnel |
| 81 | NPM Admin UI | LAN only |
| 8006 | Proxmox Web UI | LAN only |
| 9443 | Portainer | LAN only |
