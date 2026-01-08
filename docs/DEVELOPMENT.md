# pykit3 Package Development Guide

This guide documents how to create and publish new pykit3 packages.

## Package Structure

```
k3example/
├── .github/
│   └── workflows/
│       ├── python-package.yml    # CI: test, lint, doc build
│       └── python-publish.yml    # PyPI publish on tag push
├── _building/
│   ├── common.mk                 # Make targets
│   └── README.md
├── docs/
│   └── index.md                  # MkDocs documentation
├── test/
│   ├── __init__.py
│   └── test_example.py
├── .gitignore
├── .readthedocs.yaml
├── __init__.py                   # Package exports + __version__
├── example.py                    # Implementation modules
├── LICENSE
├── Makefile
├── mkdocs.yml
├── pyproject.toml
└── README.md
```

## Required Files

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "k3example"
version = "0.1.0"
description = "Short description of the package"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
authors = [
    { name = "Zhang Yanpo", email = "drdr.xp@gmail.com" }
]
keywords = ["keyword1", "keyword2"]
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
    # Runtime dependencies
]

[project.urls]
Homepage = "https://github.com/pykit3/k3example"
Documentation = "https://k3example.readthedocs.io"

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
packages = ["k3example"]

[tool.setuptools.package-dir]
k3example = "."

[tool.ruff]
line-length = 120
```

### __init__.py

```python
"""
Short description of the package.
"""

from importlib.metadata import version

__version__ = version("k3example")

from .example import (
    ExampleClass,
    example_function,
)

__all__ = [
    "ExampleClass",
    "example_function",
]
```

### Makefile

```makefile
include _building/common.mk
```

### _building/common.mk

```makefile
all: test lint readme doc

.PHONY: test lint cov

test:
	env UT_DEBUG=0 pytest -v

cov:
	coverage run --source=. -m pytest
	coverage html
	open htmlcov/index.html

doc:
	mkdocs build

lint:
	uvx ruff format .
	uvx ruff check --fix .

readme:
	pk3 readme

release:
	pk3 tag

publish:
	pk3 publish

install:
	pip install -e .
```

### mkdocs.yml

```yaml
site_name: k3example
site_description: Short description of the package
site_url: https://k3example.readthedocs.io
repo_url: https://github.com/pykit3/k3example
repo_name: pykit3/k3example

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
```

### .readthedocs.yaml

```yaml
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
```

### docs/index.md

```markdown
# k3example

[![Action-CI](https://github.com/pykit3/k3example/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3example/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3example/badge/?version=stable)](https://k3example.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3example)](https://pypi.org/project/k3example)

Short description of the package.

k3example is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Installation

```bash
pip install k3example
```

## Quick Start

... (add examples)

## API Reference

::: k3example

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
```

## GitHub CI Workflows

### .github/workflows/python-package.yml

Unit tests, linting, and doc build on every push/PR:

```yaml
name: Unit test

on:
  push:
  pull_request:

jobs:
  ut:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest]
        python-version: [3.9, "3.10", 3.11, 3.12]

    steps:
    - uses: actions/checkout@v5
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
        pip install -e .
    - name: Test with pytest
      run: |
        pytest -v

  build_doc:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest]
        python-version: ["3.12"]

    steps:
    - uses: actions/checkout@v5
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Test building doc
      run: |
        pip install -e .
        pip install mkdocs mkdocs-material "mkdocstrings[python]"
        mkdocs build

  lint:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest]
        python-version: ["3.12"]

    steps:
    - uses: actions/checkout@v5
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - name: Lint with ruff
      run: |
        pip install ruff
        ruff check .
        ruff format --check .
```

### .github/workflows/python-publish.yml

Auto-publish to PyPI when a version tag is pushed:

```yaml
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
          TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
        run: twine upload dist/*
```

**Note**: The repository must have `PYPI_PASSWORD` secret configured with a PyPI API token.

## Development Workflow

### Setup

```bash
# Clone the repository
git clone git@github.com:pykit3/k3example.git
cd k3example

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Common Commands

```bash
make test      # Run tests
make lint      # Format and lint code
make doc       # Build documentation
make readme    # Generate README.md
make cov       # Run tests with coverage
```

### CI Branch Workflow

Use the `ci` branch to validate changes before merging to master:

```bash
# 1. Develop and commit locally
git add .
git commit -m "feat: your feature description"

# 2. Push to ci branch to trigger CI
git push origin master:ci -f

# 3. Monitor CI status
gh run list --branch ci --limit 5
gh run watch <run-id> --exit-status

# 4. Once CI passes, push to master
git push origin master
```

This workflow ensures:
- All tests pass on multiple Python versions (3.9-3.12)
- Linting and type checking pass
- Documentation builds successfully
- Changes are validated before reaching master

### Testing

Tests go in the `test/` directory:

```python
# test/test_example.py
import unittest
import k3example

class TestExample(unittest.TestCase):
    def test_function(self):
        result = k3example.example_function()
        self.assertEqual(expected, result)
```

Run tests:

```bash
pytest -v
# or
make test
```

### Linting

Format and check code with ruff:

```bash
uvx ruff format .       # Format code
uvx ruff check --fix .  # Lint and auto-fix
# or
make lint
```

## Release Workflow

### 1. Bump Version

Edit `pyproject.toml`:

```toml
version = "0.1.1"  # Increment version
```

### 2. Commit and Tag

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.1.1"
git tag v0.1.1
```

### 3. Push

```bash
git push && git push origin v0.1.1
```

Pushing the tag triggers the `python-publish.yml` workflow which:
1. Builds the package with `python -m build`
2. Uploads to PyPI with `twine upload`

### Using pk3 CLI

The `pk3` CLI simplifies the release process:

```bash
pip install pk3

# Bump version, commit, and create tag
pk3 tag

# Publish to PyPI (manual alternative to GitHub Actions)
pk3 publish
```

## Conventions

### Naming

- Package names start with `k3` (e.g., `k3example`)
- Module files use snake_case (e.g., `my_module.py`)

### Version

- Version is defined in `pyproject.toml` (single source of truth)
- Read at runtime via `importlib.metadata.version()`
- Use semantic versioning: `MAJOR.MINOR.PATCH`

### Python Support

- Minimum Python version: 3.9
- Test against: 3.9, 3.10, 3.11, 3.12

### Code Style

- Line length: 120 characters
- Formatter: ruff (Black-compatible)
- Linter: ruff

### Documentation

- MkDocs with Material theme
- mkdocstrings for API docs from docstrings
- Hosted on ReadTheDocs
