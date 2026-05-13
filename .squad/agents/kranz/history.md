# Kranz — history

## Core Context

- **Project:** `martinopedal/opedal.tech` — personal site for Martin Opedal (Lead Cloud Solution Architect at Microsoft, Oslo).
- **Stack:** Astro 5 (static), GitHub dark palette in `src/styles/global.css`, JS-free, system fonts in body.
- **Maintainer:** Martin Opedal (`martinopedal`).
- **My role:** Site Redesign Specialist. I own the visual reshape across `Hero`, `OpenSource`, `Work`, `Speaking`, `Contact`, `Nav`, `About`, `index.astro`, and the bulk of `global.css`.
- **My branch context:** working on `feat/cv-and-redesign` (PR B).

## What I know about the design baseline

- **CSP is hard:** no `<style>` blocks in any `.astro` component. CSS goes in `src/styles/global.css`. Read the existing 693 lines before adding anything.
- **Palette:** `#0d1117` base, `#161b22` alt, `#2f81f7` accent. Hero name gradient `#2f81f7 → #58a6ff` is the only gradient on the site; reserve it.
- **`prefers-reduced-motion: reduce`** is already respected in existing CSS — keep that pattern in any new animation.
- **Mobile-first** with a CSS-only hamburger nav. Nav.astro carries the implementation; preserve it.

## What was decided in the 3-model review (Opus 4.7 + GPT-5.5 + Sonnet 4.6 consensus)

Locked in `.squad/decisions.md`. Highlights I act on:

- KEEP `Lead Cloud Solution Architect · Microsoft` eyebrow on hero.
- Primary CTA `View open source` → `/work` (or `#open-source`). Secondary `Email me` → `mailto:hello@opedal.tech`.
- KEEP small/subtle name gradient.
- DROP emoji on Work/OpenSource/Speaking. Do NOT replace with Octicons.
- OpenSource: grouped annotated rows by problem domain. No star counts. 2px coloured left border per language extending `.repo-lang.{terraform,python,powershell}` pattern.
- Work (homepage): trim to 4 highlights with proof links to `/work`. Lovell owns the full evidence rows on `/work`.
- Section markers: thin mono labels and a thin accent rule under each `h2`.
- Speaking: one line + link.
- Contact: add `hello@opedal.tech` button.
- Nav: add `/cv` and `/work` links.

## What I do NOT touch

- `src/pages/cv.astro` — Bales.
- `src/pages/work.astro` — Lovell.
- `cv/`, `.github/workflows/`, `public/fonts/`, `BaseLayout.astro`.

## Learnings

### Base path routing helper (2026-05-13)

**Problem:** Astro's `base` path is env-driven (`GITHUB_PAGES_BASE_PATH` set by `actions/configure-pages`). When deploying to github.io preview (`/opedal.tech/`), absolute internal links like `href="/cv"` bypassed the base and 404'd. When DNS cuts over (apex domain), base flips to `/` and the same absolute hrefs work again — but the site must render correctly in BOTH environments.

**Solution:** Created `src/utils/link.ts` with a helper function:
```ts
export function link(path: string): string {
  if (path.startsWith('#')) return path; // Anchor-only, no base
  const base = import.meta.env.BASE_URL; // Trailing-slashed by Astro
  const clean = path.replace(/^\//, '');
  return `${base}${clean}`;
}
```

Usage pattern: `<a href={link('cv')}>CV</a>` (no leading slash). Anchor-only paths (`#contact`) pass through unchanged.

**Verification:**
- Build with `GITHUB_PAGES_BASE_PATH=/opedal.tech/`: `dist/index.html` shows `<a href="/opedal.tech/cv">`, `<a href="/opedal.tech/blog">`, `<a href="/opedal.tech/work">`.
- Build without env var (default `/`): `dist/index.html` shows `<a href="/cv">`, `<a href="/blog">`, `<a href="/work">`.
- Grep verification: `Get-Content dist\index.html | Select-String -Pattern 'href="(?:/opedal\.tech)?/(cv|work|blog)(?:#[^"]*)?"|href="/opedal\.tech/"'`

**Applied to:**
- `Nav.astro`, `Hero.astro`, `Work.astro` (homepage component), `blog/index.astro`, `BlogLayout.astro`, `cv.astro`.

**Boundary:** Did NOT touch `src/pages/work.astro` (Lovell's surface). That page has two broken absolute links: `href="/blog/azure-landing-zones-2025/"` and `href="/blog/building-with-github-copilot/"`. Lovell will need to import and apply the same helper.

### WCAG AA contrast fixes (2026-05-13)

**Problem:** User feedback: "colors hard to read". Reed's contrast audit revealed one AA failure (`.btn-primary` white-on-terracotta at 3.12:1) and `--color-text-dim` hovering just below AAA on `--color-surface`.

**Solution:** Three surgical CSS token fixes in `src/styles/global.css`:

1. **Token bump (line 17):** `--color-text-dim: #a39d92;` → `--color-text-dim: #ada79d;`  
   Achieves AAA (7:1+) on both `--color-bg` and `--color-surface`. Minimal luminance bump, preserves warm taupe character.

2. **CTA legibility fix (lines 218, 225):** `.btn-primary` and `.btn-primary:hover` changed from `color: #fff;` → `color: var(--color-bg);`  
   Dark warm brown on terracotta = 6.02:1 contrast (passes AA). Maintains Architect Charcoal aesthetic (dark-on-terracotta = classic warm palette).

3. **Mobile nav polish (line 724):** Mobile nav dropdown background `rgba(13, 17, 23, 0.98)` → `rgba(20, 17, 15, 0.98)`  
   Matches new `--color-bg` (#14110f) instead of legacy GitHub dark. Visual consistency fix.

**Contrast ratios post-fix:**
- `--color-text-dim` on `--color-bg`: 7.87:1 (AAA ✅)
- `--color-text-dim` on `--color-surface`: 7.16:1 (AAA ✅)
- `.btn-primary` dark text on terracotta: 6.02:1 (AA ✅)

**Pattern:** When bumping token luminance for legibility, target AAA on both background surfaces (base and alt) while preserving hue/warmth character. For CTAs on accent backgrounds, prefer dark text over white for WCAG compliance when the accent is mid-tone.

(append as work progresses)
