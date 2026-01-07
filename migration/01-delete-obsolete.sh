#!/bin/bash
# Step 1: Delete obsolete files
# Usage: ./01-delete-obsolete.sh [package_directory]

set -e

PACKAGE_DIR="${1:-.}"
cd "$PACKAGE_DIR"

echo "=== Step 1: Delete obsolete files ==="

# Old build system files
for f in setup.py requirements.txt cov.sh .travis.yml; do
    if [ -f "$f" ]; then
        echo "  Removing: $f"
        rm -f "$f"
    fi
done

# Old _building files
for f in _building/build_setup.py \
         _building/build_readme.py \
         _building/__init__.py \
         _building/README.md.j2 \
         _building/publish.sh \
         _building/install.sh \
         _building/Makefile \
         _building/requirements.txt \
         _building/building-requirements.txt \
         _building/.gitignore; do
    if [ -f "$f" ]; then
        echo "  Removing: $f"
        rm -f "$f"
    fi
done

# Old Sphinx docs
if [ -d "docs/source" ]; then
    echo "  Removing: docs/source/"
    rm -rf docs/source/
fi
for f in docs/Makefile docs/make.bat; do
    if [ -f "$f" ]; then
        echo "  Removing: $f"
        rm -f "$f"
    fi
done

echo "=== Step 1 completed ==="
