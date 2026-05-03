# Copilot Instructions — opedal.tech

## Repository Purpose

Personal website for Martin Opedal (opedal.tech), hosted on GitHub Pages.
Built with **Astro** (static output) — Markdown-authored blog, component-based pages, zero client-side JS.

## Stack

- **Framework**: Astro (static output, `npm run build` → `dist/`)
- **Content**: Markdown blog posts in `src/content/blog/`
- **Styles**: Plain CSS in `src/styles/global.css` (GitHub dark palette)
- **Hosted**: GitHub Pages, deployed via `.github/workflows/pages.yml`
- **Custom domain**: `opedal.tech` (CNAME file present)
- **Node version**: 22 (in CI via `actions/setup-node`)

## File structure

```
src/
  components/   — Astro components (Nav, Hero, About, Work, OpenSource, Speaking, Contact)
  content/
    blog/       — Markdown blog posts (.md files)
    config.ts   — Content collection schema
  layouts/      — BaseLayout.astro, BlogLayout.astro
  pages/        — index.astro, blog/index.astro, blog/[...slug].astro, rss.xml.js
  styles/       — global.css
public/         — Static assets (favicon.svg, og images)
```

## Adding a blog post

Create `src/content/blog/my-post.md` with frontmatter:
```md
---
title: "Post title"
description: "One-sentence description"
pubDate: 2025-06-01
tags: ["Azure", "Terraform"]
---
```

## Branch protection

- Signed commits NOT required (breaks Dependabot and GitHub API commits)
- 0 required reviewers (solo-maintained)
- `enforce_admins = true`, linear history, no force push
- Required status checks: `Analyze (actions)` (CodeQL) and `Build Astro site`

## CodeQL policy

- Scans GitHub Actions workflows only — `language: [actions]`
- Astro/TypeScript/CSS do not have a CodeQL extractor — this is expected

## SHA-pinning

- All GitHub Actions MUST use SHA-pinned versions, not tags
- Example: `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6`

## GitHub Pages

- Source: GitHub Actions (workflow builds `dist/` and deploys)
- Custom domain configured in `CNAME` file and in repo Settings → Pages
- HTTPS enforced — never link to HTTP resources
- Deploy workflow: `.github/workflows/pages.yml`

## Design rules

- Color scheme: dark (#0d1117 base, #161b22 alt — GitHub dark palette)
- Accent: `#2f81f7` (GitHub blue)
- Responsive: mobile-first, CSS-only hamburger nav on mobile
- No external fonts, no CDN dependencies — fully self-contained for speed
- All images must have `alt` attributes
- `prefers-reduced-motion` respected — transitions disabled for users who prefer it

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
- CSP enforced via `<meta http-equiv="Content-Security-Policy">` in BaseLayout — no inline scripts permitted
- No `define:vars` usage in Astro components (would require loosening CSP)

## GitHub-first principle

Validate changes in GitHub Actions, not locally. Push, trigger workflow, check logs, iterate.
