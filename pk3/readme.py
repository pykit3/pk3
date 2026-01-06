"""README generation from package docstrings and templates."""

import doctest
import importlib.util
import sys
from pathlib import Path

import jinja2
import yaml

try:
    import tomllib
except ImportError:
    tomllib = None

import re


DEFAULT_TEMPLATE = """\
# {{ name }}

[![Action-CI](https://github.com/pykit3/{{ name }}/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/{{ name }}/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/{{ name }}/badge/?version=stable)](https://{{ name }}.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/{{ name }})](https://pypi.org/project/{{ name }})

{{ description }}

{{ name }} is a component of [pykit3] project: a python3 toolkit set.

{{ package_doc }}


# Install

```
pip install {{ name }}
```

# Synopsis

```python
{{ synopsis }}
```

#   Author

Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>


[pykit3]: https://github.com/pykit3
"""


def _read_toml(path: Path) -> dict:
    """Read TOML file and return parsed content."""
    content = path.read_bytes()

    if tomllib:
        return tomllib.loads(content.decode("utf-8"))

    # Fallback for Python < 3.11: basic parsing
    text = content.decode("utf-8")
    result = {"project": {}}

    # Extract name
    match = re.search(r'name\s*=\s*"([^"]+)"', text)
    if match:
        result["project"]["name"] = match.group(1)

    # Extract version
    match = re.search(r'version\s*=\s*"([^"]+)"', text)
    if match:
        result["project"]["version"] = match.group(1)

    # Extract description
    match = re.search(r'description\s*=\s*"([^"]+)"', text)
    if match:
        result["project"]["description"] = match.group(1)

    return result


def _load_package(package_dir: Path) -> tuple[str, object]:
    """
    Load package from directory.

    Returns:
        tuple: (package_name, package_module)
    """
    init_file = package_dir / "__init__.py"

    # Try to read package name from __init__.py
    package_name = None
    if init_file.exists():
        content = init_file.read_text()
        for line in content.splitlines():
            if line.strip().startswith("__name__"):
                # Extract from __name__ = "package_name"
                match = re.search(r'__name__\s*=\s*["\']([^"\']+)["\']', line)
                if match:
                    package_name = match.group(1)
                    break

    if not package_name:
        # Fallback: use directory name
        package_name = package_dir.name

    # Add parent to path for imports
    parent = str(package_dir.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)

    # Also add grandparent for indirect dependencies
    grandparent = str(package_dir.parent.parent)
    if grandparent not in sys.path:
        sys.path.insert(0, grandparent)

    # Load module
    spec = importlib.util.spec_from_file_location(package_name, init_file)
    pkg = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = pkg
    spec.loader.exec_module(pkg)

    return package_name, pkg


def _get_examples(pkg) -> str:
    """Extract examples from package docstring using doctest parser."""
    doc = pkg.__doc__ or ""
    parser = doctest.DocTestParser()
    examples = parser.get_examples(doc)

    lines = []
    for ex in examples:
        lines.append(">>> " + ex.source.strip())
        if ex.want.strip():
            lines.append(ex.want.strip())

    return "\n".join(lines)


def _read_synopsis_files(package_dir: Path) -> str:
    """Read optional synopsis.txt or synopsis.py files."""
    result = ""
    for filename in ("synopsis.txt", "synopsis.py"):
        synopsis_file = package_dir / filename
        if synopsis_file.exists():
            result += "\n" + synopsis_file.read_text()
    return result


def _get_description(package_dir: Path, pyproject: dict) -> str:
    """
    Get package description.

    Priority: .github/settings.yml > pyproject.toml
    """
    # Try .github/settings.yml first
    settings_file = package_dir / ".github" / "settings.yml"
    if settings_file.exists():
        cfg = yaml.safe_load(settings_file.read_text())
        if cfg and "repository" in cfg and "description" in cfg["repository"]:
            return cfg["repository"]["description"]

    # Fall back to pyproject.toml
    return pyproject.get("project", {}).get("description", "")


def build_readme(
    package_dir: str | Path = ".",
    template_path: str | Path | None = None,
    output_path: str | Path = "README.md",
) -> str:
    """
    Build README.md from package docstring and template.

    Args:
        package_dir: Directory containing the package. Defaults to current directory.
        template_path: Path to Jinja2 template file. If None, uses default template.
        output_path: Output file path. Defaults to README.md.

    Returns:
        Path to generated README file.
    """
    package_dir = Path(package_dir).resolve()
    output_path = package_dir / output_path

    # Read pyproject.toml
    pyproject_path = package_dir / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found in {package_dir}")

    pyproject = _read_toml(pyproject_path)

    # Load package
    package_name, pkg = _load_package(package_dir)

    # Build template variables
    j2vars = {
        "name": pyproject.get("project", {}).get("name", package_name),
        "description": _get_description(package_dir, pyproject),
        "package_doc": pkg.__doc__ or "",
        "synopsis": _get_examples(pkg) + _read_synopsis_files(package_dir),
    }

    # Load and render template
    if template_path:
        template_path = Path(template_path)
        template_loader = jinja2.FileSystemLoader(searchpath=str(template_path.parent))
        template_env = jinja2.Environment(
            loader=template_loader, undefined=jinja2.StrictUndefined
        )
        template = template_env.get_template(template_path.name)
    else:
        template = jinja2.Environment(
            undefined=jinja2.StrictUndefined
        ).from_string(DEFAULT_TEMPLATE)

    content = template.render(j2vars)

    # Write output
    output_path.write_text(content)

    return str(output_path)
