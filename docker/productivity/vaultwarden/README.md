# Vaultwarden

Lightweight, self-hosted Bitwarden-compatible password manager server. All standard
Bitwarden client apps (browser extension, mobile, desktop) work with it.

## Ports

| Port | Purpose |
|------|---------|
| 8080 | Web vault and API |

## Configuration

| Variable | Description |
|----------|-------------|
| `VAULTWARDEN_ADMIN_TOKEN` | Admin panel password (hashed) — generate with `vaultwarden hash` |
| `VAULTWARDEN_DOMAIN` | Public URL of your Vaultwarden instance (required for WebAuthn/FIDO2) |

## Notes

- **Client apps**: Use any official Bitwarden app. In the app settings, switch the server URL
  from `bitwarden.com` to your Vaultwarden URL.
- Browser extension (Chrome, Firefox, Safari), iOS app, Android app, and desktop apps all work.
- Enable HTTPS (via NPM) before using — browsers require HTTPS for the extension to work.
- Admin panel at `/admin` — requires `VAULTWARDEN_ADMIN_TOKEN` to be set.
- **Official docs**: https://github.com/dani-garcia/vaultwarden/wiki
