# `cv/`: CV source data

This directory holds the source of truth for the CV. It is **data only**; there
is no build step here.

`cv/data/architect.yml` is consumed by:

1. **`src/pages/cv.astro`**: reads the YAML at build time and renders the `/cv`
   route. This is the only rendered output.
2. **`scripts/check-facts.mjs`**: cross-checks claims made in site copy against
   this file and `content/facts.yml`, gated by `.github/workflows/fact-check.yml`.

There is deliberately no PDF build. A LaTeX pipeline (`build.py`, a Jinja
template, a vendored `hipstercv` class, and `.github/workflows/cv.yml`) used to
render 1-page and multi-page PDFs into `public/cv/`. It was removed: the `/cv`
page already carries a print stylesheet, so browser print-to-PDF covers the
occasional need, and tailored per-application CVs are generated outside this
repo. Recover it from git history if it is ever wanted back.

## Layout

```
cv/
  README.md                   ← this file
  data/
    architect.yml             ← single source of truth (sanitized; review before commit)
```

## Data redaction rules (HARD)

`cv/data/architect.yml` ships in a public repo and renders straight onto a
public page. The following rules are non-negotiable.

| Class | Rule |
|-------|------|
| Surname | Never. First name only, per the identity rules in `.github/copilot-instructions.md`. |
| Employer names | Never. Use a generic descriptor (e.g. "Global cloud platform vendor", "Norwegian systems integrator"). |
| Phone numbers | Never. Phone is permanently removed from the CV. |
| Real customer names | Never. Use sector + scale (e.g. "Tier-1 Nordic Bank"). |
| Email | `hello@opedal.tech` only. The public alias forwarded by Domeneshop. The underlying inbox address is private. |
| Employer-internal Connect-style phrasing | Never. No "revenue contributor", "pipeline ownership", "multi-million dollar targets", "consumption growth" as a deliverable, or rating language. Use neutral industry phrasing. |
| Codenames | Never. Public product names only. |
| Tracked metrics that are real and defensible | Allowed when anonymized at sector level (e.g. "48M+ NOK consultant portfolio", "94% NIC approval"). |

If you are unsure, leave it out.

Product and certification names are not employer references: `Microsoft Azure`,
`Microsoft Entra ID` and `Microsoft Certified: ...` are all fine, because they
describe technology and credentials rather than where the author works.

## Schema overview

`architect.yml` has these top-level keys:

| Key | Shape | Renders as |
|-----|-------|------------|
| `person` | Object | `/cv` header |
| `summary` | String (one paragraph) | Professional summary section |
| `experience` | Array of jobs, most recent first | Career history |
| `engagements` | Array of `{ sector, work }` | Selected enterprise engagements |
| `skills.specializations` | Array of strings | Bullet list |
| `skills.technical` | Array of `{ name, level }` (level 0.0 to 1.0) | CSS bar graphic |
| `skills.competencies` | Array of strings | Tag cloud at the bottom |
| `certifications` | Array of `{ name, kind }` | Certifications block |
| `speaking` | Array of `{ venue, talk, metric }` | Speaking credibility |
| `open_source` | Array of `{ group, repos[] }` | Open source section |
| `education` | Array (empty for now) | Reserved; the section header is skipped when empty |

### `level` on technical skills

Float in `[0.0, 1.0]`. `cv.astro` renders a CSS-only bar using
`style={"--bar-fill: " + (level * 100) + "%"}` against a `width: var(--bar-fill)`
rule in `global.css`. No client-side JS, which the site's CSP forbids anyway.

## Editing

Edit the YAML, open a PR, merge. The `Build Astro site` check renders `/cv` from
your branch, and `Fact-check content` validates the claims. The Pages deploy
publishes the updated page automatically.
