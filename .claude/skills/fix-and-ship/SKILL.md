---
name: fix-and-ship
description: Use when the user asks to fix an issue, create a PR, watch CI, and merge. Typically invoked as "fix N" referencing an issue file, with optional merge mode and CI actions URL.
---

# Fix and Ship

Fix an issue, push a PR, watch CI, merge to main, and clean up — all in one flow.

## Input

The user provides:
1. **Issue reference** — an issue file path or number (e.g., `fix 03` → `reviews/03-*.md`)
2. **Merge mode** — `squash`, `rebase` (default), or `merge`
3. **CI actions URL** — GitHub Actions URL to monitor (optional, auto-detected from remote)
4. **Post-merge cleanup** — whether to delete the issue file (default: yes)

## Process

### 1. Read the issue file

Glob for the issue file if a number is given (e.g., `03` → `reviews/03-*.md`). Read it to understand the fix needed: file, line, problem, and suggested fix.

### 2. Apply the fix

Edit the source file(s) as described in the issue. Keep changes minimal and focused.

### 3. Create branch, commit, push

```
git checkout -b fix/<slug-from-issue-filename>
git add <changed-files>
git commit  # use /git-commit skill for message
git push -u origin fix/<slug-from-issue-filename>
```

Branch name is derived from the issue filename (e.g., `03-download-stale-docstring` → `fix/download-stale-docstring`).

### 4. Create PR

```
gh pr create --title "<type>: <short description>" --body "$(cat <<'EOF'
## Summary
- <what changed and why>

## Test plan
- <how to verify>
EOF
)"
```

### 5. Watch CI

```
gh pr checks <PR#> --watch
```

- If **all checks pass**: proceed to merge.
- If **some checks fail**: inspect logs with `gh run view <run-id> --log-failed`. Distinguish flaky failures (Playwright screenshot, network timeouts) from real failures. If the PR-triggered run passed, flaky failures on the push-triggered run are acceptable.
- If **real failure**: fix, commit, push, and re-watch.

### 6. Merge

```
gh pr merge <PR#> --<mode> --delete-branch
```

Where `<mode>` is `squash`, `rebase`, or `merge`. If the repo disallows a mode (e.g., "Merge commits are not allowed"), fall back to the next mode: `merge` → `squash` → `rebase`.

### 7. Sync local

```
git checkout master && git pull --rebase origin master
```

Use the repo's default branch name (`master` or `main`).

### 8. Clean up (if requested)

Delete the issue file from disk:

```
rm <issue-file-path>
```

## Handling CI Failures

| Symptom | Action |
|---------|--------|
| Playwright screenshot error | Flaky — check if PR-triggered run passed; if so, proceed |
| Network timeout / external service | Flaky — same as above |
| Lint failure | Fix locally, commit, push, re-watch |
| Test assertion failure | Investigate — may indicate the fix is wrong |
| All runs fail same test | Real failure — fix before merging |
