#!/bin/sh

set -o errexit

usage()
{
    echo "Fetch, cherry-pick branch and push master"
    echo "$0 <remote-branch>"
}

branch="$1"
shift

git fetch
git co master

if git rev-parse $branch; then
    git cherry-pick $branch
    git push origin master
else 
    echo "no branch $branch"
fi

