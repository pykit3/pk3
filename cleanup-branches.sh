#!/bin/bash
# Remove unused branches (merged or gone) from all k3* repos
# - Prunes remote tracking refs
# - Removes local branches merged to master/main
# - Removes remote branches merged to master/main

set -e

REPOS_DIR="github.com/pykit3"
DRY_RUN="${1:-}"

cd "$(dirname "$0")"

if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "=== DRY RUN MODE ==="
    echo ""
fi

for repo in "$REPOS_DIR"/k3*; do
    [ -d "$repo/.git" ] || continue

    name=$(basename "$repo")
    echo "[$name]"
    cd "$repo"

    # Determine default branch
    default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "master")

    # Fetch and prune stale remote refs
    git fetch --prune 2>/dev/null || true

    # Remove local branches that are gone on remote
    gone_branches=$(git branch -vv 2>/dev/null | grep ': gone]' | awk '{print $1}' || true)
    for branch in $gone_branches; do
        echo "  local (gone): $branch"
        [ "$DRY_RUN" = "--dry-run" ] || git branch -D "$branch" 2>/dev/null || true
    done

    # Remove local branches merged to default branch
    merged_local=$(git branch --merged "$default_branch" 2>/dev/null | grep -v "^\*" | grep -v "$default_branch" | xargs || true)
    for branch in $merged_local; do
        echo "  local (merged): $branch"
        [ "$DRY_RUN" = "--dry-run" ] || git branch -d "$branch" 2>/dev/null || true
    done

    # Remove remote branches merged to default branch (excluding HEAD and default)
    merged_remote=$(git branch -r --merged "origin/$default_branch" 2>/dev/null | grep -v "HEAD" | grep -v "origin/$default_branch" | sed 's@origin/@@' | xargs || true)
    for branch in $merged_remote; do
        echo "  remote (merged): $branch"
        [ "$DRY_RUN" = "--dry-run" ] || git push origin --delete "$branch" 2>/dev/null || true
    done

    cd - > /dev/null
done

echo ""
echo "Done!"
