"""Publish package to PyPI."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def publish(test: bool = False) -> None:
    """
    Build and publish package to PyPI.

    Args:
        test: If True, publish to TestPyPI instead of PyPI.

    Raises:
        RuntimeError: If TWINE_PASSWORD is not set or build/upload fails.
    """
    password = os.environ.get("TWINE_PASSWORD")
    if not password:
        raise RuntimeError(
            "TWINE_PASSWORD not set\n"
            "Usage: TWINE_PASSWORD=pypi-xxx pk3 publish [--test]"
        )

    # Clean previous builds
    for pattern in ["dist", "build", "*.egg-info"]:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    # Build
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Build failed:\n{result.stdout}\n{result.stderr}")

    # Upload
    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"

    cmd = [sys.executable, "-m", "twine", "upload"]
    if test:
        cmd.extend(["--repository", "testpypi"])
    cmd.append("dist/*")

    result = subprocess.run(
        " ".join(cmd),
        shell=True,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Upload failed:\n{result.stdout}\n{result.stderr}")
