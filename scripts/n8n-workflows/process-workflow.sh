#!/bin/bash

# Usage: ./process-workflow.sh <workflow_id> <repo_name> <workflow_title>

WORKFLOW_ID=$1
REPO_NAME=$2
WORKFLOW_TITLE=$3
API_KEY="<YOUR_N8N_API_KEY>"

echo "Processing workflow: $WORKFLOW_TITLE"

# Export workflow
curl -s -X GET "https://<YOUR_N8N_DOMAIN>/api/v1/workflows/$WORKFLOW_ID" \
  -H "X-N8N-API-KEY: $API_KEY" | jq . > ${REPO_NAME}.json

# Security scan
echo "=== Security Scan ===" > ${REPO_NAME}-scan.txt
echo "Checking for sensitive data..." >> ${REPO_NAME}-scan.txt
grep -i "apikey\|api_key\|apiSecret\|password" ${REPO_NAME}.json >> ${REPO_NAME}-scan.txt 2>&1 || echo "No API keys found" >> ${REPO_NAME}-scan.txt
grep "eyJ" ${REPO_NAME}.json >> ${REPO_NAME}-scan.txt 2>&1 || echo "No JWT tokens found" >> ${REPO_NAME}-scan.txt
grep -o "[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}" ${REPO_NAME}.json | sort -u >> ${REPO_NAME}-scan.txt 2>&1 || echo "No emails found" >> ${REPO_NAME}-scan.txt

# Sanitize email addresses
sed -i 's/your-old-email@example.com/your-email@example.com/g' ${REPO_NAME}.json
sed -i 's/<YOUR_NAME>/Your Name/g' ${REPO_NAME}.json

# Create repo structure
mkdir -p ${REPO_NAME}/docs
mv ${REPO_NAME}.json ${REPO_NAME}/workflow.json

echo "Workflow exported and sanitized: ${REPO_NAME}"
