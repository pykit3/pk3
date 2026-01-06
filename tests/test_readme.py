"""Tests for pk3.readme module."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pk3.readme import build_readme


class TestBuildReadme(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_build_readme_basic(self):
        """Test basic README generation."""
        pkg_dir = Path(self.tmpdir) / "testpkg"
        pkg_dir.mkdir()

        # Create pyproject.toml
        (pkg_dir / "pyproject.toml").write_text('''
[project]
name = "testpkg"
version = "1.0.0"
description = "A test package"
''')

        # Create __init__.py with docstring
        (pkg_dir / "__init__.py").write_text('''
"""
This is the package docstring.

Example usage:

    >>> import testpkg
    >>> print("hello")
    hello
"""

__name__ = "testpkg"
__version__ = "1.0.0"
''')

        output = build_readme(pkg_dir)

        self.assertTrue(Path(output).exists())
        content = Path(output).read_text()

        expected = """\
# testpkg

[![Action-CI](https://github.com/pykit3/testpkg/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/testpkg/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/testpkg/badge/?version=stable)](https://testpkg.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/testpkg)](https://pypi.org/project/testpkg)

A test package

testpkg is a component of [pykit3] project: a python3 toolkit set.


This is the package docstring.

Example usage:

    >>> import testpkg
    >>> print("hello")
    hello



# Install

```
pip install testpkg
```

# Synopsis

```python
>>> import testpkg
>>> print("hello")
hello
```

#   Author

Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>


[pykit3]: https://github.com/pykit3
"""
        self.assertEqual(content, expected.rstrip("\n"))

    def test_build_readme_missing_pyproject(self):
        """Test error when pyproject.toml is missing."""
        pkg_dir = Path(self.tmpdir) / "nopyproject"
        pkg_dir.mkdir()

        with self.assertRaises(FileNotFoundError):
            build_readme(pkg_dir)

    def test_build_readme_custom_output(self):
        """Test custom output path."""
        pkg_dir = Path(self.tmpdir) / "custompkg"
        pkg_dir.mkdir()

        (pkg_dir / "pyproject.toml").write_text('''
[project]
name = "custompkg"
version = "1.0.0"
description = "Custom package"
''')

        (pkg_dir / "__init__.py").write_text('''
"""Custom package docstring."""
__name__ = "custompkg"
''')

        output = build_readme(pkg_dir, output_path="CUSTOM.md")

        # Use resolve() to handle /private/var vs /var on macOS
        self.assertEqual(Path(output).resolve(), (pkg_dir / "CUSTOM.md").resolve())
        self.assertTrue((pkg_dir / "CUSTOM.md").exists())

        content = Path(output).read_text()
        expected = """\
# custompkg

[![Action-CI](https://github.com/pykit3/custompkg/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/custompkg/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/custompkg/badge/?version=stable)](https://custompkg.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/custompkg)](https://pypi.org/project/custompkg)

Custom package

custompkg is a component of [pykit3] project: a python3 toolkit set.

Custom package docstring.


# Install

```
pip install custompkg
```

# Synopsis

```python

```

#   Author

Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>


[pykit3]: https://github.com/pykit3
"""
        self.assertEqual(content, expected.rstrip("\n"))

    def test_build_readme_with_synopsis_file(self):
        """Test README generation with synopsis.txt file."""
        pkg_dir = Path(self.tmpdir) / "synopsispkg"
        pkg_dir.mkdir()

        (pkg_dir / "pyproject.toml").write_text('''
[project]
name = "synopsispkg"
version = "1.0.0"
description = "Synopsis package"
''')

        (pkg_dir / "__init__.py").write_text('''
"""Package with synopsis file."""
__name__ = "synopsispkg"
''')

        (pkg_dir / "synopsis.txt").write_text("# Additional synopsis content\nprint('hello')")

        output = build_readme(pkg_dir)
        content = Path(output).read_text()

        expected = """\
# synopsispkg

[![Action-CI](https://github.com/pykit3/synopsispkg/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/synopsispkg/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/synopsispkg/badge/?version=stable)](https://synopsispkg.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/synopsispkg)](https://pypi.org/project/synopsispkg)

Synopsis package

synopsispkg is a component of [pykit3] project: a python3 toolkit set.

Package with synopsis file.


# Install

```
pip install synopsispkg
```

# Synopsis

```python

# Additional synopsis content
print('hello')
```

#   Author

Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>


[pykit3]: https://github.com/pykit3
"""
        self.assertEqual(content, expected.rstrip("\n"))


class TestReadmeCLI(unittest.TestCase):
    def test_readme_help(self):
        """Test pk3 readme --help."""
        result = subprocess.run(
            ["pk3", "readme", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--dir", result.stdout)
        self.assertIn("--template", result.stdout)
        self.assertIn("--output", result.stdout)


if __name__ == "__main__":
    unittest.main()
