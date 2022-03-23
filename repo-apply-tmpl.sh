#!/bin/sh

set -o errexit
git fetch
git merge --ff-only
../../../applytmpl.sh
{ git  status --short | grep "."; } || { echo all clean; exit 0; }

git add -u .
git add ./_building
git ci -m 'deps: apply tmpl'
{ git  status --short | grep "."; } && { echo not clean; exit 1; }
git push

