#!/bin/bash
# starksuit-pre-change-check.sh
# MUST be run before ANY file modifications in the StarkSuit-Project repo.
# Checks remote for new commits; if there are conflicts, aborts immediately.
# Exit 0 = safe to proceed, Exit 1 = collision detected (stop).

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "=== StarkSuit Pre-Change Check ==="
echo "Branch: $(git branch --show-current)"
echo "Remote HEAD: $(git ls-remote origin HEAD | cut -f1)"

# Fetch latest
git fetch origin >/dev/null 2>&1

REMOTE_HEAD=$(git ls-remote origin HEAD | cut -f1)
LOCAL_HEAD=$(git rev-parse HEAD)

if [ "$REMOTE_HEAD" = "$LOCAL_HEAD" ]; then
    echo "✓ Repo is up to date. No remote changes detected."
    echo "=== CHECK PASSED ==="
    exit 0
fi

echo "Remote is ahead by $(git rev-list --count HEAD..origin/main) commit(s)."
echo ""
echo "Attempting rebase..."
if git pull --rebase origin main 2>&1; then
    echo ""
    echo "✓ Rebase succeeded. No conflicts."
    echo "=== CHECK PASSED ==="
    exit 0
else
    echo ""
    echo "✗ COLLISION DETECTED — conflicts during rebase."
    echo "Run 'git status' to see conflict markers, resolve them, then 'git rebase --continue'."
    echo "=== CHECK FAILED ==="
    exit 1
fi
