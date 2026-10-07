"""
Version extraction from pyproject.toml.

CLI usage:
    pk3 version [--path PATH]

Reads the [project].version field from pyproject.toml and prints it to stdout.
This allows shell scripts to obtain the package version without TOML parsing:

    VER=$(pk3 version)
    echo "Building version $VER"

Uses tomllib on Python 3.11+ and tomli on Python 3.10.
"""

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def get_version(path: str | Path = "pyproject.toml") -> str:
    """
    Read version from pyproject.toml.

    Args:
        path: Path to pyproject.toml file. Defaults to current directory.

    Returns:
        Version string from pyproject.toml.

    Raises:
        FileNotFoundError: If pyproject.toml doesn't exist.
        ValueError: If version cannot be found in the file.
    """
    path = Path(path)
    content = path.read_bytes()

    config = tomllib.loads(content.decode("utf-8"))
    version = config.get("project", {}).get("version")
    if version is None:
        raise ValueError(f"Could not find version in {path}")

    return version
