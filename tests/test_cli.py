"""Tests for pk3 CLI."""

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pk3.__main__ import main

this_base = Path(__file__).parent
tag_test_git = this_base / "testdata" / "tag_test_git"
tag_test_worktree = this_base / "testdata" / "tag_test_worktree"


def _clean_testdata():
    """Reset testdata to clean state."""
    git_file = tag_test_worktree / ".git"
    if git_file.exists():
        git_file.unlink()

    for tag in ["v1.2.3", "release-1.2.3", "1.2.3"]:
        subprocess.run(
            ["git", f"--git-dir={tag_test_git}", "tag", "-d", tag],
            capture_output=True,
        )


class TestCLIVersion(unittest.TestCase):
    def test_version_command(self):
        pyproject = this_base.parent / "pyproject.toml"

        with patch.object(sys, "argv", ["pk3", "version", "--path", str(pyproject)]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called()
                # Version should be a valid semver string
                args = mock_print.call_args[0][0]
                self.assertRegex(args, r"^\d+\.\d+\.\d+")

    def test_version_from_testdata(self):
        pyproject = tag_test_worktree / "pyproject.toml"

        with patch.object(sys, "argv", ["pk3", "version", "--path", str(pyproject)]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with("1.2.3")


class TestCLITag(unittest.TestCase):
    def setUp(self):
        _clean_testdata()
        (tag_test_worktree / ".git").write_text("gitdir: ../tag_test_git")

    def tearDown(self):
        _clean_testdata()

    def test_tag_command(self):
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        try:
            os.chdir(tag_test_worktree)
            with patch.object(sys, "argv", ["pk3", "tag", "--path", str(pyproject)]):
                with patch("builtins.print") as mock_print:
                    main()
                    calls = [str(c) for c in mock_print.call_args_list]
                    self.assertTrue(any("v1.2.3" in c for c in calls))
        finally:
            os.chdir(original_cwd)

    def test_tag_custom_prefix(self):
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        try:
            os.chdir(tag_test_worktree)
            with patch.object(sys, "argv", ["pk3", "tag", "--path", str(pyproject), "--prefix", "release-"]):
                with patch("builtins.print") as mock_print:
                    main()
                    calls = [str(c) for c in mock_print.call_args_list]
                    self.assertTrue(any("release-1.2.3" in c for c in calls))
        finally:
            os.chdir(original_cwd)


class TestCLISubprocess(unittest.TestCase):
    """Test CLI via subprocess (integration test)."""

    def test_version_subprocess(self):
        pyproject = this_base.parent / "pyproject.toml"
        result = subprocess.run(
            ["pk3", "version", "--path", str(pyproject)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertRegex(result.stdout.strip(), r"^\d+\.\d+\.\d+")

    def test_help_subprocess(self):
        result = subprocess.run(
            ["pk3", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("version", result.stdout)
        self.assertIn("tag", result.stdout)


if __name__ == "__main__":
    unittest.main()
