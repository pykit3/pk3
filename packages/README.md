# pykit3 Packages

This directory contains all pykit3 modules as independent repositories using sparse checkout.

## Structure

- `k3*/` - Individual pykit3 modules (each is a separate git repository)
- `tmpl/` - Template for creating new modules

## Usage

Modules are managed through scripts in `../scripts/`:
- Use `multi-repo-*.sh` to operate on all modules
- Use `dev-create-package.sh` to create new modules from template

Each module follows the standard pykit3 structure with its own:
- `__init__.py` - Version and exports
- `test/` - Unit tests
- `Makefile` - Build commands
- `pyproject.toml` - Package configuration
