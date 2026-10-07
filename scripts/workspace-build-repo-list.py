#!/usr/bin/env python

# require:
#   gh: github cli: brew install gh

import json
import os

import k3handy


def load_repos():
    j = k3handy.cmdout("gh", "repo", "list", "pykit3", "--limit", "1000", "--json", "name,url,description")
    j = "".join(j)
    repos = json.loads(j)

    return repos


def filter(repos):
    """
    remove support repos
    """

    not_need = [
        "tmpl",  # tempalte repo
        "pk3",  # this repo
        "gh-config",  # a config container for maintaining github configs.
    ]

    return [x for x in repos if x["name"] not in not_need]


def build_md_ref_list(repos):
    """
    Build a reference definition list in markdown syntax, such as:

            [k3color]:      https://github.com/pykit3/k3color
            [k3common]:     https://github.com/pykit3/k3common
    """

    res = []

    for repo in repos:
        res.append("[{name}]: {url}".format(**repo))

    return "\n".join(res)


def build_md_table(repos):
    """
    Build a reference definition list in markdown syntax, such as:

        | Name             | Desc                                                               |
        | :--              | :--                                                                |
        | [k3color][]      | create colored text on terminal                                    |
        | [k3common][]     | dependency manager                                                 |
    """

    res = [
        "| Name | Desc |",
        "| :-- | :-- |",
    ]

    for repo in repos:
        res.append("| [{name}][] | {description} |".format(**repo))

    return "\n".join(res)


def write_files(contents):
    """
    Write every `path: text` item of `contents`.

    All texts go to temporary files first, so a failure leaves each file
    either old or new, never truncated.
    """

    for path, text in contents.items():
        with open(path + ".tmp", "w") as f:
            f.write(text)

    for path in contents:
        os.replace(path + ".tmp", path)


if __name__ == "__main__":
    repos = load_repos()
    repos.sort(key=lambda x: x["name"])
    repos = filter(repos)
    names = [x["name"] for x in repos]

    write_files(
        {
            "docs/repos.txt": "\n".join(names) + "\n",
            "docs/repo_def.md": build_md_ref_list(repos),
            "docs/repo_table.md": build_md_table(repos),
        }
    )
