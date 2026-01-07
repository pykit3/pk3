#!/bin/bash
# Step 2: Create template files
# Usage: ./02-create-templates.sh [package_directory]

set -e

PACKAGE_DIR="${1:-.}"
cd "$PACKAGE_DIR"
PACKAGE_NAME="$(basename "$(pwd)")"

echo "=== Step 2: Create template files ==="

# Create pyproject.toml template if not exists
if [ ! -f "pyproject.toml" ]; then
    echo "  Creating: pyproject.toml (EDIT REQUIRED)"
    cat > pyproject.toml << 'PYPROJECT_EOF'
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "PACKAGE_NAME"
version = "0.1.0"
description = "DESCRIPTION"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    { name = "Zhang Yanpo", email = "drdr.xp@gmail.com" }
]
keywords = ["KEYWORD1", "KEYWORD2"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    # Add dependencies here
]

[project.urls]
Homepage = "https://github.com/pykit3/PACKAGE_NAME"
Documentation = "https://PACKAGE_NAME.readthedocs.io"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff",
    "coverage",
]
publish = [
    "build",
    "twine",
    "pk3",
]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.24",
]

[tool.setuptools]
packages = ["PACKAGE_NAME"]

[tool.setuptools.package-dir]
PACKAGE_NAME = "."

[tool.ruff]
line-length = 120
PYPROJECT_EOF
    # Replace PACKAGE_NAME placeholder
    sed -i.bak "s/PACKAGE_NAME/$PACKAGE_NAME/g" pyproject.toml && rm -f pyproject.toml.bak
else
    echo "  Skipped: pyproject.toml (already exists)"
fi

# Create mkdocs.yml template if not exists
if [ ! -f "mkdocs.yml" ]; then
    echo "  Creating: mkdocs.yml (EDIT REQUIRED)"
    cat > mkdocs.yml << MKDOCS_EOF
site_name: $PACKAGE_NAME
site_description: DESCRIPTION
site_url: https://$PACKAGE_NAME.readthedocs.io
repo_url: https://github.com/pykit3/$PACKAGE_NAME
repo_name: pykit3/$PACKAGE_NAME

theme:
  name: material
  palette:
    primary: blue
    accent: blue

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [.]
          options:
            show_source: true
            show_root_heading: true
            heading_level: 2

nav:
  - Home: index.md

markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
MKDOCS_EOF
else
    echo "  Skipped: mkdocs.yml (already exists)"
fi

# Create .readthedocs.yaml if not exists
if [ ! -f ".readthedocs.yaml" ]; then
    echo "  Creating: .readthedocs.yaml"
    cat > .readthedocs.yaml << 'RTD_EOF'
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

mkdocs:
  configuration: mkdocs.yml

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
RTD_EOF
else
    echo "  Skipped: .readthedocs.yaml (already exists)"
fi

# Create docs/index.md template if not exists
mkdir -p docs
if [ ! -f "docs/index.md" ]; then
    echo "  Creating: docs/index.md (EDIT REQUIRED)"
    cat > docs/index.md << DOCS_EOF
# $PACKAGE_NAME

[![Action-CI](https://github.com/pykit3/$PACKAGE_NAME/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/$PACKAGE_NAME/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/$PACKAGE_NAME/badge/?version=stable)](https://$PACKAGE_NAME.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/$PACKAGE_NAME)](https://pypi.org/project/$PACKAGE_NAME)

DESCRIPTION

$PACKAGE_NAME is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Installation

\`\`\`bash
pip install $PACKAGE_NAME
\`\`\`

## Quick Start

... (add examples)

## API Reference

::: $PACKAGE_NAME

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
DOCS_EOF
else
    echo "  Skipped: docs/index.md (already exists)"
fi

# Add site/ to .gitignore if not present
if ! grep -q "^site/$" .gitignore 2>/dev/null; then
    echo "  Adding: site/ to .gitignore"
    echo "site/" >> .gitignore
else
    echo "  Skipped: site/ already in .gitignore"
fi

# Update .github/workflows/python-publish.yml
PUBLISH_YML=".github/workflows/python-publish.yml"
if [ -f "$PUBLISH_YML" ]; then
    echo "  Updating: $PUBLISH_YML"
    cat > "$PUBLISH_YML" << PUBLISH_EOF
name: Upload Python Package

on:
  push:
    tags:
      - v*

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: \${{ secrets.PYPI_PASSWORD }}
        run: twine upload dist/*
PUBLISH_EOF
else
    echo "  Skipped: $PUBLISH_YML (not found)"
fi

echo "=== Step 2 completed ==="
