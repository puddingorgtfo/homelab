# Scripts

Shell scripts and exported n8n workflow configurations.

## n8n-watchdog.sh

Host-level watchdog for the n8n container. Runs every minute via cron, independently of
n8n itself — the belt-and-suspenders safety net.

**What it does:**
1. Checks if the `n8n` Docker container is running
2. If not, runs `docker compose restart`
3. Waits 20 seconds, then re-checks
4. Sends a Telegram alert whether the restart succeeded or failed

**Install:**
```bash
chmod +x scripts/n8n-watchdog.sh

# Edit the script to set your credentials (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID),
# or export them in your shell/cron environment.

# Add to crontab:
(crontab -l 2>/dev/null; echo "* * * * * TELEGRAM_BOT_TOKEN=<your-token> TELEGRAM_CHAT_ID=<your-chat-id> /home/user/homelab/scripts/n8n-watchdog.sh") | crontab -
```

**Log file:** `/var/log/n8n-watchdog.log`

See [docker/automation/n8n/README.md](../docker/automation/n8n/README.md) for full documentation
of the complete monitoring system.

---

## n8n-workflows/

Exported n8n workflow JSON files with documentation. These are snapshots of the n8n
workflows and can be imported directly into n8n via Settings → Import from File.

See [n8n-workflows/SUMMARY.md](n8n-workflows/SUMMARY.md) for the full list and setup instructions.
