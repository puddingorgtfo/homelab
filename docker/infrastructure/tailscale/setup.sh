#!/bin/bash
# Tailscale setup for homelab server
# Run this script: bash /path/to/setup.sh
# You'll need to authenticate via a URL printed at the end.

set -e

echo "=== Step 1: Installing Tailscale ==="
curl -fsSL https://tailscale.com/install.sh | sh

echo ""
echo "=== Step 2: Enabling IP forwarding (persisted) ==="
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

echo ""
echo "=== Step 3: Configuring UFW to allow Tailscale ==="
sudo ufw allow in on tailscale0
sudo ufw allow 41641/udp comment 'Tailscale'

echo ""
echo "=== Step 4: Starting Tailscale with subnet routing ==="
echo ""
echo ">>> OPEN THE URL BELOW IN YOUR BROWSER TO AUTHENTICATE <<<"
echo ""
sudo tailscale up \
  --advertise-routes=YOUR_LAN_SUBNET/24 \
  --accept-dns=false \
  --hostname=YOUR_HOSTNAME

echo ""
echo "=== After authenticating in the browser ==="
echo "1. Go to https://login.tailscale.com/admin/machines"
echo "2. Find your machine and click the '...' menu"
echo "3. Click 'Edit route settings' and ENABLE the subnet route"
echo "4. (Optional) Disable key expiry for a server that should always be accessible"
echo ""
echo "=== Verify with ==="
echo "  tailscale status"
echo "  tailscale ip"
