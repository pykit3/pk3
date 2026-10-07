**pykit3** is a collection of python3 modules that are loved by [s2][] developers.

| Name | Desc |
| :-- | :-- |
| [k3awssign][] | A python lib is used for adding aws version 4 signature to request. |
| [k3cacheable][] | Cache data which access frequently. |
| [k3cat][] | Just like nix command cat or tail, it continuously scan a file line by line. |
| [k3cgrouparch][] | This lib is used to set up cgroup directory tree according to configuration saved in zookeeper, and add pid to cgroup accordingly. |
| [k3color][] | create colored text on terminal |
| [k3confloader][] | k3confloader loads conf for other pykit3 modules |
| [k3daemonize][] | It supplies a command line interface API to start/stop/restart a daemon. |
| [k3dict][] | It provides with several dict operation functions. |
| [k3down2][] | convert markdown segment into easy to transfer media sucha images. |
| [k3etcd][] | A python client for Etcd https://github.com/coreos/etcd This module will only work correctly with the etcd server version 2.3.x or later. |
| [k3fmt][] | It provides with several string operation functions. |
| [k3fnmatch][] | Enhanced fnmatch with grouping regex and path transformation |
| [k3fs][] | File-system Utilities |
| [k3git][] | wrapper of git command-line |
| [k3handy][] | handy alias of mostly used functions |
| [k3heap][] | k3heap is a binary min heap implemented with reference |
| [k3http][] | We find that 'httplib' must work in blocking mode and it can not have a timeout when recving response. |
| [k3httpmultipart][] | This module provides some util methods to get multipart headers and body. |
| [k3jobq][] | k3jobq processes a series of inputs with functions concurrently |
| [k3kroki][] | Convert diagrams to images via the kroki.io API — zero local dependencies |
| [k3log][] | k3log is a collection of log utilities. |
| [k3logcollector][] | Scan log files on local machine, collector all interested logs, and send to somewhere for display. |
| [k3math][] | k3math is a toy math impl |
| [k3mime][] | This module provide some util methods to handle mime type. |
| [k3modutil][] | Submodule Utilities. |
| [k3net][] | Utility functions for network related operation. |
| [k3num][] | Convert number to human readable format in a string. |
| [k3pattern][] | Find common prefix of several `string`s, tuples of string, or other nested structure, recursively by default. |
| [k3portlock][] | k3protlock is a cross-process lock that is implemented with `tcp` port binding. |
| [k3priorityqueue][] | priorityQueue is a queue with priority support |
| [k3proc][] | easy to use `Popen` |
| [k3rangeset][] | segmented range which is represented in a list of sorted interleaving range. |
| [k3redisutil][] | For using redis more easily. |
| [k3shell][] | A python module to manage commands. |
| [k3stopwatch][] | StopWatch - library for adding timers and tags in your code for performance monitoring |
| [k3str][] | k3str is a collection of string utilities. |
| [k3thread][] | utility to create thread. |
| [k3time][] | Time convertion utils |
| [k3txutil][] | A collection of helper functions to implement transactional operations. |
| [k3ut][] | unittest util |
| [k3utdocker][] | unit test for python-docker |
| [k3utfjson][] | force `json.dump` and `json.load` in `utf-8` encoding. |
| [k3wsjobd][] | This module is a gevent based websocket server. When the server receives a job description from a client, it runs that job asynchronously in a thread, and reports the progress back to the client periodically. |
| [k3zkutil][] | Some helper function to make life easier with zookeeper. |


# Usage

Install a module by its name, e.g. `pip install k3proc`.

# Workspace

`pk3` is the workspace repo of pykit3. It holds:

- `pk3/`: the `pk3` command that every module's `Makefile` calls. It shows the
  version in `pyproject.toml` (`pk3 version`), creates the release tag
  (`pk3 tag`), uploads to PyPI (`pk3 publish`), and generates a module's
  `README.md` (`pk3 readme`). See [pk3/README.md](pk3/README.md).

- `.github/workflows/`: the CI and publish workflows that every module calls,
  and the daily `Workspace test`. `Workspace test` tests each module against
  the master of every k3 module it depends on.

- `scripts/`: workspace scripts. `multi-repo-*` scripts act on every module
  repo, `single-repo-*` scripts act on one repo, `workspace-*` scripts build
  this README, and `dev-*` scripts help with daily work.

- `packages/`: a clone of each module repo. Each one is its own git repo.

Set up the workspace:

```
git clone git@github.com:pykit3/pk3.git
cd pk3
pip install -e .                    # install the pk3 command
./scripts/multi-repo-clone-all.sh   # clone every module into packages/
```


# Development

## Engineering practices

- Start with the correctness requirements, ignore the performance impact until
  the end. You'll usually write something faster by focusing on keeping things
  minimal anyway.

- Throw away what can't be done in a day of coding. when you rewrite it
  tomorrow, it will be simpler.

- Write code for human.

    - Clarity comes first.
    - Then the correctness.
    - Then the performance(It is python, right?).

    You are a smart guy. But your colleagues may not
    be smart as you are.

    **Do not write smart codes**.

- Only write comment to explain **WHY**.
  Improve the code to explain **HOW** and **WHAT**.

## Developing workflow

Follow the github flow:

- Fork a repo
- Hacking on it
- Fire a pull request and then merge it to upstream.

    - Rebase to upstream master before open a PR to reduce conflict.

- Open an issue to describe what you gonna do before hacking on it:
    Let everybody else know what you are doing.




## Make changes to a module

- `github-action` is used for CI, such as  https://github.com/pykit3/k3proc/actions .
    The CI action is defined in `.github/workflows/python-package.yml`.
    Most of the time you do not need to modify this file unless **you know what
    you are doing**.

- Run the tests with `make test`, and format and lint the code with
  `make lint`. CI runs the tests on each Python version that the
  `Programming Language :: Python :: 3.X` classifiers in `pyproject.toml` list.

- Document is generated by [MkDocs](https://www.mkdocs.org/) from the
  docstrings.
  Python docstring follows [google docstring style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

  To build and test the doc: `make doc`.

- `README.md` of a module is generated. DO NOT MODIFY IT. `make readme`
  re-generates it from the module docstring in `__init__.py` and from the
  optional `synopsis.py` or `synopsis.txt`.

- Github meta data such as description and project labels are managed with
  `.github/settings.yml`. see https://github.com/pykit3/gh-config for detail.

- `pyproject.toml` defines the name, the version and the dependencies of a
  module. A version must be in [semantic-version][] syntax. `__init__.py`
  reads the version with `importlib.metadata`.

- Publish a module to `pip`:

    - Update `version` in `pyproject.toml`, e.g., to publish next version
        `0.2.14` of `k3proc`, set it to `"0.2.14"`.

    - Commit the version change and run `make release`.
        This step creates the tag `v0.2.14`. It refuses to run when the tree
        has uncommitted changes.

    - Push the tag with `git push --tags`. The tag triggers a github action
        that builds the package and uploads it to `pypi.org`.

    Then one can install the module(e.g. `k3proc`)
    with `pip install k3proc` or with version specified:
    `pip install k3proc==0.2.14`.

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the module layout and the
files that every module needs.


## Create a new module

- Clone [tmpl][], which is a template module, into `packages/tmpl`:
  `git clone git@github.com:pykit3/tmpl.git packages/tmpl`.

- Choose a good name that starts with `k3`, e.g. `k3whatever`, and create the
  module: `./scripts/dev-create-package.sh packages k3whatever`.
  The script copies the template, replaces its placeholder name, and makes the
  first commit.

- Create the repo `pykit3/k3whatever` on github, and push the module to it.

## Document

Write the `f**king` doc!

- Document the module, classes and methods.

## Testing

Write the `f**king` test!


[s2]: https://github.com/bsc-s2
[semantic-version]: https://semver.org/
[tmpl]: https://github.com/pykit3/tmpl

[k3awssign]: https://github.com/pykit3/k3awssign
[k3cacheable]: https://github.com/pykit3/k3cacheable
[k3cat]: https://github.com/pykit3/k3cat
[k3cgrouparch]: https://github.com/pykit3/k3cgrouparch
[k3color]: https://github.com/pykit3/k3color
[k3confloader]: https://github.com/pykit3/k3confloader
[k3daemonize]: https://github.com/pykit3/k3daemonize
[k3dict]: https://github.com/pykit3/k3dict
[k3down2]: https://github.com/pykit3/k3down2
[k3etcd]: https://github.com/pykit3/k3etcd
[k3fmt]: https://github.com/pykit3/k3fmt
[k3fnmatch]: https://github.com/pykit3/k3fnmatch
[k3fs]: https://github.com/pykit3/k3fs
[k3git]: https://github.com/pykit3/k3git
[k3handy]: https://github.com/pykit3/k3handy
[k3heap]: https://github.com/pykit3/k3heap
[k3http]: https://github.com/pykit3/k3http
[k3httpmultipart]: https://github.com/pykit3/k3httpmultipart
[k3jobq]: https://github.com/pykit3/k3jobq
[k3kroki]: https://github.com/pykit3/k3kroki
[k3log]: https://github.com/pykit3/k3log
[k3logcollector]: https://github.com/pykit3/k3logcollector
[k3math]: https://github.com/pykit3/k3math
[k3mime]: https://github.com/pykit3/k3mime
[k3modutil]: https://github.com/pykit3/k3modutil
[k3net]: https://github.com/pykit3/k3net
[k3num]: https://github.com/pykit3/k3num
[k3pattern]: https://github.com/pykit3/k3pattern
[k3portlock]: https://github.com/pykit3/k3portlock
[k3priorityqueue]: https://github.com/pykit3/k3priorityqueue
[k3proc]: https://github.com/pykit3/k3proc
[k3rangeset]: https://github.com/pykit3/k3rangeset
[k3redisutil]: https://github.com/pykit3/k3redisutil
[k3shell]: https://github.com/pykit3/k3shell
[k3stopwatch]: https://github.com/pykit3/k3stopwatch
[k3str]: https://github.com/pykit3/k3str
[k3thread]: https://github.com/pykit3/k3thread
[k3time]: https://github.com/pykit3/k3time
[k3txutil]: https://github.com/pykit3/k3txutil
[k3ut]: https://github.com/pykit3/k3ut
[k3utdocker]: https://github.com/pykit3/k3utdocker
[k3utfjson]: https://github.com/pykit3/k3utfjson
[k3wsjobd]: https://github.com/pykit3/k3wsjobd
[k3zkutil]: https://github.com/pykit3/k3zkutil