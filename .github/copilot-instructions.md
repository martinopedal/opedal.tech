# Copilot Instructions — opedal.tech

## Repository Purpose

Personal website for Martin Opedal (opedal.tech), hosted on GitHub Pages.
Built with **Astro** (static output) — Markdown-authored blog, component-based pages, zero client-side JS.

## Stack

- **Framework**: Astro (static output, `npm run build` → `dist/`)
- **Content**: Markdown blog posts in `src/content/blog/`
- **Styles**: Plain CSS in `src/styles/global.css` (warm earth — Architect Charcoal palette)
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

- **Color scheme: warm earth dark** (Architect Charcoal — *not* GitHub blue)
  - `--color-bg: #14110f` (warm near-black base)
  - `--color-surface: #1c1814` (card resting)
  - `--color-elevated: #261f19` (card hover/active)
- **Accents (two-tone):**
  - `--color-accent: #d4a584` (peach — links, focus rings, primary accents)
  - `--color-accent-strong: #d97757` (terracotta — emphasis, button hover, metrics, /work arrows, skip-link)
  - `--color-accent-glow: rgba(217, 119, 87, .15)` (warm radial halos, button glows)
- **Shadows:** `--shadow-warm-sm` and `--shadow-warm-md` are terracotta-tinted (no neutral grey shadows).
- **Typography:**
  - Body, About prose, hero tagline, h2/h3 headings: system sans (`--font`)
  - JetBrains Mono (self-hosted, `/fonts/jetbrains-mono-variable.woff2`) for *all* technical labels: nav links, dates, language pills, repo names, footer, `.section-label`, `.cv-period`, `.cv-job h3`, hero `h1` name treatment
  - `--font-mono` stack: `'JetBrains Mono', 'SFMono-Regular', Consolas, ...`
- **Do not** reintroduce a GitHub-blue accent (`#2f81f7`) or GitHub-grey surfaces (`#0d1117`, `#161b22`). The warm palette is the brand commitment, locked in by `feat/design-stepup`.
- **Hero h1** is plain solid `--color-text` set in mono — no `linear-gradient` + `background-clip: text` tricks.
- **Card hover lift** (`.repo-row`, `.blog-card`, `.work-row`): 2px `translateY` + `--color-elevated` background + `--shadow-warm-md`. Property-scoped transitions, cancelled by `prefers-reduced-motion: reduce`.
- **Magnetic primary button** (`.btn-primary`): 1px lift + warm glow + 1px inset terracotta ring on hover, only inside `@media (prefers-reduced-motion: no-preference)`.
- **Section atmosphere alternation** on the homepage: `#hero` (radial halo), `#about` (bg), `#work` (surface), `#oss` (bg + inset accent line), `#speaking` (surface).
- Responsive: mobile-first, CSS-only hamburger nav on mobile (mobile dropdown is fully opaque `var(--color-surface)`).
- No external fonts, no CDN dependencies — fully self-contained for speed.
- All images must have `alt` attributes.
- Eyebrow (`.section-label`) text must add a category and never echo the H2 word-for-word.
- All new colors go through CSS variables — no magic hex literals scattered through the code.
- `prefers-reduced-motion` respected — transitions and hover lifts disabled for users who prefer it.

## Content rules

- Keep bio text accurate and current
- Repo stats (stars, forks) can drift — update quarterly or when significant
- No customer names or confidential engagement details
- No secrets in HTML source (no API keys, tokens, tracking pixels)

## Issue conventions

- Use labels `enhancement`, `bug`, `content`, `chore`, `documentation`, `dependencies`
- Issue titles: `feat:`, `fix:`, `content:`, `chore:` prefix convention
- The `copilot` label assigns an issue to the GitHub Copilot coding agent

## Security rules

- No secrets in code — use GitHub Secrets for any future workflow secrets
- SHA-pin all GitHub Actions
- No third-party analytics scripts that collect PII
- CSP enforced via `<meta http-equiv="Content-Security-Policy">` in BaseLayout — no inline scripts permitted
- No `define:vars` usage in Astro components (would require loosening CSP)
- **No `<style>` blocks in `.astro` components.** The CSP sets `style-src 'self'` with no `'unsafe-inline'`, so Astro's scoped `<style>` blocks (which become inline `<style>` tags in the head) are blocked at runtime. Add styles to `src/styles/global.css` instead.
- **No `<script>` blocks in `.astro` components** (same reason — `script-src 'none'`). The site is intentionally JS-free.
- **JSON-LD is fine**: `<script type="application/ld+json">` blocks are CSP-exempt because they're parsed as data, not executable script. Used in `BaseLayout.astro` for the Person schema and in `BlogLayout.astro` for Article schema.
- **External link hygiene**: every `target="_blank"` link must have `rel="noopener noreferrer"`.

## SEO baseline

- Every page passes `title` + `description` to `BaseLayout`. Descriptions should read as a real sentence, 120–160 chars, with the Microsoft-anchored title appearing somewhere on the homepage.
- Blog post pages use `BlogLayout`, which sets `ogType="article"` and emits an `Article` JSON-LD block alongside the sitewide `Person` schema.
- Sitemap is generated by `@astrojs/sitemap` (configured in `astro.config.mjs`); `public/robots.txt` declares it.

## GitHub-first principle

Validate changes in GitHub Actions, not locally. Push, trigger workflow, check logs, iterate.
