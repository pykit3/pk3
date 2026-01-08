"""
Version extraction from pyproject.toml.

CLI usage:
    pk3 version [--path PATH]

Reads the [project].version field from pyproject.toml and prints it to stdout.
This allows shell scripts to obtain the package version without TOML parsing:

    VER=$(pk3 version)
    echo "Building version $VER"

Uses tomllib (Python 3.11+) when available, falls back to regex parsing.
"""

import re
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None


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

    if tomllib:
        config = tomllib.loads(content.decode("utf-8"))
        return config["project"]["version"]

    # Fallback: regex for Python < 3.11
    match = re.search(rb'version\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1).decode("utf-8")

    raise ValueError(f"Could not find version in {path}")
