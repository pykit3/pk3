#!/bin/bash
set -e

# Publish Python package to PyPI
# Usage: TWINE_PASSWORD=pypi-xxx ./publish.sh [test]
#
# Sub-repos can reuse this script by symlinking:
#   ln -s ../../pk3/scripts/dev-publish-to-pypi.sh ./publish.sh

if [ -z "$TWINE_PASSWORD" ]; then
    echo "Error: TWINE_PASSWORD not set"
    echo "Usage: TWINE_PASSWORD=pypi-xxx $0 [test]"
    exit 1
fi

if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found in current directory"
    exit 1
fi

export TWINE_USERNAME="__token__"
rm -rf dist/ build/ *.egg-info src/*.egg-info

python -m build

if [ "$1" = "test" ]; then
    twine upload --repository testpypi dist/*
else
    twine upload dist/*
fi
