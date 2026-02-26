# Homelab Repository Update Workflow

This document outlines the process for keeping both the public and private repositories in sync
while ensuring sensitive data remains protected.

## Repository Structure

- **Public repository** (`origin`) — sanitized, no credentials, `main` branch
  - `git push origin main`
  - https://github.com/puddingorgtfo/homelab

- **Private repository** (`private`) — full config with encrypted `.env` files, `main` branch
  - Uses git-crypt to encrypt `.env` files at rest
  - https://github.com/puddingorgtfo/homelab-private

Both remotes use `main` as their only branch. The local working tree is always on `main`.

## Update Workflow

### 1. Work on the local `main` branch

```bash
git checkout main
# make your changes
git add <files>
git commit -m "description of changes"
```

### 2. Push to public (origin)

Run a quick safety scan first to confirm no sensitive data is staged:

```bash
git diff HEAD~1 | grep -iE 'password|secret|token|eyJ|192\.168\.|[0-9]{10}:AA'
git push origin main
```

### 3. Push to private

The private remote has a git-crypt encrypted file (`sensitive/linkwarden.env`) that is
corrupted and blocks a normal `git checkout`. Use git plumbing to push without checking out:

```bash
# Fetch current private/main HEAD
git fetch private main
PRIVATE_HEAD=$(cat .git/FETCH_HEAD | awk '{print $1}')

# Build a new tree based on private/main + your changes
export GIT_INDEX_FILE=/tmp/homelab-private-index
git read-tree $PRIVATE_HEAD

# Stage each changed file by its blob SHA (repeat for each file)
git update-index --add --cacheinfo 100644,$(git rev-parse HEAD:path/to/file),path/to/file

NEW_TREE=$(git write-tree)
NEW_COMMIT=$(git commit-tree $NEW_TREE -p $PRIVATE_HEAD -m "your commit message")
git push private $NEW_COMMIT:main

unset GIT_INDEX_FILE && rm -f /tmp/homelab-private-index
```

For multiple changed files at once:
```bash
git diff HEAD~1 --name-only | while read f; do
  MODE=$(git ls-tree HEAD -- "$f" | awk '{print $1}')
  SHA=$(git ls-tree HEAD -- "$f" | awk '{print $3}')
  [ -n "$SHA" ] && git update-index --add --cacheinfo "$MODE,$SHA,$f"
done
```

## Important Guidelines

1. **Never commit actual credentials to the public repository**
2. **Always use `${VARIABLE}` substitution in compose files — never hardcode values**
3. **Use `your-`, `change-me`, or `CHANGE_ME_` prefixes in `.env.example` files**
4. **Double-check before pushing to public:**
   ```bash
   git diff HEAD~1 | grep -iE 'password|secret|token|eyJ|your-real-domain'
   ```
5. **Real credentials live in encrypted `.env` files on the private remote** — not in
   any tracked file on the public remote

## Unlocking git-crypt (private repo)

To read encrypted `.env` files locally:
```bash
git-crypt unlock /home/beanz/homelab-private-git-crypt.key
```

The key is stored at `/home/beanz/homelab-private-git-crypt.key` and backed up in Vaultwarden.

## Useful Commands

```bash
# Confirm no .env files are tracked on public
git ls-files | grep '\.env'

# Scan for sensitive data in staged changes
git diff --cached | grep -iE "password\|secret\|token\|key\|credential"

# Compare what each remote has
git log origin/main..private/main --oneline
git log private/main..origin/main --oneline
```
