#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="research-agent-toolkit"
OWNER="linshuijin6"
VISIBILITY="public"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI is required. Install from https://cli.github.com/"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Please run: gh auth login"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init
fi

git add .
git commit -m "Initial v1.0.0 literature monitor" || true

if ! gh repo view "${OWNER}/${REPO_NAME}" >/dev/null 2>&1; then
  gh repo create "${OWNER}/${REPO_NAME}" --${VISIBILITY} --source=. --remote=origin --push --description "AI-powered literature monitoring toolkit for researchers"
else
  git remote remove origin 2>/dev/null || true
  git remote add origin "https://github.com/${OWNER}/${REPO_NAME}.git"
  git branch -M main
  git push -u origin main
fi

echo "Done: https://github.com/${OWNER}/${REPO_NAME}"
