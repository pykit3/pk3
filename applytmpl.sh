#!/bin/sh

# Apply changes from the tmpl repo to the current repo.
# Run it in a repo root dir, such as in `k3git`.

# The repos are organized in:
# ~/xp/vcs/github.com/pykit3/pk3/github.com/pykit3/k3down2
template_repo_path=../../../tmpl

cp $template_repo_path/_building/Makefile                  ./_building/
cp $template_repo_path/_building/README.md                 ./_building/
cp $template_repo_path/_building/README.md.j2              ./_building/
cp $template_repo_path/_building/__init__.py               ./_building/
cp $template_repo_path/_building/build_readme.py           ./_building/
cp $template_repo_path/_building/build_setup.py            ./_building/
cp $template_repo_path/_building/building-requirements.txt ./_building/
cp $template_repo_path/_building/common.mk                 ./_building/
cp $template_repo_path/_building/install.sh                ./_building/
cp $template_repo_path/_building/publish.sh                ./_building/
cp $template_repo_path/_building/requirements.txt          ./_building/

cp $template_repo_path/docs/source/conf.py                 ./docs/source/

cp $template_repo_path/.github/workflows/python-package.yml .github/workflows/
cp $template_repo_path/.github/workflows/python-publish.yml .github/workflows/
