#!/bin/bash
# Pre-migration check script
# Run this BEFORE starting migration. If it fails, DO NOT proceed.

set -e

echo "=== Pre-Migration Check ==="

# Check for staged changes
if ! git diff --cached --quiet; then
    echo "ERROR: Staged changes detected. Commit or unstage them first."
    git diff --cached --name-only
    exit 1
fi

# Check for uncommitted changes
if ! git diff --quiet; then
    echo "ERROR: Uncommitted changes detected. Commit or discard them first."
    git diff --name-only
    exit 1
fi

# Check for untracked files (optional, warn only)
untracked=$(git ls-files --others --exclude-standard)
if [ -n "$untracked" ]; then
    echo "WARNING: Untracked files detected:"
    echo "$untracked"
    echo "Consider adding them to .gitignore or committing them."
fi

# Fetch latest from remote
git fetch origin

# Check if branch is behind remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
    echo "ERROR: No upstream branch configured."
    exit 1
fi

if [ "$LOCAL" != "$REMOTE" ]; then
    BEHIND=$(git rev-list --count HEAD..@{u})
    AHEAD=$(git rev-list --count @{u}..HEAD)

    if [ "$BEHIND" -gt 0 ]; then
        echo "ERROR: Branch is $BEHIND commits behind remote. Pull first."
        exit 1
    fi

    if [ "$AHEAD" -gt 0 ]; then
        echo "ERROR: Branch is $AHEAD commits ahead of remote. Push first."
        exit 1
    fi
fi

echo "=== Repository is clean and synced. Ready for migration. ==="
