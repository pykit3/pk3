#!/bin/sh

set -o errexit

git fetch
git merge --ff-only
cp ../../../tmpl/.github/workflows/python-package.yml ./.github/workflows/
{ git  status --short | grep "."; } || { echo all clean; exit 0; }

git add -u .
git add ./_building
git ci -m 'apply tmpl: ci: split ut into 3: ut, lint and doc'
{ git  status --short | grep "."; } && { echo not clean; exit 1; }
git push

