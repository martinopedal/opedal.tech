# Copilot Instructions — opedal.tech

## Repository Purpose

Personal website for Martin Opedal (opedal.tech), hosted on GitHub Pages.
Static HTML/CSS — no build system, no npm, no Jekyll. Just clean, fast HTML.

## Stack

- Static HTML (`index.html`) + CSS (`assets/css/style.css`)
- Hosted on GitHub Pages from `main` branch root
- Custom domain: `opedal.tech` (CNAME file present)
- No JavaScript frameworks — vanilla JS only where needed

## Branch protection

- Signed commits NOT required (breaks Dependabot and GitHub API commits)
- 0 required reviewers (solo-maintained)
- `enforce_admins = true`, linear history, no force push
- Required status checks: `Analyze (actions)` (CodeQL)

## CodeQL policy

- Scans GitHub Actions workflows only — `language: [actions]`
- HTML/CSS do not have a CodeQL extractor — this is expected

## SHA-pinning

- All GitHub Actions MUST use SHA-pinned versions, not tags
- Example: `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6`

## GitHub Pages

- Source: `main` branch, root (`/`)
- Custom domain configured in `CNAME` file and in repo Settings → Pages
- HTTPS enforced — never link to HTTP resources
- Deploy workflow: `.github/workflows/pages.yml`

## Design rules

- Color scheme: dark (#0d1117 base, #161b22 alt — GitHub dark palette)
- Accent: `#2f81f7` (GitHub blue)
- Responsive: mobile-first, nav collapses on narrow screens
- No external fonts, no CDN dependencies — fully self-contained for speed
- All images must have `alt` attributes

## Content rules

- Keep bio text accurate and current
- Repo stats (stars, forks) can drift — update quarterly or when significant
- No customer names or confidential engagement details
- No secrets in HTML source (no API keys, tokens, tracking pixels)

## Squad integration

- Issues are auto-labelled with `squad` on open
- Use labels `enhancement`, `bug`, `content`, `chore` alongside `squad`
- Issue titles: `feat:`, `fix:`, `content:`, `chore:` prefix convention
- The `copilot` label assigns an issue to GitHub Copilot coding agent

## Security rules

- No secrets in code — use GitHub Secrets for any future workflow secrets
- SHA-pin all GitHub Actions
- No third-party analytics scripts that collect PII
- CSP: avoid inline event handlers; use `defer` script loading

## GitHub-first principle

Validate changes in GitHub Actions, not locally. Push, trigger workflow, check logs, iterate.
