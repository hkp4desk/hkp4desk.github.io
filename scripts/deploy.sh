#!/usr/bin/env bash
# HKP4 deploy: publish dist/ to gh-pages as a SINGLE commit (force push).
# Past rendered versions never accumulate in the Pages branch history.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f dist/index.html ]; then
  echo "dist/index.html not found — run 'astro build' first" >&2
  exit 1
fi

REPO_URL="$(git remote get-url origin)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git -C "$TMP" init -q -b gh-pages
git -C "$TMP" config user.name "$(git config user.name || echo HKP4-Deploy)"
git -C "$TMP" config user.email "$(git config user.email || echo deploy@localhost)"
cp -R dist/. "$TMP"/
touch "$TMP/.nojekyll"
git -C "$TMP" add -A
git -C "$TMP" commit -q -m "deploy $(git rev-parse --short HEAD)"
git -C "$TMP" push -f "$REPO_URL" gh-pages:gh-pages
echo "Published (single-commit gh-pages)"
