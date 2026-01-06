"""CLI entry point for pk3."""

import argparse
import sys

from .tag import create_tag
from .version import get_version
from .publish import publish


def main():
    parser = argparse.ArgumentParser(description="pk3 build utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # version command
    ver_parser = subparsers.add_parser("version", help="Show version from pyproject.toml")
    ver_parser.add_argument("--path", default="pyproject.toml", help="Path to pyproject.toml")

    # tag command
    tag_parser = subparsers.add_parser("tag", help="Create git tag from version")
    tag_parser.add_argument("--path", default="pyproject.toml", help="Path to pyproject.toml")
    tag_parser.add_argument("--prefix", default="v", help="Tag prefix (default: v)")

    # publish command
    pub_parser = subparsers.add_parser("publish", help="Build and publish to PyPI")
    pub_parser.add_argument("--test", action="store_true", help="Publish to TestPyPI")

    args = parser.parse_args()

    if args.command == "version":
        print(get_version(args.path))
    elif args.command == "tag":
        tag = create_tag(args.path, prefix=args.prefix)
        print(f"Created tag: {tag}")
        print("Run 'git push --tags' to push the tag")
    elif args.command == "publish":
        publish(test=args.test)
        print("Published successfully")


if __name__ == "__main__":
    main()
