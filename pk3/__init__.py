"""pk3 - Build utilities for pykit3 packages."""

from importlib.metadata import version

__version__ = version("pk3")

from .publish import publish
from .readme import build_readme
from .tag import create_tag
from .version import get_version

__all__ = ["__version__", "build_readme", "create_tag", "get_version", "publish"]
