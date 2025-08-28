# pykit3

Collection of Python 3 utility modules.

| Module | Description |
| :-- | :-- |
| [k3color][] | Terminal text coloring |
| [k3confloader][] | Configuration loader |
| [k3dict][] | Dictionary operations |
| [k3down2][] | Markdown to media converter |
| [k3fmt][] | String formatting utilities |
| [k3fs][] | File system utilities |
| [k3git][] | Git command wrapper |
| [k3handy][] | Common function aliases |
| [k3heap][] | Binary min heap |
| [k3jobq][] | Concurrent job processor |
| [k3log][] | Logging utilities |
| [k3math][] | Math implementations |
| [k3net][] | Network utilities |
| [k3num][] | Human-readable numbers |
| [k3pattern][] | Pattern matching |
| [k3portlock][] | TCP port-based locks |
| [k3priorityqueue][] | Priority queue |
| [k3proc][] | Process utilities |
| [k3rangeset][] | Range operations |
| [k3shell][] | Shell command management |
| [k3str][] | String utilities |
| [k3thread][] | Thread utilities |
| [k3time][] | Time conversion |
| [k3txutil][] | Transaction helpers |
| [k3ut][] | Unit test utilities |

This repository manages the pykit3 module collection.


# Development

## Engineering Principles

- **Clarity first**: Write code for humans, prioritize readability
- **Correctness over performance**: Focus on getting it right first  
- **Simplicity**: Throw away what can't be done in a day, rewrite simpler tomorrow
- **No smart code**: Write straightforward, maintainable code
- **Comment WHY, not HOW**: Let code explain itself

## Workflow

1. Fork repository
2. Create feature branch  
3. Implement changes
4. Open pull request with rebase to main




## Module Development

### Setup
- CI: GitHub Actions (`.github/workflows/python-package.yml`)
- Testing: `pytest` framework
- Documentation: Sphinx with [Google docstring style](https://www.sphinx-doc.org/en/1.5/ext/example_google.html)
- Build docs: `make doc`

### Module Structure
- `__init__.py` must define `__name__` and `__version__` ([semantic versioning](https://semver.org/))
- GitHub metadata managed via `.github/settings.yml`

### Publishing
1. Update `__version__` in `__init__.py`
2. Commit and run `make build_setup_py`
3. Push tag to trigger PyPI upload via GitHub Actions


## Directory Structure

```
k3module/
├── .github/workflows/    # CI/CD configurations
├── _building/           # Build utilities  
├── docs/               # Sphinx documentation
├── test/               # Unit tests
├── __init__.py        # Module metadata and exports
├── main_module.py     # Primary implementation
├── LICENSE
├── Makefile          # Build commands
├── README.md         # Auto-generated, do not edit
├── requirements.txt  # Dependencies
└── setup.py         # Auto-generated for releases
```

Key files:
- `docs/source/index.rst`: Update for new APIs
- `README.md`: Generated via `make readme`
- `setup.py`: Generated via `make build_setup_py`


## Creating New Modules

1. Fork from [tmpl][] (template repository)
2. Choose name starting with `k3`
3. Clone: `git clone git@github.com:pykit3/k3newmodule.git`
4. Generate skeleton: `python ./_building/populate.py`

## Template Updates

- Populate it: `python ./_building/populate.py`.
    This step generates a skeleton of a module:
    ```
    python ./_building/populate.py
    git status
    ...
        new file：   .github/settings.yml
        new file：   __init__.py
        new file：   docs/source/index.rst
        new file：   package.json
        new file：   packages.txt
        new file：   requirements.txt
        new file：   test-requirements.txt
        new file：   test/test_doctest.py
        new file：   test/test_k3whatever.py
    ```

    Examine the generated files and add them and make your first commit!

## Update tmpl changes

`applytmpl.sh` copies changes from repo `tmpl` to current dir.
It should be run in a repo dir, e.g., `k3zkutil`:
```
./tmpl
./k3zkutil
```

To apply tmlp chagnes to every repo:
```
run-script-in-repos.sh repo-apply-tmpl.sh
```

## Documentation & Testing

- Document all modules, classes, and methods
- Write comprehensive tests


[s2]: https://github.com/bsc-s2
[semantic-version]: https://semver.org/
[tmpl]: https://github.com/pykit3/tmpl

[k3color]: https://github.com/pykit3/k3color
[k3confloader]: https://github.com/pykit3/k3confloader
[k3dict]: https://github.com/pykit3/k3dict
[k3down2]: https://github.com/pykit3/k3down2
[k3fmt]: https://github.com/pykit3/k3fmt
[k3fs]: https://github.com/pykit3/k3fs
[k3git]: https://github.com/pykit3/k3git
[k3handy]: https://github.com/pykit3/k3handy
[k3heap]: https://github.com/pykit3/k3heap
[k3jobq]: https://github.com/pykit3/k3jobq
[k3log]: https://github.com/pykit3/k3log
[k3math]: https://github.com/pykit3/k3math
[k3net]: https://github.com/pykit3/k3net
[k3num]: https://github.com/pykit3/k3num
[k3pattern]: https://github.com/pykit3/k3pattern
[k3portlock]: https://github.com/pykit3/k3portlock
[k3priorityqueue]: https://github.com/pykit3/k3priorityqueue
[k3proc]: https://github.com/pykit3/k3proc
[k3rangeset]: https://github.com/pykit3/k3rangeset
[k3shell]: https://github.com/pykit3/k3shell
[k3str]: https://github.com/pykit3/k3str
[k3thread]: https://github.com/pykit3/k3thread
[k3time]: https://github.com/pykit3/k3time
[k3txutil]: https://github.com/pykit3/k3txutil
[k3ut]: https://github.com/pykit3/k3ut
