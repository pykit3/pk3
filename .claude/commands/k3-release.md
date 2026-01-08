# Release Package

Automate the full release workflow: CI validation, version bump, tag, publish to PyPI, and open the package page.

## Process

1. **Push to CI branch and validate**
   - Push current branch to `ci` branch: `git push origin HEAD:ci -f`
   - Get the latest CI run ID for the `ci` branch
   - Watch the CI run until completion
   - If any CI job fails:
     - Analyze the failure logs
     - Fix the issue in the code
     - Commit the fix
     - Push to `ci` branch again
     - Watch the new CI run
     - Repeat until all CI jobs pass

2. **Push to master**
   - Push current branch to master: `git push origin HEAD:master`

3. **Bump version**
   - Read current version from `pyproject.toml`
   - Increment the patch version (e.g., 0.1.8 → 0.1.9)
   - Update `pyproject.toml` with the new version
   - Commit with message: `chore: bump version to X.Y.Z`

4. **Create and push tag**
   - Create tag: `git tag vX.Y.Z`
   - Push the commit to master: `git push origin master`
   - Push the tag: `git push origin vX.Y.Z`

5. **Watch publish workflow**
   - Find the "Upload Python Package" workflow run triggered by the tag
   - Watch until completion
   - If publish fails, report the failure

6. **Verify and open PyPI page**
   - Extract package name from `pyproject.toml`
   - Wait a few seconds for PyPI to update
   - Open the PyPI package page: `open https://pypi.org/project/{package_name}/{version}/`

## Notes

- Stop immediately if any step fails
- Report progress at each step
- The package name is read from `pyproject.toml` `[project]` section
