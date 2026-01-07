# Migration Guide: setup.py to pyproject.toml

This guide documents the migration from the old `setup.py` + Sphinx build system to `pyproject.toml` + MkDocs.

## Overview

| Before | After |
|--------|-------|
| `setup.py` | `pyproject.toml` |
| Sphinx (RST) | MkDocs (Markdown) |
| `flake8` | `ruff` |
| `unittest` | `pytest` |
| `_building/build_setup.py` | `pk3 tag` |
| `_building/publish.sh` | `pk3 publish` |
| `_building/build_readme.py` | `pk3 readme` |

## Quick Start

Run the migration scripts in order from this directory:

```bash
cd /path/to/k3package
MIGRATION=~/xp/vcs/github.com/pykit3/pk3/migration

$MIGRATION/00-pre-check.sh .      # Verify repo is clean and synced
$MIGRATION/01-delete-obsolete.sh . # Delete old build system files
$MIGRATION/02-create-templates.sh . # Create pyproject.toml, mkdocs.yml, etc.
$MIGRATION/03-update-building.sh .  # Update _building/common.mk

# ... complete manual steps in Part 2, verify in Part 3, create PR in Part 4 ...

$MIGRATION/04-merge-and-tag.sh .  # Wait for CI, merge, and tag
```

Each script:
- Takes an optional package directory argument (defaults to current directory)
- Can be run independently for debugging
- Prints what it does for review

## Part 0: Pre-Migration Check (REQUIRED)

**IMPORTANT**: Before starting migration, the repository MUST be clean and synced.

The check verifies:
- No staged changes
- No uncommitted changes
- Branch is synced with remote (not ahead or behind)

Run manually if needed:

```bash
./00-pre-check.sh
```

**If it fails, STOP and resolve the issues first.**

## Part 1: Automated Changes

Scripts `01-delete-obsolete.sh`, `02-create-templates.sh`, and `03-update-building.sh` handle:

**Deletions:**
- `setup.py`, `requirements.txt`, `cov.sh`, `.travis.yml`
- `_building/build_setup.py`, `_building/build_readme.py`, `_building/__init__.py`
- `_building/README.md.j2`, `_building/publish.sh`, `_building/install.sh`
- `_building/Makefile`, `_building/requirements.txt`, `_building/building-requirements.txt`
- `_building/.gitignore`
- `docs/source/`, `docs/Makefile`, `docs/make.bat`

**Creates/Updates:**
- `pyproject.toml` (template)
- `mkdocs.yml` (template)
- `.readthedocs.yaml`
- `docs/index.md` (template)
- `_building/common.mk`
- `_building/README.md`
- `.github/workflows/python-publish.yml` (for PyPI deployment on tag push)

## Part 2: Manual Changes

After running the automated scripts, complete these manual steps:

### 2.1 Edit `pyproject.toml`

Update placeholders:
- `version` - from old `__init__.py`
- `description` - from `.github/settings.yml`
- `keywords` - package-specific
- `dependencies` - from old `requirements.txt`

### 2.2 Edit `mkdocs.yml`

Update:
- `site_description`

### 2.3 Edit `docs/index.md`

Update:
- `DESCRIPTION`
- Add Quick Start examples
- Update API Reference sections (`::: module.Class`)

### 2.4 Update `__init__.py`

Change version from static to dynamic:

```python
# Before:
__version__ = "X.Y.Z"

# After:
from importlib.metadata import version
__version__ = version("PACKAGE_NAME")
```

### 2.5 Update `.github/workflows/python-package.yml`

Key changes:
- Remove Python 3.6 comment block
- Update `actions/setup-python@v2` → `@v5`
- Change `cp setup.py .. && cd .. && python setup.py install` → `pip install -e .`
- Change `flake8` → `ruff`
- Change `make -C docs html` → see below

For doc build step:
```yaml
- name: Test building doc
  run: |
    # Install package first, then docs tools separately to avoid sphinx conflict
    pip install -e .
    pip install mkdocs mkdocs-material "mkdocstrings[python]"
    mkdocs build
```

For lint job - update install and lint steps:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install ruff
    # ... rest unchanged

- name: Lint with ruff
  run: |
    ruff check .
    ruff format --check .
```

### 2.6 Run `ruff format`

Format all Python files:

```bash
uvx ruff format .
```

### 2.7 Update README.md

Remove Travis CI badge if present:

```markdown
# Remove this line:
[![Build Status](https://travis-ci.com/pykit3/PACKAGE_NAME.svg?branch=master)](https://travis-ci.com/pykit3/PACKAGE_NAME)
```

### 2.8 Update `.gitignore`

Add mkdocs build output:

```
site/
```

## Part 3: Verification

After migration, verify:

```bash
# Install package
pip install -e .

# Run tests
make test

# Check lint
make lint

# Build docs
make doc

# Generate README
make readme
```

## Part 4: Create Migration PR

After verification passes, commit all changes and create a PR:

```bash
# Create migration branch
git checkout -b migration

# Add tracked file changes
git add -u

# Add new files individually
git add pyproject.toml
git add mkdocs.yml
git add .readthedocs.yaml
git add docs/index.md
# ... add any other new files

# Commit
git commit -m "chore: migrate from setup.py to pyproject.toml"

# Push to remote
git push -u origin migration

# Create PR for review
gh pr create --title "Migrate to pyproject.toml" --body "Migration from setup.py to pyproject.toml + MkDocs."

```

### Wait for CI, Merge, and Tag

Run the merge script (from the migration branch):

```bash
$MIGRATION/04-merge-and-tag.sh .
```

This script:
1. Opens the PR in browser
2. Waits for CI checks (ignores initial empty status)
3. Merges to master with `--ff-only`
4. Bumps version in `pyproject.toml` (patch version)
5. Commits version bump and pushes to master
6. Creates and pushes version tag via `pk3 tag`
7. Pushing the tag triggers GitHub Actions to deploy to PyPI

## Dependencies

The migration requires the `pk3` package:

```bash
pip install pk3
```

## Notes

- **Dependency conflicts**: Some k3* packages pin old sphinx versions. Install docs tools separately in CI to avoid conflicts.
- **Version source**: Version is now in `pyproject.toml`, read at runtime via `importlib.metadata`.
- **README generation**: `pk3 readme` uses a default template. Custom templates can be specified with `--template`.
