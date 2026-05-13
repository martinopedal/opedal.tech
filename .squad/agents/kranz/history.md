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

(append as work progresses)
