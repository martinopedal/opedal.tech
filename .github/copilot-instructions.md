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
  - `:root { color-scheme: dark; }` — locks native UI (scrollbars, form controls, focus rings) to the dark palette regardless of OS preference. The site is dark-only by design.
- **Accents (two-tone):**
  - `--color-accent: #d4a584` (peach — links at rest, primary accents)
  - `--color-accent-strong: #d97757` (terracotta — emphasis, link hover, focus rings, button hover, metrics, /work arrows, skip-link, eyebrows)
  - `--color-accent-glow: rgba(217, 119, 87, .15)` (warm radial halos, button glows, prose h2 separator)
- **Shadows:** `--shadow-warm-sm` and `--shadow-warm-md` are terracotta-tinted (no neutral grey shadows).
- **Type scale (single source of truth):** every body and heading size resolves to a token. Do *not* introduce ad-hoc rem literals for `font-size:` — round to the nearest step.
  - `--fs-xs: 0.78rem` (eyebrows, blog tags, cert kinds)
  - `--fs-sm: 0.92rem` (nav links, dates, body small, post-meta)
  - `--fs-base: 1rem` (body)
  - `--fs-md: 1.18rem` (hero tagline, cv-job h3, prose h3)
  - `--fs-lg: 1.5rem` (prose h2)
  - `--fs-xl: 2rem` (section h2)
  - `--fs-2xl: 2.75rem` (cv-header h1)
  - `--fs-3xl: 4rem` (hero name — cap on `clamp()`)
  - Line-height tokens: `--lh-tight: 1.15`, `--lh-snug: 1.35`, `--lh-base: 1.6`
- **Spacing scale (4px geometric):** `--space-1` (4px) … `--space-9` (96px). Use `--space-9` for desktop section padding and `--space-7` (48px) for mobile.
- **Reading measure:** long-form prose containers (`.post-content`, `.post-header`) cap at `var(--measure)` = 64ch. Do not use fixed pixel widths for blog post content.
- **Typography (faces):**
  - Body, About prose, hero tagline: system sans (`--font`)
  - JetBrains Mono (self-hosted, `/fonts/jetbrains-mono-variable.woff2`) for *all* technical labels and headings: nav links, dates, language pills, repo names, footer, `.eyebrow`, `.section-label`, `.cv-period`, `.cv-job h3`, hero `h1`, `.post-header h1`, `.prose h2`, `.prose h3`
  - `--font-mono` stack: `'JetBrains Mono', 'SFMono-Regular', Consolas, ...`
- **Eyebrows (`.eyebrow`, `.section-label`):** UPPERCASE, mono, `--fs-xs`, `letter-spacing: 0.12em`, color `--color-accent-strong`. Both share the same casing/color rules.
- **Do not** reintroduce a GitHub-blue accent (`#2f81f7`) or GitHub-grey surfaces (`#0d1117`, `#161b22`). The warm palette is the brand commitment.
- **Hero h1** is plain solid `--color-text` set in mono — no `linear-gradient` + `background-clip: text` tricks.
- **Hero signature texture:** `#hero::before` layers the `/dot-grid.svg` pattern (24×24 tile, single 1.25px peach circle at 8% opacity) masked with a radial gradient so dots are densest near the upper-center and fade at the edges. Keep it; it's the visual signature.
- **Links (default `a`):** thin (1px) terracotta-tinted underline at 3px offset; hover thickens to 2px and shifts color from peach to terracotta. Structural surfaces (nav, cards, buttons, footer) opt out via the explicit selector list at the top of `global.css`.
- **Focus-visible:** 2px solid `--color-accent-strong` outline, 3px offset, 2px border-radius. Distinct from link rest color.
- **Card hover lift** (`.repo-row`, `.blog-card`, `.work-row`): 2px `translateY` + `--color-elevated` background + `--shadow-warm-md`. Property-scoped transitions, cancelled by `prefers-reduced-motion: reduce`.
- **Magnetic primary button** (`.btn-primary`): 1px lift + warm glow + 1px inset terracotta ring on hover, only inside `@media (prefers-reduced-motion: no-preference)`.
- **Section atmosphere alternation** on the homepage: `#hero` (radial halo + dot-grid), `#about` (bg), `#work` (surface), `#oss` (bg + inset accent line), `#speaking` (surface).
- **Section padding:** `var(--space-9) 0` desktop, `var(--space-7) 0` mobile. Mobile override lives inside `@media (max-width: 700px)` covering `section`, `.work-page`, `#hero`, `.blog-hero`, `.cv-page`.
- **Blog content (`.prose`):** body `--text` color (not muted), font-size 17px, line-height 1.75. `h2` is a mono heading with a thin `--color-accent-glow` rule above (no border-bottom). Inline `code` sits on `--color-elevated` in terracotta with no border. `pre` blocks have a 2px terracotta left-stripe.
- Responsive: mobile-first, CSS-only hamburger nav on mobile (mobile dropdown is fully opaque `var(--color-surface)`).
- No external fonts, no CDN dependencies — fully self-contained for speed.
- All images must have `alt` attributes.
- Eyebrow text must add a category and never echo the H2 word-for-word.
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
