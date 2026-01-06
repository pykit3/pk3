"""Tests for pk3.version module."""

import tempfile
import unittest
from pathlib import Path

from pk3.version import get_version


class TestGetVersion(unittest.TestCase):
    def test_get_version_from_valid_pyproject(self):
        content = b'''
[project]
name = "test-package"
version = "1.2.3"
'''
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
            f.write(content)
            f.flush()
            result = get_version(f.name)

        self.assertEqual(result, "1.2.3")

    def test_get_version_with_complex_pyproject(self):
        content = b'''
[build-system]
requires = ["setuptools>=61.0"]

[project]
name = "complex-package"
version = "0.5.0"
description = "A test package"
dependencies = ["requests>=2.0"]
'''
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
            f.write(content)
            f.flush()
            result = get_version(f.name)

        self.assertEqual(result, "0.5.0")

    def test_get_version_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_version("/nonexistent/path/pyproject.toml")

    def test_get_version_no_version_field(self):
        content = b'''
[project]
name = "no-version-package"
'''
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
            f.write(content)
            f.flush()
            with self.assertRaises((ValueError, KeyError)):
                get_version(f.name)

    def test_get_version_accepts_path_object(self):
        content = b'''
[project]
version = "2.0.0"
'''
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
            f.write(content)
            f.flush()
            result = get_version(Path(f.name))

        self.assertEqual(result, "2.0.0")

    def test_get_version_from_actual_pyproject(self):
        """Test reading version from the actual pk3 pyproject.toml."""
        pk3_root = Path(__file__).parent.parent
        pyproject_path = pk3_root / "pyproject.toml"

        if pyproject_path.exists():
            result = get_version(pyproject_path)
            self.assertEqual(result, "0.1.0")


if __name__ == "__main__":
    unittest.main()
