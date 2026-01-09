# pk3 Workspace Scripts

This directory contains all workspace management scripts for the pykit3 collection.

## Script Naming Convention

Scripts follow a clear prefix-based naming system:

- **`multi-repo-*`** - Operate on all k3* packages simultaneously
- **`single-repo-*`** - Per-repository operations (executed via multi-repo-exec)
- **`workspace-*`** - Manage pk3 workspace documentation and metadata
- **`dev-*`** - Developer utilities for package and repository management

## Quick Reference

### Multi-Repository Operations

Execute scripts across all k3* packages:

```bash
# Run a script in all k3* repositories
../scripts/multi-repo-exec.sh <script_name> <args...>

# Clone all pykit3 packages from GitHub
./scripts/multi-repo-clone-all.sh

# Clean up merged/stale branches across all repos
./scripts/multi-repo-cleanup-branches.sh          # Show what would be removed
./scripts/multi-repo-cleanup-branches.sh --dry-run # Preview mode
```

### Workspace Documentation

Build and maintain pk3 workspace documentation:

```bash
# Generate repository list and README (recommended: use make)
make readme

# Or run scripts individually:
python scripts/workspace-build-repo-list.py  # Generates docs/repos.txt, repo_def.md, repo_table.md
python scripts/workspace-build-readme.py     # Generates README.md from template
```

### Development Tools

Utilities for package and repository management:

```bash
# Create a new k3* package from template
./scripts/dev-create-package.sh <parent_dir> <package_name>
# Example: ./scripts/dev-create-package.sh packages k3newmodule

# Publish package to PyPI
cd <package_dir>
TWINE_PASSWORD=pypi-xxx ../../scripts/dev-publish-to-pypi.sh        # PyPI
TWINE_PASSWORD=pypi-xxx ../../scripts/dev-publish-to-pypi.sh test   # TestPyPI

# Open package URLs in browser
./scripts/dev-open-repo-urls.sh pypi    # Open PyPI pages
./scripts/dev-open-repo-urls.sh action  # Open GitHub Actions pages
```

### Single-Repository Helpers

These scripts operate on individual repositories and are typically executed via `multi-repo-exec.sh`:

```bash
# Add entries to .gitignore across all repos
./scripts/multi-repo-exec.sh single-repo-add-gitignore.sh "*.pyc"

# Convert git remote URLs across all repos
./scripts/multi-repo-exec.sh single-repo-convert-remote.sh

# Merge a PR branch in all repos
./scripts/multi-repo-exec.sh single-repo-merge-pr.sh feature-branch

# Cherry-pick a PR branch in all repos
./scripts/multi-repo-exec.sh single-repo-pick-pr.sh feature-branch
```

## Common Workflows

### Initial Setup

Clone all pykit3 packages:

```bash
./scripts/multi-repo-clone-all.sh
```

### Regular Maintenance

Update documentation after adding/removing packages:

```bash
make readme
```

Clean up stale branches across all repositories:

```bash
./scripts/multi-repo-cleanup-branches.sh --dry-run  # Preview
./scripts/multi-repo-cleanup-branches.sh            # Execute
```

### Creating a New Package

```bash
./scripts/dev-create-package.sh packages k3mypackage
cd packages/k3mypackage
# Implement your package...
```

### Applying Changes to All Repositories

```bash
# Example: Add .DS_Store to all .gitignore files
./scripts/multi-repo-exec.sh single-repo-add-gitignore.sh ".DS_Store"
```

## Script Details

### Multi-Repo Scripts

| Script | Description |
|--------|-------------|
| `multi-repo-exec.sh` | Execute any script across all k3* packages in packages/ |
| `multi-repo-clone-all.sh` | Clone all pykit3 repositories listed in docs/repos.txt |
| `multi-repo-cleanup-branches.sh` | Remove merged/gone branches and prune remote refs |

### Workspace Scripts

| Script | Description |
|--------|-------------|
| `workspace-build-repo-list.py` | Generate repository lists using GitHub CLI (`gh`) |
| `workspace-build-readme.py` | Generate README.md from Jinja2 template |

### Development Scripts

| Script | Description |
|--------|-------------|
| `dev-create-package.sh` | Create new k3* package from tmpl template |
| `dev-publish-to-pypi.sh` | Publish Python package to PyPI or TestPyPI |
| `dev-open-repo-urls.sh` | Open PyPI or GitHub Actions URLs for all packages |

### Single-Repo Scripts

| Script | Description |
|--------|-------------|
| `single-repo-add-gitignore.sh` | Append entries to .gitignore |
| `single-repo-convert-remote.sh` | Convert git remote URLs |
| `single-repo-merge-pr.sh` | Merge PR branch with fast-forward |
| `single-repo-pick-pr.sh` | Cherry-pick commits from PR branch |

## Dependencies

- **Python 3.x** - For workspace builder scripts
- **GitHub CLI (`gh`)** - Required by workspace-build-repo-list.py
- **Git** - For repository operations
- **Twine** - For PyPI publishing (dev-publish-to-pypi.sh)
- **k3handy** - Required by workspace-build-repo-list.py
- **Jinja2** - Required by workspace-build-readme.py

## Notes

- All scripts are designed to be run from the pk3 repository root
- Multi-repo scripts automatically discover k3* directories in packages/
- Single-repo scripts are meant to be executed per-repository via multi-repo-exec.sh
- Workspace builder scripts generate files in docs/ directory
