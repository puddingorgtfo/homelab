#!/bin/bash
# n8n host-level watchdog — runs every minute via cron
# Belt-and-suspenders: runs independently of n8n itself
# Sends Telegram via raw curl if n8n container is not running
#
# SETUP:
#   1. Copy this file to /home/<user>/scripts/n8n-watchdog.sh
#   2. Set credentials either via environment variables in your crontab:
#        TELEGRAM_BOT_TOKEN=<your_bot_token> TELEGRAM_CHAT_ID=<your_chat_id> /path/to/script
#      Or export them in /etc/environment or ~/.profile
#   3. Update N8N_COMPOSE_PATH if your compose file lives elsewhere
#   4. Install cron entry:
#        (crontab -l 2>/dev/null; echo "* * * * * /home/<user>/scripts/n8n-watchdog.sh") | crontab -

BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"
COMPOSE="${N8N_COMPOSE_PATH:-/home/beanz/homelab/docker/automation/n8n/compose.yml}"
LOG="/var/log/n8n-watchdog.log"
LOCK="/tmp/n8n-watchdog.lock"

# Prevent concurrent runs
[ -f "$LOCK" ] && exit 0
touch "$LOCK"
trap "rm -f $LOCK" EXIT

send_telegram() {
  curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}&text=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1")" \
    >> "$LOG" 2>&1
}

if ! docker ps --format '{{.Names}}' | grep -q '^n8n$'; then
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] n8n container not running — attempting restart" >> "$LOG"
  docker compose -f "$COMPOSE" restart >> "$LOG" 2>&1

  sleep 20

  if docker ps --format '{{.Names}}' | grep -q '^n8n$'; then
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] n8n restarted successfully by host cron" >> "$LOG"
    send_telegram "n8n was down — host cron restarted it successfully."
  else
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] n8n STILL DOWN after restart attempt" >> "$LOG"
    send_telegram "n8n STILL DOWN after host cron restart. SSH to your Docker host: docker logs n8n --tail 30"
  fi
fi
