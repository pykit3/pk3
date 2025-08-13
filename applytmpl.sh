#!/bin/sh

# Apply changes from the tmpl repo to the current repo.
# Run it in the _building dir in a repo, such as in `k3git`.

cp ../tmpl/_building/Makefile                  ./_building/
cp ../tmpl/_building/README.md                 ./_building/
cp ../tmpl/_building/README.md.j2              ./_building/
cp ../tmpl/_building/__init__.py               ./_building/
cp ../tmpl/_building/build_readme.py           ./_building/
cp ../tmpl/_building/build_setup.py            ./_building/
cp ../tmpl/_building/building-requirements.txt ./_building/
cp ../tmpl/_building/common.mk                 ./_building/
cp ../tmpl/_building/install.sh                ./_building/
cp ../tmpl/_building/requirements.txt          ./_building/

cp ../tmpl/docs/source/conf.py                 ./docs/source/

cp ../tmpl/.github/workflows/python-package.yml .github/workflows/
cp ../tmpl/.github/workflows/python-publish.yml .github/workflows/
