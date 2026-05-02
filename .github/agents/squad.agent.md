# Squad Agent — opedal.tech

## Purpose

This is the squad orchestration agent for the `martinopedal/opedal.tech` personal website.
The squad coordinates GitHub Copilot coding agent tasks for building and maintaining the site.

## Scope

- Personal website for Martin Opedal at opedal.tech
- Stack: static HTML + CSS, GitHub Pages, GitHub Actions CI
- No build system, no npm, no Jekyll — plain HTML/CSS/vanilla JS

---

## Squad Members

| Role | Agent / Person | Responsibility |
|------|---------------|----------------|
| **Maintainer** | @martinopedal | Approves and merges all PRs. Final authority on content and design. |
| **Copilot Coding Agent** | copilot-swe-agent[bot] | Implements issues labelled `copilot`. Opens draft PRs. |
| **Copilot Code Reviewer** | copilot-pull-request-reviewer | Reviews every PR. All review threads must be resolved before merge. |

---

## Issue Labels

| Label | Meaning |
|-------|---------|
| `squad` | Auto-added to every issue. Required for squad dispatch. |
| `copilot` | Assigned to GitHub Copilot coding agent for implementation. |
| `enhancement` | New feature or section for the site. |
| `content` | Text/copy update — bio, repos list, speaking entries. |
| `bug` | Something broken on the site. |
| `chore` | Dependency update, workflow fix, CI maintenance. |
| `documentation` | README or docs update. |

---

## Workflow

### New issue → Copilot agent

1. Open an issue with the `copilot` label (auto-label workflow adds `squad` automatically).
2. GitHub Copilot coding agent picks it up and opens a draft PR.
3. `copilot-agent-pr-review.yml` automatically requests Copilot code review on PR open.
4. Copilot review results enter the **Comment Triage Loop** (below).
5. Maintainer reviews, approves, and merges when all checks are green.

### Comment Triage Loop

Every Copilot review comment on a PR must be:
- **Addressed** with a code change (push the fix, reply with the commit SHA), OR
- **Rejected** with an explicit explanation of why it does not apply.

Do not merge until all review threads are **Resolved**.

---

## CI Checks (required green before merge)

| Check | Workflow |
|-------|----------|
| `Analyze (actions)` | `codeql.yml` — CodeQL on GitHub Actions workflows |
| `Deploy to GitHub Pages` | `pages.yml` — validates and deploys the static site |

---

## Branch Protection (configure via Settings → Branches → main)

```
Branch: main
✅ Require a pull request before merging
   - Required approving reviews: 0 (solo-maintained)
✅ Require status checks to pass before merging
   - Required: Analyze (actions)
✅ Require linear history (no merge commits)
✅ Include administrators (enforce_admins = true)
❌ Require signed commits (breaks Dependabot / API commits)
❌ Allow force pushes
❌ Allow deletions
```

---

## Pages Deployment

- Source: `main` branch, root (`/`)
- Custom domain: `opedal.tech`
- HTTPS: enforced
- Deploy triggered on push to `main`

---

## Content update pattern

For content-only changes (bio text, repo list, speaking entries):

1. Open a `content:` issue with label `content` + `squad`
2. Assign to `copilot` or implement directly
3. PR must still pass CI before merge

---

## Resilience Contract

A PR is "done" only when it is **green AND merged**.

- CI red → fetch failed-job logs, fix root cause, push, re-check
- Copilot rejection → Comment Triage Loop until all threads resolved
- Merge conflict → rebase on `main`, `git push --force-with-lease`

Never abandon a branch without closing the PR and explaining why.

---

## Security Invariants

- No secrets in HTML source
- No inline JavaScript event handlers (use `addEventListener`)
- No third-party analytics that collect PII
- All outbound links: `target="_blank" rel="noopener"`
- HTTPS only — never reference HTTP resources
- SHA-pin all GitHub Actions

---

## Handoff to Maintainer

When the Copilot agent opens a PR:
1. The PR description must reference the closing issue (`Closes #N`)
2. The PR must be ready for review (not draft) before maintainer review
3. All Copilot review threads must be resolved
4. `Analyze (actions)` check must be green
5. Maintainer approves and squash-merges with a descriptive commit message
