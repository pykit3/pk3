"""Git tag creation for releases."""

import subprocess
import sys
from pathlib import Path

from .version import get_version

if hasattr(sys, "getfilesystemencoding"):
    _defenc = sys.getfilesystemencoding()
if _defenc is None:
    _defenc = sys.getdefaultencoding()


def create_tag(path: str | Path = "pyproject.toml", prefix: str = "v") -> str:
    """
    Create a git tag based on version from pyproject.toml.

    Args:
        path: Path to pyproject.toml file.
        prefix: Tag prefix, defaults to "v".

    Returns:
        The created tag name (e.g., "v0.1.0").

    Raises:
        FileNotFoundError: If pyproject.toml doesn't exist.
        ValueError: If version cannot be found.
        RuntimeError: If git tag creation fails.
    """
    ver = get_version(path)
    tag = f"{prefix}{ver}"

    result = subprocess.run(
        ["git", "tag", tag],
        encoding=_defenc,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to create tag {tag}: {result.stderr}")

    return tag
