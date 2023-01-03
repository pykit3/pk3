#!/bin/sh

set -o errexit
git fetch
git merge --ff-only
../../../applytmpl.sh

# git bug: if not running git-status first, git-diff-index report a lot changes.
git status
# check if worktree is clean
git diff-index --quiet HEAD -- && { echo all clean; exit 0; } || { echo "to commit"; }

git add -u .
git add ./_building
git ci -m 'deps: apply tmpl'

git status
# check if worktree is clean
git diff-index --quiet HEAD -- || { echo not clean; exit 1; }
git push

