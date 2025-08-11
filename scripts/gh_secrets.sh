#!/usr/bin/env bash
# Usage: ./scripts/gh_secrets.sh lanoic tsembwog
set -euo pipefail
OWNER="${1:-}"
REPO="${2:-}"
if [[ -z "$OWNER" || -z "$REPO" ]]; then
  echo "Usage: $0 <github-owner> <repo>"; exit 1
fi

# Frontend (Netlify) secrets
gh secret set NETLIFY_AUTH_TOKEN --repos "$OWNER/$REPO"
gh secret set NETLIFY_SITE_ID --repos "$OWNER/$REPO"
gh secret set REACT_APP_API_URL --repos "$OWNER/$REPO"
gh secret set REACT_APP_SOCKET_URL --repos "$OWNER/$REPO"
gh secret set REACT_APP_MAILCHIMP_URL --repos "$OWNER/$REPO"

# Backend (Docker Hub & Render build hook)
gh secret set DOCKERHUB_USERNAME --repos "$OWNER/$REPO"
gh secret set DOCKERHUB_TOKEN --repos "$OWNER/$REPO"
gh secret set RENDER_DEPLOY_HOOK --repos "$OWNER/$REPO"

echo "GitHub secrets placeholders created. Use 'gh secret set ... --body "value"' to set actual values."
