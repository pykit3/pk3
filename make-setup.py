#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys
import imp

import setuptools
import yaml
import requirements

if hasattr(sys, 'getfilesystemencoding'):
    defenc = sys.getfilesystemencoding()
if defenc is None:
    defenc = sys.getdefaultencoding()

name = os.environ.get("MOD")


def get_ver(name):
    pkg = imp.load_source(name, name + '/__init__.py')
    pkgver = pkg.__version__

    sb = subprocess.Popen(["git", "tag", "v"+pkgver], cwd=name,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sb.communicate()
    if sb.returncode != 0:
        raise Exception("failure to add tag: " + pkgver, out, err)
    return pkgver

    sb = subprocess.Popen(["git", "describe", "--tags"], cwd=name, stdout=subprocess.PIPE)
    out, _ = sb.communicate()
    out = out.decode(defenc, 'surrogateescape')
    return out.strip().lstrip('v')


def get_gh_config(name):
    with open(name + '/.github/settings.yml', 'r') as f:
        cont = f.read()

    cfg = yaml.load(cont)
    tags = cfg['repository']['topics'].split(',')
    tags = [x.strip() for x in tags]
    cfg['repository']['topics'] = tags
    return cfg

def get_travis(name):
    try:
        with open(name + '/.travis.yml', 'r') as f:
            cont = f.read()
    except OSError:
        return None

    cfg = yaml.load(cont)
    return cfg


def get_compatible(name):

    # https://pypi.org/classifiers/

    rst = []
    t = get_travis(name)
    if t is None:
        return ["Programming Language :: Python :: 3"]

    for v in t['python']:
        if v.startswith('pypy'):
            v = "Implementation :: PyPy"
        rst.append("Programming Language :: Python :: {}".format(v))

    return rst

def get_req(name):
    try:
        with open(name + '/requirements.txt', 'r') as f:
            req = list(requirements.parse(f))
    except OSError:
        req = []

    # req.name, req.specs, req.extras
    # Django [('>=', '1.11'), ('<', '1.12')]
    # six [('==', '1.10.0')]
    req = [ x.name + ','.join([a+b for a, b in x.specs])
            for x in req
    ]

    return req


cfg = get_gh_config(name)

ver = get_ver(name)
description = cfg['repository']['description']
long_description = open(name + '/README.md').read()
req = get_req(name)
prog = get_compatible(name)


tmpl='''import setuptools
setuptools.setup(
    name="${name}",
    packages=["${name}"],
    version="$ver",
    license='MIT',
    description=$description,
    long_description=$long_description,
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/$name',
    keywords=$topics,
    python_requires='>=3.0',

    install_requires=$req,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + $prog,
)
'''

from string import Template
s = Template(tmpl)
rst = s.substitute(
        name=name,
        ver=ver,
        description=repr(description), 
        long_description=repr(long_description), 
        topics = repr(cfg['repository']['topics']), 
        req = repr(req),
        prog=repr(prog)
)
with open('setup.py', 'w') as f:
    f.write(rst)
