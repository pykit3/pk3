# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

`pk3` is a workspace metarepo for the **pykit3** collection — a set of Python 3 utility modules. Each module lives as an independent git repo under `packages/k3*`. The root repo contains:

- **`pk3/`** — A CLI tool (`pk3 version|tag|publish|readme`) used by all sub-packages for build operations
- **`packages/k3*/`** — Individual pykit3 modules (each with its own git repo)
- **`packages/tmpl/`** — Template for creating new modules (placeholder: `k3xxnamexx`)
- **`scripts/`** — Workspace management scripts (naming convention: `multi-repo-*`, `single-repo-*`, `workspace-*`, `dev-*`)

All modules share `_building/common.mk` which delegates to the `pk3` CLI. The Makefile in each module is just `include _building/common.mk`.

## Common Development Commands

### Working on a Module
```bash
cd packages/k3color

make test          # pytest -v
make lint          # ruff format + ruff check --fix (via uvx)
make doc           # mkdocs build
make cov           # coverage run + html report
make static_check  # mypy
make install       # pip install -e .
make readme        # pk3 readme (auto-generated, do not hand-edit)
```

### Testing
```bash
# Run all tests for a module
cd packages/k3color && make test

# Run a single test file
cd packages/k3color && pytest test/test_color.py -v

# Run a single test method
cd packages/k3color && pytest test/test_color.py::TestColor::test_method -v

# Tests requiring root
cd packages/k3color && make sudo_test
```

### Release Workflow
```bash
cd packages/k3color
# 1. Bump version in pyproject.toml
# 2. Create git tag
make release       # runs: pk3 tag (creates vX.Y.Z tag from pyproject.toml)
git push --tags    # triggers GitHub Actions → PyPI publish
```

### Cross-Repository Operations
```bash
# Execute a script across all packages/k3* repos
./scripts/multi-repo-exec.sh <script_name> <args...>

# Clone all pykit3 packages
./scripts/multi-repo-clone-all.sh

# Create a new package from template
./scripts/dev-create-package.sh packages k3newmodule
```

### Workspace-Level
```bash
make readme        # Regenerate root README.md (fetches repo list via gh CLI)
```

## Module Structure

Every k3* module follows this layout:
```
k3modulename/
├── _building/common.mk    # Shared Makefile targets (test, lint, doc, release, etc.)
├── test/
│   ├── test_modulename.py # Tests using unittest.TestCase, run via pytest
│   └── test_doctest.py    # Doctest loader for module docstrings
├── __init__.py            # Exports + version via importlib.metadata
├── modulename.py          # Implementation
├── pyproject.toml         # Package metadata, version (single source of truth)
├── Makefile               # Just: include _building/common.mk
└── mkdocs.yml             # Documentation config
```

### Version Management
- Version is defined in `pyproject.toml` (single source of truth)
- `__init__.py` reads it at runtime: `__version__ = version("k3modulename")` via `importlib.metadata`
- `make release` → `pk3 tag` creates a git tag from the pyproject.toml version

### Module `__init__.py` Pattern
```python
from .impl_module import Foo, bar, baz
from importlib.metadata import version

__version__ = version("k3modulename")
__all__ = ["Foo", "bar", "baz"]
```

## Tooling

- **Testing**: `pytest` (tests use `unittest.TestCase` but are discovered/run by pytest)
- **Linting**: `ruff` via `uvx` (line-length: 120)
- **Documentation**: `mkdocs` with mkdocs-material theme
- **Type checking**: `mypy` via `uvx`
- **CI**: Reusable GitHub Actions workflows in `.github/workflows/` (matrix: Python 3.9–3.12)
- **Publishing**: `twine` upload triggered by pushing version tags
- **Workspace CLI**: `pk3` (installed from root pyproject.toml, provides `version|tag|publish|readme`)
- **GitHub CLI**: `gh` required for `workspace-build-repo-list.py`

## Code Standards

### Type Annotations
All code must use strong typing with Python 3.10+ syntax (`X | Y` not `Union[X, Y]`).
Use `from __future__ import annotations` for forward references.

```python
def command(
    cmd: str | Sequence[str],
    *arguments: str,
    timeout: float | None = None,
) -> tuple[int, str, str]:
    ...
```

### Docstrings
Google docstring style. READMEs are auto-generated from docstrings — write good module and function docs, do not hand-edit README.md.

## Engineering Philosophy

- **Clarity first**: Write code for humans, then correctness, then performance
- **Simplicity**: Throw away what can't be done in a day, rewrite simpler tomorrow
- **No smart code**: Write straightforward, maintainable code
- **Comment WHY, not HOW**: Let code explain itself
