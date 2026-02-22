# Homelab Setup

This repository contains configuration files and documentation for my homelab setup.

## Hardware Specifications

- **CPU**: Intel i7-9700K
- **RAM**: 64GB DDR4
- **System disk**: 512GB SSD
- **Data storage**: NAS mounted at `/mnt/nas`

## Services

Various services running on the homelab...

## Security Best Practices

This repository is designed with security in mind. Here are some key practices to follow:

### Environment Variables
- Never commit `.env` files to this repository
- Use the provided `.env.example` files as templates
- Copy `.env.example` to `.env` and fill in your values
- Consider using a password manager to generate strong passwords

### Sensitive Information
- This repository uses environment variables for all sensitive data
- Avoid hardcoding IP addresses, credentials, or API keys in Docker compose files
- Use the .gitignore file to prevent accidentally committing sensitive files

### Recommended Setup
1. Initialize your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```
2. For each service, check for a service-specific .env.example:
   ```bash
   # For example with vaultwarden:
   cp docker/productivity/vaultwarden/.env.example docker/productivity/vaultwarden/.env
   # Edit with your values
   ```
3. Start services with Docker Compose:
   ```bash
   cd docker/service-folder
   docker-compose up -d
   ```

### Updates and Maintenance
- When updating services, check for any new environment variables
- Regularly review docker-compose files for hardcoded values
- Keep your .env files backed up securely outside of git