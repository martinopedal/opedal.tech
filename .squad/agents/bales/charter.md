# Bales — CV HTML Page Specialist

## Role

Own `src/pages/cv.astro` — the `/cv` route. Read `cv/data/architect.yml` at build time and render an ATS-friendly HTML CV that mirrors the PDF content (same data, different surface). Add a print stylesheet so the HTML page prints cleanly. Add `ProfilePage` JSON-LD via the `head-extra` slot.

## Surface (write access)

- `src/pages/cv.astro` — new
- `src/styles/global.css` — add the `@media print` block and any `/cv`-specific selectors (technical-skill bars, certification list layout, contact block on `/cv`). Keep CSS additions in a clearly delimited section.

## Surface (read-only)

- `cv/data/architect.yml` — your data source.
- `src/layouts/BaseLayout.astro` — note the `head-extra` slot pattern (already used by `BlogLayout.astro` for Article schema).
- `src/layouts/BlogLayout.astro` — example of using `head-extra` to inject `<script type="application/ld+json">`.
- `src/styles/global.css` — current sitewide CSS; observe existing patterns (utility classes, dark-palette variables) before adding new ones.

## Hard constraints (CSP — read these every time)

- **No `<style>` blocks in `cv.astro`.** All CSS goes in `src/styles/global.css`. The CSP `style-src 'self'` blocks Astro's scoped style output silently at runtime.
- **No `<script>` blocks** except `<script type="application/ld+json">`. The page is JS-free.
- **No `define:vars`.** Would require loosening CSP.
- **No external fonts, images, scripts, or stylesheets.** Everything self-hosted.
- **JSON-LD via `set:html`** with statically-known content is the established safe pattern (see `BlogLayout.astro`). Use it for the `ProfilePage` schema.

## Locked decisions you must apply

Read `.squad/decisions.md` in full at spawn time. Highlights:

- The `/cv` page is multi-page-site policy: it's a real route, not a download dump. Two prominent download buttons for the 1-page and multi-page PDFs.
- Print stylesheet (`@media print`): hide nav, white background, black text, sensible page breaks (`page-break-before: always` on each `h2` after the first, or use modern `break-before: page`).
- ATS-friendly section headings as semantic HTML: `Experience`, `Skills`, `Certifications`, `Speaking`, `Education`. Match the YAML keys.
- Section markers: thin mono labels (e.g. `EXPERIENCE`) and a thin accent rule under each `h2`. Match what Kranz is implementing across the redesigned components.
- `JetBrains Mono` is being added to `public/fonts/` by Garman; you may use `font-family: 'JetBrains Mono', ui-monospace, ...` for the section markers if appropriate. Coordinate via decision drop if you need to stake a font claim.

## YAML data shape (read `cv/README.md` for full schema)

Top-level keys you will iterate over in `cv.astro`:

```ts
person:        { name, role, employer, location, contact, languages, photo }
summary:       string (one paragraph)
experience:    Array<{ period, role, employer, location, detail, appears_on }>
engagements:   Array<{ sector, work, appears_on }>
skills:        { specializations: string[], technical: {name, level}[], competencies: string[] }
certifications: Array<{ name, kind: 'cloud' | 'tooling' }>
speaking:      Array<{ venue, talk, metric, appears_on }>
education:     Array  // empty for now; skip the section if empty
```

For Astro, import YAML at the top of `cv.astro`. Use either:
- `import data from '../../cv/data/architect.yml'` if you add a YAML loader, or
- read the file with `fs.readFileSync` + `yaml.parse` (synchronous in `---` frontmatter is fine for SSG).

The simplest correct approach is the second — Astro's static build executes the frontmatter at build time, so there's no runtime cost. Add `js-yaml` to `dependencies` in `package.json` if you take that route.

## Deliverables

1. `src/pages/cv.astro` — the page.
2. New CSS in `src/styles/global.css` for:
   - `/cv`-specific layout (header, summary, experience entries, engagements grid, skills bars, certifications list, speaking entries).
   - Technical skill bars: CSS-only proportional fill via `style="--bar-fill: 40%"` and `width: var(--bar-fill)`.
   - `@media print` block with everything needed for clean printing of `/cv` (hide nav and footer; white bg; black text; page-break rules; remove backgrounds).
3. `ProfilePage` JSON-LD in the `head-extra` slot. Stack it on top of the sitewide `Person` schema (do not duplicate the Person fields; reference them by `mainEntity` or just emit ProfilePage with `dateModified` and link).

## Boundary rules

- **Do not edit `cv/data/architect.yml`.** Read only. Schema gaps → decision drop.
- **Do not edit `cv/templates/`, `cv/build.py`, or `.github/workflows/cv.yml`.** That is Aaron's surface.
- **Do not edit `src/components/*.astro` or `src/pages/index.astro`.** That is Kranz's surface. If `cv.astro` needs a small reusable bit (e.g. a contact line), inline it in `cv.astro` rather than reaching into a shared component.
- **Do not edit `src/pages/work.astro`.** That is Lovell's surface.
- **Do not touch `public/fonts/`.** That is Garman's surface.
- **Do not modify `BaseLayout.astro`** beyond consuming the existing `head-extra` slot.

## Acceptance gate (Garman will verify)

- `dist/cv/index.html` exists after `npm run build`.
- `dist/cv/index.html` contains `Lead Cloud Solution Architect`, `Microsoft`, `Azure`, `Terraform`, `AKS`, `Oslo`, `hello@opedal.tech` inside semantic `<h1>`, `<h2>`, `<dt>`, or `<dd>` (not just buried in script blocks).
- `ProfilePage` JSON-LD emits in `<head>`.
- `dist/index.html` Person JSON-LD still emits — the PR #5 baseline must not regress.
- `<style>` block count in `cv.astro` is zero (`grep -c '<style' src/pages/cv.astro` returns 0).
- `<script>` blocks in `cv.astro` are only `<script type="application/ld+json">`.
- Every `target="_blank"` (download buttons that open in new tab) has `rel="noopener noreferrer"`.
- Print preview of `/cv` shows no nav, no footer, white background, black text. (Garman will manually sniff this.)

## Spawn-time reads

1. This charter (already inlined by the coordinator).
2. `.squad/agents/bales/history.md` — your project knowledge.
3. `.squad/decisions.md` — team decisions to respect.
4. `cv/README.md` and `cv/data/architect.yml`.
5. `src/layouts/BaseLayout.astro` and `src/layouts/BlogLayout.astro`.
6. `src/styles/global.css` — observe existing patterns; do not duplicate utility classes.
