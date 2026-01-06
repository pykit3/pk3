# pk3

Build utilities for pykit3 packages.

## Installation

```bash
pip install pk3
```

## CLI Usage

### Show version from pyproject.toml

```bash
pk3 version
# 0.1.1

pk3 version --path /path/to/pyproject.toml
```

### Create git tag from version

```bash
pk3 tag
# Created tag: v0.1.1
# Run 'git push --tags' to push the tag

pk3 tag --prefix release-
# Created tag: release-0.1.1

pk3 tag --prefix ""
# Created tag: 0.1.1
```

## Python API

```python
from pk3 import get_version, create_tag

# Get version from pyproject.toml
version = get_version()  # reads ./pyproject.toml
version = get_version("/path/to/pyproject.toml")

# Create git tag
tag = create_tag()                    # creates "v0.1.1"
tag = create_tag(prefix="release-")   # creates "release-0.1.1"
tag = create_tag(prefix="")           # creates "0.1.1"
```

## Publishing

Sub-repos can reuse the publish script:

```bash
# Symlink in sub-repo
ln -s ../../pk3/publish.sh ./publish.sh

# Publish to PyPI
TWINE_PASSWORD=pypi-xxx ./publish.sh

# Publish to TestPyPI first
TWINE_PASSWORD=pypi-xxx ./publish.sh test
```
