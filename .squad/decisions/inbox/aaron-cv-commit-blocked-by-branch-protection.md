# Decision: CV PDF commit strategy blocked by branch protection

**Date:** 2026-05-13  
**From:** Aaron (CV Pipeline Specialist)  
**To:** Coordinator

## Problem

The cv.yml workflow's commit-back strategy (git-auto-commit-action) is blocked by branch protection:

```
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - Changes must be made through a pull request.
error: failed to push some refs to 'https://github.com/martinopedal/opedal.tech'
```

Branch protection (verified via API):
- `required_pull_request_reviews.required_approving_review_count: 1`
- No bypass actors configured
- `enforce_admins: false`
- GitHub Actions bot token doesn't have bypass permission

## Current Architecture

**cv.yml (current design):**
1. `build` job: LaTeX install + PDF build → uploads artifacts
2. `commit` job: downloads artifacts → git-auto-commit-action pushes to main
3. **BLOCKED** at step 2 — can't push to protected main

**pages.yml (working):**
1. `build` job: Astro build (expects PDFs already in `public/cv/`)
2. `deploy` job: deploys `dist/` to GitHub Pages

## Options

### A. Add bypass actor for GitHub Actions (RECOMMENDED for current design)

Configure branch protection to allow `github-actions[bot]` to bypass PR requirement for automated commits:

```bash
gh api --method PUT repos/martinopedal/opedal.tech/branches/main/protection/required_pull_request_reviews \
  -f bypass_pull_request_allowances='{"apps": ["github-actions"]}'
```

**Pros:**
- Minimal workflow change (current design works)
- PDFs live in git history (versioned)
- cv.yml stays self-contained

**Cons:**
- Weakens branch protection for automated commits
- Every CV rebuild creates a commit to main

### B. Cross-workflow artifact consumption (ALTERNATIVE)

Have `pages.yml` download CV artifacts from the most recent successful `cv.yml` run and place them in `dist/cv/` after Astro build:

**cv.yml changes:**
- Drop `commit` job entirely
- Keep `build` job uploading artifacts

**pages.yml changes:**
- Add step after Astro build to download `cv-pdfs` artifact from last successful cv.yml run
- Copy PDFs into `dist/cv/` before Pages deploy

**Pros:**
- No commit-back needed (respects branch protection)
- PDFs don't bloat git history
- Separation of concerns (build vs deploy)

**Cons:**
- Cross-workflow artifact dependency (more complex)
- PDFs not versioned in git (ephemeral artifacts)
- Requires GitHub API call or action to fetch latest cv.yml artifact

### C. Manual PR for CV updates (current blocking workaround)

Keep current design but:
1. cv.yml runs on PR (builds + uploads artifacts for review)
2. **Manual merge** of PR triggers push event
3. Commit job runs but is blocked → someone manually pulls, commits PDFs, opens PR
4. PR gets approved → PDFs land in main → pages.yml deploys

**Pros:**
- No workflow change needed
- PDFs get PR review

**Cons:**
- Requires manual intervention every time
- Defeats automation goal

## Recommendation

**Option A** with a guardrail: configure bypass for `github-actions[bot]` but add a CODEOWNERS rule that requires approval for any `public/cv/*.pdf` change that comes from a human (not the bot). The bot can auto-commit, but humans must go through PR review.

Alternatively, if you want PDFs out of git history entirely, go with **Option B** (cross-workflow artifact fetch).

## Next Steps

Coordinator decision needed:
1. If A: I'll document the `gh api` command to add bypass actor (requires admin token)
2. If B: I'll refactor both cv.yml and pages.yml for artifact consumption
3. If C: Stop here, wait for manual workflow

---

**Current state:**
- PR #19 merged (workflow_dispatch + stable filename fixes)
- Run 25801320210 failed at commit step (branch protection)
- `public/cv/` still empty on main (404s persist)
