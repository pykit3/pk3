#!/bin/sh

# Source this script in a _building directory to use the tmpl repo's git directory.
# Example: `source path/to/astmpl.sh` in `k3git/_building`
#
# Enables direct pushing changes from _building dir to the tmpl repo.


GIT_DIR=../tmpl/.git GIT_WORK_TREE=. bash
