#!/bin/sh

name="$1"
echo name:$name
rm -rf dist
MOD=$name python make-setup.py
python setup.py sdist
twine upload dist/*

exit 0

cd dist
tar -xzf pykit*.tar.gz
