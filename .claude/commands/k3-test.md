# k3-test: Test and Fix Package

Run tests for a k3 package, fix any issues, and commit the changes.

## Workflow

1. **Install the package in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run pytest and fix issues**
   ```bash
   python -m pytest -v
   ```
   - If any tests fail, analyze the failure and fix the code
   - If any warnings appear, fix them
   - Re-run pytest until all tests pass without warnings

3. **Run linting and fix issues**
   ```bash
   make lint
   ```
   - If linting fails, fix the issues
   - Re-run `make lint` until it passes

4. **Stage and commit changes**
   - Use `git status` to see all modified files
   - Use `git add <file>` for each modified file one by one
   - Use `/x-git-commit` to commit with an appropriate message

## Notes

- Focus on fixing the actual issues, not suppressing warnings
- If a test failure is a pre-existing issue unrelated to current work, note it but continue
- Run tests in the package directory (where pyproject.toml is located)
