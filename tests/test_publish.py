"""Tests for pk3.publish module."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pk3.publish import publish


class TestPublish(unittest.TestCase):
    def test_publish_missing_password(self):
        """Test that publish raises error when TWINE_PASSWORD is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Ensure TWINE_PASSWORD is not set
            os.environ.pop("TWINE_PASSWORD", None)
            with self.assertRaises(RuntimeError) as ctx:
                publish()
            self.assertIn("TWINE_PASSWORD not set", str(ctx.exception))

    def test_publish_missing_password_message(self):
        """Test error message includes usage hint."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("TWINE_PASSWORD", None)
            with self.assertRaises(RuntimeError) as ctx:
                publish()
            self.assertIn("pk3 publish", str(ctx.exception))

    def test_publish_passes_dist_files_to_twine(self):
        # Each built file is its own argument, so no shell is needed to expand "dist/*".
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append((cmd, kwargs.get("shell", False)))
            if cmd == [sys.executable, "-m", "build"]:
                os.mkdir("dist")
                Path("dist/pkg-1.0.tar.gz").touch()
                Path("dist/pkg-1.0-py3-none-any.whl").touch()
            return subprocess.CompletedProcess(cmd, 0, "", "")

        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as d:
            try:
                os.chdir(d)
                env = {"TWINE_PASSWORD": "pypi-test"}
                with patch.dict(os.environ, env), patch.object(subprocess, "run", side_effect=fake_run):
                    publish()
            finally:
                os.chdir(original_cwd)

        upload = [sys.executable, "-m", "twine", "upload", "dist/pkg-1.0-py3-none-any.whl", "dist/pkg-1.0.tar.gz"]
        self.assertEqual([([sys.executable, "-m", "build"], False), (upload, False)], calls)


if __name__ == "__main__":
    unittest.main()
