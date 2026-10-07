"""Tests for pk3.tag module."""

import os
import subprocess
import tempfile
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
            check=False,
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
            check=False,
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

    def test_create_tag_in_repo_of_path(self):
        # Run from another repository: the tag must go to the one of pyproject.toml.
        pyproject = tag_test_worktree / "pyproject.toml"
        original_cwd = os.getcwd()

        with tempfile.TemporaryDirectory() as other_repo:
            subprocess.run(["git", "init", "-q", other_repo], check=True)
            identity = ["-c", "user.name=test", "-c", "user.email=test@example.com"]
            subprocess.run(
                ["git", "-C", other_repo, *identity, "commit", "-q", "--allow-empty", "-m", "init"], check=True
            )

            try:
                os.chdir(other_repo)
                tag = create_tag(pyproject)
            finally:
                os.chdir(original_cwd)

            other_tags = subprocess.run(
                ["git", "-C", other_repo, "tag", "-l"], capture_output=True, text=True, check=False
            )

        self.assertEqual("v1.2.3", tag)
        self.assertEqual("", other_tags.stdout)

        result = subprocess.run(
            ["git", f"--git-dir={tag_test_git}", "tag", "-l", "v1.2.3"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual("v1.2.3\n", result.stdout)

    def test_create_tag_uncommitted_changes_fails(self):
        # The version bump is not committed: HEAD does not hold the version to tag.
        with tempfile.TemporaryDirectory() as repo:
            pyproject = Path(repo) / "pyproject.toml"
            pyproject.write_text('[project]\nversion = "1.0.0"\n')
            identity = ["-c", "user.name=test", "-c", "user.email=test@example.com"]
            subprocess.run(["git", "init", "-q", repo], check=True)
            subprocess.run(["git", "-C", repo, "add", "pyproject.toml"], check=True)
            subprocess.run(["git", "-C", repo, *identity, "commit", "-q", "-m", "init"], check=True)
            pyproject.write_text('[project]\nversion = "1.0.1"\n')

            with self.assertRaises(RuntimeError):
                create_tag(pyproject)

            tags = subprocess.run(["git", "-C", repo, "tag", "-l"], capture_output=True, text=True, check=False)

        self.assertEqual("", tags.stdout)

    def test_create_tag_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            create_tag("/nonexistent/pyproject.toml")


if __name__ == "__main__":
    unittest.main()
