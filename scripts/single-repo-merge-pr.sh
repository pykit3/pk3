#!/bin/sh

set -o errexit

usage()
{
    echo "Fetch, merge branch and push the default branch"
    echo "$0 <remote-branch>"
}

branch="$1"
shift

git fetch
default_branch=$(git ls-remote --symref origin HEAD | awk '/^ref:/ {sub("refs/heads/", "", $2); print $2}')
[ -n "$default_branch" ] || { echo "no default branch found on origin" >&2; exit 1; }
git checkout "$default_branch"

if git rev-parse $branch; then
    git merge --ff-only $branch
    git push origin "$default_branch"
else 
    echo "no branch $branch"
fi

