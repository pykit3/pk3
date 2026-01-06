"""Tests for pk3.tag module."""

import os
import subprocess
import unittest
from pathlib import Path

from pk3.tag import create_tag

this_base = Path(__file__).parent
tag_test_git = this_base / "testdata" / "tag_test_git"
tag_test_worktree = this_base / "testdata" / "tag_test_worktree"


def _clean_testdata():
    """Reset testdata to clean state."""
    # Remove .git file from worktree
    git_file = tag_test_worktree / ".git"
    if git_file.exists():
        git_file.unlink()

    # Delete test tags
    for tag in ["v1.2.3", "release-1.2.3", "1.2.3"]:
        subprocess.run(
            ["git", f"--git-dir={tag_test_git}", "tag", "-d", tag],
            capture_output=True,
        )


class TestCreateTag(unittest.TestCase):
    def setUp(self):
        _clean_testdata()
        # Link worktree to git dir (same as k3git pattern)
        (tag_test_worktree / ".git").write_text("gitdir: ../tag_test_git")

    def tearDown(self):
        _clean_testdata()

    def test_create_tag_default_prefix(self):
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        try:
            os.chdir(tag_test_worktree)
            tag = create_tag(pyproject)
        finally:
            os.chdir(original_cwd)

        self.assertEqual(tag, "v1.2.3")

        # Verify tag exists
        result = subprocess.run(
            ["git", f"--git-dir={tag_test_git}", "tag", "-l"],
            capture_output=True,
            text=True,
        )
        self.assertIn("v1.2.3", result.stdout)

    def test_create_tag_custom_prefix(self):
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        try:
            os.chdir(tag_test_worktree)
            tag = create_tag(pyproject, prefix="release-")
        finally:
            os.chdir(original_cwd)

        self.assertEqual(tag, "release-1.2.3")

    def test_create_tag_no_prefix(self):
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        try:
            os.chdir(tag_test_worktree)
            tag = create_tag(pyproject, prefix="")
        finally:
            os.chdir(original_cwd)

        self.assertEqual(tag, "1.2.3")

    def test_create_tag_duplicate_fails(self):
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        try:
            os.chdir(tag_test_worktree)
            create_tag(pyproject)

            with self.assertRaises(RuntimeError):
                create_tag(pyproject)
        finally:
            os.chdir(original_cwd)

    def test_create_tag_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            create_tag("/nonexistent/pyproject.toml")


if __name__ == "__main__":
    unittest.main()
