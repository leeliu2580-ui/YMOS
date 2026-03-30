#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

git add .
if git diff --cached --quiet; then
  echo "No changes to commit"
else
  git commit -m "workspace backup $(date +%Y-%m-%d)"
fi

git push origin main
echo "BACKUP_OK"
