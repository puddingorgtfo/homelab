# Git-Crypt Usage Guide

This repository uses **git-crypt** to encrypt sensitive files (passwords, tokens, API keys).

## What's Encrypted

All files matching these patterns are automatically encrypted:
- `**/.env` - Environment variable files containing secrets
- `**/.env.*` - Any .env variant files
- `secrets/**` - Anything in the secrets directory
- `docker/infrastructure/cloudflared/config.yml` - Contains Cloudflare tunnel credentials

## Symmetric Key Location

The encryption key is stored at:
```
~/homelab-private-git-crypt.key
```

**IMPORTANT:** Back this up to:
- Password manager (Bitwarden/Vaultwarden)
- USB drive
- Encrypted cloud storage

Without this key, you cannot decrypt the repository on a new machine.

## Unlocking on a New Machine

When you clone this repo on a fresh system, the encrypted files will appear as binary garbage. To decrypt:

```bash
# Install git-crypt
sudo apt install git-crypt

# Clone the repo
git clone git@github.com:<YOUR_GITHUB_USERNAME>/homelab-private.git
cd homelab-private

# Unlock with the key
git-crypt unlock ~/homelab-private-git-crypt.key

# Verify decryption worked
cat docker/infrastructure/nginx-proxy-manager/.env
# Should show plaintext passwords, not binary
```

## Checking Encryption Status

To see which files are encrypted:
```bash
git-crypt status
```

Files marked `encrypted:` are protected.

## Adding New Secrets

When adding new passwords/tokens to the repo:

1. Create a `.env` file in the service directory:
   ```bash
   cd docker/your-service/
   nano .env
   ```

2. Add your secrets:
   ```
   DB_PASSWORD=your_password_here
   API_KEY=your_key_here
   ```

3. The `.gitattributes` file will automatically encrypt any `.env` file when you commit.

4. Update the `compose.yml` to reference the .env file:
   ```yaml
   services:
     app:
       env_file: .env
       environment:
         # Use ${VAR} syntax to reference .env variables
         DB_PASSWORD: ${DB_PASSWORD}
   ```

## Verifying Encryption on GitHub

After pushing, visit GitHub and view a `.env` file. It should show binary/encrypted content, not plaintext.

## Current Status

Currently encrypted files:
- `docker/infrastructure/nginx-proxy-manager/.env` (MySQL passwords)

## TODO: Extract More Secrets

The following services still have plaintext secrets in compose files that need to be extracted to `.env`:

- [ ] pihole - WEBPASSWORD
- [ ] cloudflared - tunnel token (already encrypted via .gitattributes rule)
- [ ] immich - DB password
- [ ] paperless-ngx - DB password, admin password, secret key
- [ ] vaultwarden - admin token
- [ ] nextcloud - DB password
- [ ] wordpress - DB passwords
- [ ] qbittorrent/gluetun - WireGuard private key
- [ ] plex - PLEX_CLAIM token
- [ ] romm - DB passwords

To complete the migration, create `.env` files for each service above and update their compose files to use `env_file: .env`.
