# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is `pk3`, a workspace repository for the pykit3 collection - a set of Python3 utility modules. The repository structure uses a sparse checkout organization:

- **Root directory (`pk3`)**: Contains management scripts and coordination tools
- **Module directories**: Each `k3*` module is stored under `github.com/pykit3/k3*` (some as independent git repos, others as working copies)
- **Template system**: Uses `tmpl` as a template for creating new modules

### Key Architecture Concepts

1. **Sparse Workspace Management**: Individual pykit3 modules are managed as separate working directories, some with their own git repositories
2. **Template-driven Development**: New modules are created by forking from `tmpl` and using `populate.py`
3. **Consistent Structure**: All modules follow the same directory layout and build system
4. **Cross-module Operations**: Scripts exist to apply changes across all modules simultaneously

## Common Development Commands

### Building and Documentation
```bash
# Build README for the main repository
make readme

# Build README for a specific module
cd github.com/pykit3/k3color && make readme

# Build documentation for a module
cd github.com/pykit3/k3color && make doc
```

### Testing
```bash
# Run tests for a specific module
cd github.com/pykit3/k3color && make test

# Run tests with specific environment
cd github.com/pykit3/k3color && sudo env "PATH=$PATH" UT_DEBUG=0 PYTHONPATH="$(cd ..; pwd)" python -m unittest discover -c --failfast -s .

# Test a single file
cd github.com/pykit3/k3color && python -m unittest test.test_color -v
```

### Release Management
```bash
# Prepare a module for release (generates setup.py)
cd github.com/pykit3/k3color && make release

# Install a module locally
cd github.com/pykit3/k3color && make install
```

### Cross-Repository Operations
```bash
# Apply template changes to all repos
./run-script-in-repos.sh repo-apply-tmpl.sh

# Run any script across all k3* repositories
./run-script-in-repos.sh <script_name> <args...>

# Copy template files from tmpl to current directory
./applytmpl.sh
```

## Module Development Workflow

### Creating a New Module
1. Fork from `tmpl` repository with name starting with `k3`
2. Clone the repository: `git clone git@github.com:pykit3/k3newmodule.git`
3. Populate the skeleton: `python ./_building/populate.py`
4. Update `__init__.py` with proper `__name__` and `__version__`
5. Implement functionality in appropriately named Python files

### Module Structure
Each module follows this standard layout:
```
k3modulename/
├── .github/workflows/        # CI/CD configurations
├── _building/               # Build utilities and common scripts  
├── docs/                    # Sphinx documentation
├── test/                    # Unit tests
├── __init__.py             # Module metadata and exports
├── main_module.py          # Primary implementation
├── LICENSE
├── Makefile               # Build commands
├── README.md              # Auto-generated, do not edit
├── requirements.txt       # Dependencies
└── setup.py              # Auto-generated for releases
```

### Version Management
- Update `__version__` in `__init__.py` using semantic versioning
- Commit version changes and run `make release` to create tags
- Pushing tags triggers automated PyPI publishing via GitHub Actions

## Testing Standards

- **Framework**: Uses Python's built-in `unittest` module
- **Discovery**: Tests are auto-discovered from `test/` directory
- **Naming**: Test files follow `test_*.py` pattern
- **Doctests**: Each module includes `test_doctest.py` for docstring testing
- **Environment**: Tests run with `PYTHONPATH` set to parent directory for local imports

## Documentation System

- **Generator**: Uses Sphinx for documentation building
- **Style**: Python docstrings follow Google docstring style
- **Auto-generation**: READMEs are auto-generated from code and should not be manually edited
- **Build Command**: `make doc` builds HTML documentation in `docs/` directory

## Repository Management Tools

### Key Scripts
- `build_list.py`: Generates repository lists and markdown tables using GitHub CLI
- `build_readme.py`: Auto-generates the main README.md from module data
- `run-script-in-repos.sh`: Executes scripts across all k3* subdirectories
- `applytmpl.sh`: Copies template changes to current repository

### GitHub Integration
- Uses `gh` CLI tool for repository management
- Automated CI/CD via GitHub Actions
- Repository metadata managed through `.github/settings.yml`

## Engineering Philosophy

From the README.md, this project follows these principles:
- **Clarity first**: Write code for humans, prioritize readability
- **Correctness over performance**: Focus on getting it right first
- **Simplicity**: Throw away what can't be done in a day, rewrite simpler tomorrow
- **No smart code**: Write straightforward, maintainable code
- **Comment WHY, not HOW**: Let code explain itself

## Dependencies and Requirements

- **Python**: Python 3.x
- **GitHub CLI**: Required for repository management (`gh` command)
- **Build Tools**: Standard Python build tools (pip, setuptools)
- **Testing**: Built-in unittest module
- **Documentation**: Sphinx for doc generation
