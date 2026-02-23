#!/bin/bash

# Script to push all n8n workflows to GitHub
# Run this after authenticating with: gh auth login

echo "===== Pushing n8n Workflows to GitHub ====="
echo ""

# List of workflows to push
workflows=(
  "ai-message-router"
  "claude-cli-telegram"
  "conversation-memory-service"
  "gmail-auto-response-agent"
  "ocr-workflow"
  "ocr-workflow-v2"
)

# Check gh auth
echo "Checking GitHub authentication..."
if ! gh auth status 2>&1 | grep -q "Logged in"; then
  echo "ERROR: Not authenticated with GitHub"
  echo "Please run: gh auth login"
  exit 1
fi

echo "✓ GitHub authentication OK"
echo ""

# Push each workflow
for workflow in "${workflows[@]}"; do
  echo "Processing: $workflow"
  cd "/home/beanz/n8n-workflows/$workflow" || continue

  # Create GitHub repo
  echo "  Creating GitHub repository..."
  if gh repo create "<YOUR_GITHUB_USERNAME>/$workflow" --public --source=. --remote=origin 2>&1; then
    echo "  ✓ Repository created"
  else
    echo "  ! Repository might already exist, trying to push..."
  fi

  # Rename branch to main
  git branch -M main

  # Push to GitHub
  echo "  Pushing to GitHub..."
  if git push -u origin main 2>&1; then
    echo "  ✓ Pushed to GitHub: https://github.com/<YOUR_GITHUB_USERNAME>/$workflow"
  else
    echo "  ✗ Failed to push $workflow"
  fi

  echo ""
done

echo "===== Complete ====="
echo "All workflows processed. Check the output above for any errors."
echo ""
echo "Repositories created:"
for workflow in "${workflows[@]}"; do
  echo "  - https://github.com/<YOUR_GITHUB_USERNAME>/$workflow"
done
