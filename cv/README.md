# `cv/` — same-repo CV pipeline

This directory holds the source of truth for the Architect CV in three forms:

1. **LaTeX → PDF** — `cv/build.py` reads `cv/data/architect.yml`, renders
   `cv/templates/architect.tex.j2` for both 1-page and multi-page variants, and
   compiles each via `latexmk` into `public/cv/architect-{1page,multipage}.pdf`.
2. **HTML page** — `src/pages/cv.astro` reads `cv/data/architect.yml` at build
   time and renders the `/cv` route directly. Same data, different output.
3. **CI workflow** — `.github/workflows/cv.yml` runs the LaTeX build on `cv/**`
   changes, uploads PDFs as artifacts on PRs, and commits them back to `main`
   on push so the GitHub Pages deploy job picks them up.

## Layout

```
cv/
  README.md                   ← this file
  architect/                  ← assets needed by LaTeX (vendored from latex-ninja/hipster-cv, MIT)
    hipstercv.cls
    hipstercv.sty
    photo.jpg
  data/
    architect.yml             ← single source of truth (sanitized; review before commit)
  templates/
    architect.tex.j2          ← Jinja2 template; renders 1page or multipage by mode
  build.py                    ← YAML → .tex (both variants) → .pdf via latexmk
```

## Data redaction rules — HARD

`cv/data/architect.yml` ships in a public repo and is consumed by both the
PDF build and the HTML page. The following rules are non-negotiable.

| Class | Rule |
|-------|------|
| Phone numbers | Never. Phone is permanently removed from the CV. |
| Real customer names | Never. Use sector + scale (e.g. "Tier-1 Nordic Bank"). |
| Email | `hello@opedal.tech` only — the public alias forwarded by Domeneshop. The underlying inbox address is private. |
| Microsoft-internal Connect-style phrasing | Never. No "revenue contributor", "pipeline ownership", "multi-million dollar targets", "consumption growth" as a deliverable, or rating language. Use neutral industry phrasing. |
| Codenames | Never. Public product names only. |
| Tracked metrics that are real and defensible | Allowed when anonymized at sector level (e.g. "48M+ NOK consultant portfolio", "94% NIC approval"). |

If you are unsure, leave it out.

## Schema overview

`architect.yml` has these top-level keys:

| Key | Shape | Used by |
|-----|-------|---------|
| `person` | Object | Header on both PDFs and `/cv` |
| `summary` | String (one paragraph) | Professional summary section |
| `experience` | Array of jobs, most recent first | Career history table |
| `engagements` | Array of `{ sector, work, appears_on }` | Selected enterprise engagements |
| `skills.specializations` | Array of strings | Bullet list under the photo |
| `skills.technical` | Array of `{ name, level }` (level 0.0–1.0) | Bar-fraction skills graphic |
| `skills.competencies` | Array of strings | Tag cloud at the bottom |
| `certifications` | Array of `{ name, kind }` | Certifications block (icon picked by `kind`) |
| `speaking` | Array of `{ venue, talk, metric, appears_on }` | Speaking credibility |
| `education` | Array (empty for now) | Reserved |

### `appears_on`

Entries on `experience`, `engagements`, and `speaking` carry an `appears_on`
array. Valid values: `1page`, `multipage`. The Jinja template filters by this
on each variant. The `/cv` HTML page ignores it and shows everything.

### `level` on technical skills

Float in `[0.0, 1.0]`. The LaTeX template passes it directly to
`\barrule{level}{0.5em}{cvpurple}`. The Astro page renders a CSS-only bar
using `style={"--bar-fill: " + (level * 100) + "%"}` and a `width: var(--bar-fill)`
rule in `global.css`. No client-side JS.

## How to add a new variant later

If a "consultant" or "speaker" CV is needed:

1. Author `cv/data/consultant.yml` (or whatever) following the same schema.
2. Add a `cv/templates/consultant.tex.j2` if the layout differs from architect.
3. Extend `cv/build.py` to iterate variants and emit
   `public/cv/{variant}-{1page,multipage}.pdf`.
4. Update `.github/workflows/cv.yml` `paths:` filter if needed (probably not —
   `cv/**` already covers it).

## Local build (informational; CI is source of truth)

```powershell
# Requires Python 3, pyyaml, jinja2, and latexmk on PATH.
python cv/build.py
# Outputs land in public/cv/.
```

CI installs `texlive-*` + `latexmk` via `apt-get` on the runner and invokes
`python3 cv/build.py` directly (see `.github/workflows/cv.yml`). A local TeX
install is not required to ship.

## End-to-end pipeline

A push to `main` that touches `cv/**` runs three workflow legs in sequence:

1. `cv.yml` `build` job — renders both PDFs and uploads them as artifacts.
2. `cv.yml` `commit` job — downloads the artifacts and commits them to
   `public/cv/` via `git-auto-commit-action`. Because the bot push uses
   `GITHUB_TOKEN`, GitHub's anti-loop rule prevents it from triggering
   `pages.yml` automatically. `cv.yml` therefore explicitly dispatches
   `pages.yml` (`gh workflow run pages.yml --ref main`) when the auto-commit
   step reports `changes_detected == 'true'`.
3. `pages.yml` — rebuilds the Astro site (which re-reads `architect.yml`),
   runs the lychee link gate against the rendered `dist/`, and deploys to
   GitHub Pages.

Net effect: edit the YAML, push, walk away. New PDFs and the updated `/cv`
page are live within a couple of minutes with no manual steps.
