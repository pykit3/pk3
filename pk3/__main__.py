"""CLI entry point for pk3."""

import argparse

from .tag import create_tag
from .version import get_version
from .publish import publish
from .readme import build_readme


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

    # readme command
    readme_parser = subparsers.add_parser("readme", help="Generate README.md from package docstring")
    readme_parser.add_argument("--dir", default=".", help="Package directory (default: current)")
    readme_parser.add_argument("--template", help="Path to Jinja2 template file")
    readme_parser.add_argument("--output", default="README.md", help="Output file (default: README.md)")

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
    elif args.command == "readme":
        output = build_readme(args.dir, args.template, args.output)
        print(f"Generated: {output}")


if __name__ == "__main__":
    main()
