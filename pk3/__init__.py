"""pk3 - Build utilities for pykit3 packages."""

from importlib.metadata import version

__version__ = version("pk3")

from .version import get_version
from .tag import create_tag

__all__ = ["get_version", "create_tag", "__version__"]
