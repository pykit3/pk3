#!/bin/bash
# Step 3: Update _building files
# Usage: ./03-update-building.sh [package_directory]

set -e

PACKAGE_DIR="${1:-.}"
cd "$PACKAGE_DIR"

echo "=== Step 3: Update _building files ==="

# Update _building/common.mk
echo "  Updating: _building/common.mk"
cat > _building/common.mk << 'COMMON_MK_EOF'
all: test lint readme doc

.PHONY: test lint cov
sudo_test:
	sudo env "PATH=$$PATH" UT_DEBUG=0 pytest -v

test:
	env UT_DEBUG=0 pytest -v

cov:
	coverage run --source=. -m pytest
	coverage html
	open htmlcov/index.html

doc:
	mkdocs build

lint:
	# ruff format: fast Python code formatter (Black-compatible)
	uvx ruff format .
	# ruff check: fast Python linter with auto-fixes
	uvx ruff check --fix .

static_check:
	# mypy: static type checker for Python
	uvx mypy . --ignore-missing-imports

readme:
	pk3 readme

release:
	pk3 tag

publish:
	pk3 publish

install:
	pip install -e .
COMMON_MK_EOF

# Update _building/README.md
echo "  Updating: _building/README.md"
cat > _building/README.md << 'BUILDING_README_EOF'
# _building

Shared build configuration for pykit3 packages.

## Commands

All commands use the `pk3` package:

```bash
make test      # Run tests with pytest
make lint      # Format and lint with ruff
make cov       # Generate coverage report
make doc       # Build documentation with mkdocs
make readme    # Generate README.md from docstrings
make release   # Create git tag from version in pyproject.toml
make publish   # Build and upload to PyPI
```

## Release Process

1. Update version in `pyproject.toml`
2. Run `make release` to create git tag
3. Run `git push --tags` to trigger GitHub Actions
4. GitHub Actions automatically publishes to PyPI
BUILDING_README_EOF

echo "=== Step 3 completed ==="
