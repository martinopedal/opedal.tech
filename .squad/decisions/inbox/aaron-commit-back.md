# Decision: Commit-back strategy for CV PDFs

**By:** Aaron (CV Pipeline Specialist)  
**Date:** 2026-05-13  
**Context:** PR B — CV pipeline

## What

`.github/workflows/cv.yml` commits built PDFs back to the `main` branch via `stefanzweifel/git-auto-commit-action@b863ae1933cb653a53c021fe36dbb774e1fb9403 # v5`.

**Key characteristics:**
- PDFs are generated artifacts, but committed to the repo (not uploaded separately).
- The commit-back happens in a dedicated `commit` job (not the `build` job).
- The `commit` job declares `permissions: contents: write` at the job level (not the workflow level).
- The workflow has a concurrency group (`cv-${{ github.ref }}`) to prevent simultaneous builds on the same ref from conflicting.

**File pattern:** `public/cv/architect-*.pdf`

**Commit message:**
```
chore(cv): rebuild architect PDFs

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

## Why

**Why commit PDFs instead of GitHub Releases or artifact upload:**
- The PDFs must be available at `/cv/architect-1page.pdf` and `/cv/architect-multipage.pdf` on the deployed site.
- GitHub Pages serves `public/` as the site root — the PDFs need to be in the repo at deploy time.
- Releases are for versioned distributions, not per-push builds.
- Artifacts expire (max 90 days); we want the PDFs to persist indefinitely.

**Why a separate `commit` job:**
- Keeps the `build` job read-only (principle of least privilege).
- The `build` job runs on both PRs and pushes; the `commit` job runs only on push to `main`.
- Cleaner to scope `contents: write` to a single job that does nothing else.

**Why `stefanzweifel/git-auto-commit-action`:**
- Handles git add, commit, and push in one step.
- Skips the commit if no changes (idempotent).
- Widely used (7.4k stars), actively maintained, SHA-pinned.

**Why the concurrency group:**
- If two commits to `main` touch `cv/**` in quick succession, the first build completes and commits PDFs. The second build starts before the first's commit is pulled. Without concurrency control, the second build would conflict on push. The concurrency group cancels the second build, which will re-trigger after the first completes (because the first's commit also touches `cv/**`).

## Alternatives considered

- **Manual commit:** fragile, requires `git config`, error-prone.
- **GitHub Releases:** wrong abstraction — releases are for versioned artifacts, not per-push rebuilds.
- **Artifact upload only:** PDFs wouldn't be available on the deployed site.

## Scope

This decision applies to `.github/workflows/cv.yml`. If a future pipeline needs to commit generated files back (e.g., auto-generated diagrams, minified assets), the same pattern should be used: separate job, scoped write permission, concurrency group, and `git-auto-commit-action`.

## SHA verification

- **Action:** `stefanzweifel/git-auto-commit-action`
- **Tag:** `v5`
- **SHA:** `b863ae1933cb653a53c021fe36dbb774e1fb9403` (verified via `gh api repos/stefanzweifel/git-auto-commit-action/commits/v5 --jq .sha` on 2026-05-13)
