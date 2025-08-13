#!/bin/sh

# Source this script in repo directory to use the tmpl repo's git directory.
# Example: `source path/to/astmpl.sh` in `k3git/`
#
# Enables direct pushing changes from repo dir to the tmpl repo.


# ~/xp/vcs/github.com/pykit3/pk3/github.com/pykit3/k3git/
GIT_DIR=../../../tmpl/.git GIT_WORK_TREE=. bash
