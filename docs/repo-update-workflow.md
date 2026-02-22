# Homelab Repository Update Workflow

This document outlines the process for safely updating both private and public versions of the homelab repository, ensuring sensitive data remains protected.

## Repository Structure

- **Private Repository**: `homelab-private` (contains complete data with sensitive information)
  - Uses git-crypt to encrypt sensitive files
  - All sensitive data is stored in actual configuration files or in the `sensitive/` directory

- **Public Repository**: `homelab` (sanitized version)
  - No sensitive data is included
  - Uses environment variables for all sensitive information
  - No git-crypt is used

## Update Workflow

### 1. Make Changes to Private Repository

```bash
# Switch to main branch
git checkout main

# Unlock git-crypt if needed
git-crypt unlock /path/to/homelab-private-git-crypt.key

# Make your changes
# For sensitive data:
# - Add directly to compose files using real values, or
# - Store in the sensitive/ directory as separate files
# - Environment variables can reference these files

# Commit changes to private repository
git add .
git commit -m "Description of changes (private version)"
git push private main
```

### 2. Create Sanitized Version for Public Repository

```bash
# Create or switch to public branch
git checkout public
# If public branch doesn't exist: git checkout -b public

# Remove sensitive directory if it exists
git rm -r sensitive/

# Update .gitattributes for public repository
# Make it clear this is the public version without encryption

# Sanitize any files that might contain sensitive information:
# - Replace real domains with example.com
# - Replace passwords/tokens with environment variables
# - Remove any other sensitive information

# Commit sanitized changes
git add .
git commit -m "Description of changes (public version)"

# Push to public repository
git push origin public:main
```

### 3. Important Guidelines

1. **Never commit actual credentials to the public repository**
2. **Always replace sensitive values with environment variables in the public version**
3. **Use descriptive placeholders in .env.example (e.g., CHANGE_ME_SOMETHING)**
4. **Double-check files for sensitive data before pushing to public**
5. **Keep both repositories in sync (same features but different handling of secrets)**

### 4. Useful Commands

```bash
# Check for sensitive information
git grep -i "password\|secret\|token\|key\|credential"
git grep -i "your-actual-domain-name"

# Check file differences between branches
git diff main..public

# Create a .env file from example
cp .env.example .env
# Then edit the .env file with your actual values
```

## Troubleshooting

- If git-crypt key is lost, you'll need to reinitialize git-crypt and recreate encrypted files
- If public repository accidentally includes sensitive data, immediately:
  1. Remove the sensitive data
  2. Force push a new commit
  3. Consider the exposed data compromised (reset passwords, etc.)