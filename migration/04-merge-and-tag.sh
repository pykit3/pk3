#!/bin/bash
# Merge migration PR and create version tag
# Usage: ./04-merge-and-tag.sh [package_dir]

set -e

PKG_DIR="${1:-.}"
cd "$PKG_DIR"

# Get current branch
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "migration" ]]; then
    echo "Error: Must be on 'migration' branch, currently on '$BRANCH'"
    exit 1
fi

# Get PR number for current branch
PR_URL=$(gh pr view --json url -q '.url' 2>/dev/null || true)
if [[ -z "$PR_URL" ]]; then
    echo "Error: No PR found for current branch"
    exit 1
fi

echo "PR: $PR_URL"
echo "Opening in browser..."
open "$PR_URL"

echo ""
echo "Waiting for CI checks to complete..."
echo "(Initial empty status is ignored)"

while true; do
    # Get check status: total count and success count
    STATUS=$(gh pr checks --json name,state 2>/dev/null || echo "[]")

    TOTAL=$(echo "$STATUS" | jq 'length')
    PASSED=$(echo "$STATUS" | jq '[.[] | select(.state == "SUCCESS" or .state == "SKIPPED")] | length')
    PENDING=$(echo "$STATUS" | jq '[.[] | select(.state == "PENDING" or .state == "QUEUED" or .state == "IN_PROGRESS")] | length')
    FAILED=$(echo "$STATUS" | jq '[.[] | select(.state == "FAILURE" or .state == "ERROR")] | length')

    if [[ "$TOTAL" -eq 0 ]]; then
        echo -ne "\rWaiting for CI to start...                    "
        sleep 5
        continue
    fi

    if [[ "$FAILED" -gt 0 ]]; then
        echo -e "\n\nCI failed! Check the PR page for details."
        exit 1
    fi

    if [[ "$PENDING" -gt 0 ]]; then
        echo -ne "\rCI running: $PASSED/$TOTAL passed, $PENDING pending...    "
        sleep 10
        continue
    fi

    if [[ "$PASSED" -eq "$TOTAL" ]]; then
        echo -e "\n\nAll $TOTAL CI checks passed!"
        break
    fi

    sleep 5
done

echo ""
echo "Merging to master..."
git checkout master
git pull origin master
git merge --ff-only migration
git push origin master

echo ""
echo "Bumping version..."
# Extract current version and bump patch
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
MINOR=$(echo "$CURRENT_VERSION" | cut -d. -f2)
PATCH=$(echo "$CURRENT_VERSION" | cut -d. -f3)
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

echo "  $CURRENT_VERSION -> $NEW_VERSION"
sed -i.bak "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml && rm -f pyproject.toml.bak

git add pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"
git push origin master

echo ""
echo "Creating version tag..."
pk3 tag
git push origin --tags

PACKAGE_NAME=$(basename "$(pwd)")
PYPI_URL="https://pypi.org/project/$PACKAGE_NAME"
echo ""
echo "Opening PyPI page: $PYPI_URL"
open "$PYPI_URL"

echo ""
echo "Done! Migration complete. Version $NEW_VERSION deployed to PyPI."
