#!/usr/bin/env python3
"""Show a compact Git status table for the k3* package repositories."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

CONFLICT_STATES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    return result.stdout.rstrip("\n")


def worktree_status(lines: list[str]) -> str:
    counts = {"staged": 0, "unstaged": 0, "untracked": 0, "conflicts": 0}
    for line in lines:
        state = line[:2]
        if state == "??":
            counts["untracked"] += 1
        elif state in CONFLICT_STATES:
            counts["conflicts"] += 1
        else:
            if state[0] != " ":
                counts["staged"] += 1
            if state[1] != " ":
                counts["unstaged"] += 1
    parts = [f"{name}:{count}" for name, count in counts.items() if count]
    return ", ".join(parts) if parts else "clean"


def tag_status(repo: Path) -> str:
    output = git(repo, "tag", "--merged", "HEAD")
    if not output:
        return "-"
    tag = git(repo, "describe", "--tags", "--abbrev=0")
    count = git(repo, "rev-list", "--count", f"{tag}..HEAD")
    if count == "0":
        return tag
    return f"{tag} +{count}"


def status_row(repo: Path) -> tuple[str, str, str, str]:
    output = git(repo, "status", "--porcelain=v1", "--branch", "--untracked-files=all")
    lines = output.splitlines()
    branch = lines[0].removeprefix("## ")
    worktree = worktree_status(lines[1:])
    tag = "-"
    if not branch.startswith("No commits yet on "):
        tag = tag_status(repo)
    return repo.name, worktree, branch, tag


def print_table(rows: list[tuple[str, str, str, str]]) -> None:
    widths = []
    for column in zip(*rows):
        lengths = [len(value) for value in column]
        widths.append(max(lengths))
    for row in rows:
        cells = zip(row, widths)
        columns = [value.ljust(width) for value, width in cells]
        line = "  ".join(columns)
        print(line.rstrip())


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    workspace_dir = script_path.parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages_dir", nargs="?", type=Path, default=workspace_dir / "packages")
    parser.add_argument("--fetch", action="store_true", help="refresh remote branches and tags before reporting")
    args = parser.parse_args()
    args.packages_dir = args.packages_dir.expanduser()
    if not args.packages_dir.is_dir():
        parser.error(f"package directory does not exist: {args.packages_dir}")
    return args


def main() -> None:
    args = parse_args()
    rows = [("PACKAGE", "WORKTREE", "BRANCH / UPSTREAM", "TAG (+COMMITS)")]
    repos = sorted(args.packages_dir.glob("k3*"))
    for repo in repos:
        git_path = repo / ".git"
        if not git_path.exists():
            continue
        if args.fetch:
            git(repo, "fetch", "--prune", "--tags")
        row = status_row(repo)
        rows.append(row)
    print_table(rows)


if __name__ == "__main__":
    main()
