# Bales — history

## Core Context

- **Project:** `martinopedal/opedal.tech` — personal site for Martin Opedal (Lead Cloud Solution Architect at Microsoft, Oslo).
- **Stack:** Astro 5 (static), GitHub dark palette in `src/styles/global.css`, JS-free.
- **Maintainer:** Martin Opedal (`martinopedal`).
- **My role:** CV HTML Page Specialist. I own `src/pages/cv.astro` and the `@media print` block in `global.css`.
- **My branch context:** working on `feat/cv-and-redesign` (PR B).

## What I know about the layout patterns

- **`BaseLayout.astro`** sets the CSP, the sitewide Person JSON-LD, the Permissions-Policy and Referrer-Policy meta tags (added in PR B commit 3), and exposes a `head-extra` slot for per-page schema additions.
- **`BlogLayout.astro`** is the canonical example of using `head-extra` to inject `<script type="application/ld+json">` for a per-page schema (Article in that case; ProfilePage in mine).
- **CSP is hard.** No `<style>` blocks in components — they will be silently blocked at runtime by `style-src 'self'`. All CSS goes in `src/styles/global.css`.
- **Existing palette:** `#0d1117` base, `#161b22` alt, `#2f81f7` accent. Reuse the existing CSS variables, don't redefine.

## What I know about the CV data

- **Source of truth:** `cv/data/architect.yml`. I read it in `cv.astro` frontmatter at build time using `js-yaml` (need to add to `dependencies`).
- **Schema:** `cv/README.md`. Top-level keys: `person`, `summary`, `experience`, `engagements`, `skills` (with `specializations`, `technical`, `competencies` sub-keys), `certifications`, `speaking`, `education`.
- **`appears_on` filter:** ignore on `/cv` — the HTML page shows everything. Aaron's LaTeX template filters by it.
- **Skills bars:** `level: 0.0–1.0`. Render as CSS-only bar via `style="--bar-fill: 40%"` and a `width: var(--bar-fill)` rule in `global.css`.

## Print stylesheet expectations

`@media print { ... }` block in `global.css`. Hide nav, hide footer, white background, black text, sensible page breaks (`break-before: page` on each `h2` after the first), remove backgrounds on cards/containers. Garman will print-preview `/cv` to verify.

## Learnings

(append as work progresses)
