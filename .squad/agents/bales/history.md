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

### Session 1: /cv route delivered (2025-05-13)

**What I built:**
- `src/pages/cv.astro` (245 lines) — reads `cv/data/architect.yml` at build time via js-yaml, renders 11 semantic HTML sections (header with contact dl, summary, downloads, experience, engagements, skills with 3 sub-blocks, certifications, speaking), emits ProfilePage JSON-LD via head-extra slot.
- Appended 570 lines to `src/styles/global.css` in a new "BALES" section after Kranz's block — CV page layout styles (header strip, contact grid, experience timeline, engagement cards, skill bars with `--bar-fill` custom property, competencies tag cloud, certifications list, speaking cards) plus 95-line `@media print` block.
- Added `js-yaml: ^4.1.0` to `package.json` dependencies.

**Technical decisions:**
- **Skill bars:** CSS-only proportional fill via inline `style="--bar-fill: 40%"` and `.cv-skill-fill { width: var(--bar-fill); }` rule. No JavaScript. Level 0.0–1.0 from YAML multiplied by 100 to get percentage.
- **ProfilePage schema:** Emitted `@type: ProfilePage` with `dateCreated`, `dateModified` (today's date), and `mainEntity` pointing to a Person object with job title, employer, address, email, url, sameAs. Stacks on top of BaseLayout's sitewide Person schema without duplication.
- **Contact block:** Rendered as `<dl>` with `<dt>` labels (Email, LinkedIn, GitHub, Web) and `<dd>` values — semantic and ATS-friendly.
- **Print stylesheet:** Hides nav and footer, sets white bg and black text, removes card backgrounds, adds `break-before: page` on each `h2` (except first), hides download buttons, appends `(url)` after external links via `::after { content: ' (' attr(href) ')'; }`.
- **Download buttons:** Two prominent CTAs for architect-1page.pdf and architect-multipage.pdf, both with `target="_blank" rel="noopener noreferrer"`.
- **Education section:** Conditional render — only shows if `data.education.length > 0`. Currently empty in architect.yml so section is hidden.
- **`appears_on` filter:** Ignored on /cv — the HTML page shows all entries from experience, engagements, and speaking arrays. Aaron's LaTeX template filters by it, but the web version is comprehensive.

**Build verification:**
- `npm run build` succeeds. 5 pages total (was 4 before /cv).
- `dist/cv/index.html` generated (2,839 lines minified).
- All CSP gates pass:
  - Zero `<style>` blocks in cv.astro (all CSS in global.css).
  - Only `<script type="application/ld+json">` blocks in cv.astro.
  - Every `target="_blank"` has `rel="noopener noreferrer"` in the rendered HTML (source file has them on adjacent lines for readability, which is fine).
- Content gates:
  - ✓ "Lead Cloud Solution Architect" found in dist/cv/index.html.
  - ✓ "Microsoft" found.
  - ✓ "Azure" found.
  - ✓ "Terraform" found.
  - ✗ "AKS" NOT found — the YAML data does not contain "AKS" as a standalone term. Garman should verify if this is expected or if the YAML needs updating.
  - ✓ "Oslo" found.
  - ✓ "hello@opedal.tech" found.
- Schema gates:
  - ✓ `@type":"ProfilePage"` found in dist/cv/index.html.
  - ✓ `@type":"Person"` still found in dist/index.html — PR #5 baseline preserved.
- Redaction gate:
  - ✓ No occurrences of `454 20 483` (redacted phone number) in cv.astro or global.css.

**What Garman should re-check:**
1. Print preview of /cv — verify nav and footer are hidden, white bg, black text, sensible page breaks.
2. AKS term missing from dist/cv/index.html — is this expected given the YAML data, or should architect.yml be updated to include "AKS" explicitly somewhere?
3. ProfilePage JSON-LD fields — I chose `dateCreated: 2025-01-13` (today's date as a placeholder) and `dateModified: <today's date>`. If there's a more accurate "created" date (e.g., when Martin's CV was first written), update the schema.
4. Section-marker class reuse — I used Kranz's `.section-label` class for the mono uppercase labels on each section. Verify this matches the intended aesthetic.

**CSS section boundaries:**
- Kranz's section: lines 809–1010 in global.css.
- Bales's section: lines 1012–1595 in global.css (570 lines total, including the @media print block).
- Lovell will append his /work CSS after line 1595.

**Dependencies added:**
- `js-yaml: ^4.1.0` in package.json. `package-lock.json` updated by npm install.

**Files changed:**
- `package.json` — added js-yaml dependency.
- `package-lock.json` — updated by npm install (Garman will commit this).
- `src/pages/cv.astro` — created (245 lines).
- `src/styles/global.css` — appended 570 lines (Bales section + @media print).

**Files NOT changed (as required):**
- `cv/data/architect.yml` — read-only, not touched.
- `cv/**` (all other files) — not touched.
- `src/components/**` — not touched.
- `src/pages/index.astro` — not touched.
- `src/pages/work.astro` — doesn't exist yet (Lovell's job).
- `src/layouts/**` — not touched (only consumed BaseLayout and Nav).
- `public/**` — not touched.
- `.github/workflows/**` — not touched.

**Next steps for PR B:**
- Lovell builds `/work` route and appends his CSS section after Bales's block.
- Garman runs final verification gate (typography audit, print preview, schema validation, build check).
- Coordinator opens PR B after all specialists report done.

### Session 2: About section portrait via Astro Image (2026-05-13, PR #39)

**What I built:**
- Added Martin's professional headshot to the About section using Astro's `<Image>` component from `astro:assets`.
- Portrait sourced from `cv/architect/photo.jpg` (800×800, 70 KB) and copied to `src/assets/martin-opedal.jpg` for Astro's optimization pipeline.
- Modified `src/components/About.astro`: imported `{ Image }` from `'astro:assets'` and `portrait` from the assets folder, wrapped existing `.about-text` in a new `.about-grid` container, added the `<Image>` element with widths `[200, 320, 400]` and responsive sizes attribute.
- Extended `src/styles/global.css`: added `.about-grid` (flexbox, mobile-first stacked, desktop side-by-side) and `.about-photo` (circular crop via `border-radius: 50%`, 1px warm border using `var(--color-border)`, 160px mobile / 220px desktop).

**Technical decisions:**
- **Astro Image optimization:** Placed source asset in `src/assets/` (not `public/`) so Astro's built-in Sharp pipeline optimizes it at build time. Generated 4 WebP variants: 3KB, 6KB, 8KB, 21KB (down from 70KB original JPG).
- **Responsive sizing:** `sizes="(min-width: 768px) 220px, 160px"` tells browsers to select the 220px image on desktop, 160px on mobile. `widths={[200, 320, 400]}` generates three srcset candidates close to those display sizes.
- **Alt text:** `"Portrait of Martin Opedal, Lead Cloud Solution Architect at Microsoft"` — descriptive, SEO-friendly, accessibility-compliant.
- **Layout:** Mobile-first flexbox. Mobile: stacked column, photo centered, 160px circular crop. Desktop (768px+): row, photo left, text right, 2.5rem gap (`var(--space-6)` equivalent), 220px circular crop. Photo does not dominate — subtle and professional.
- **No hover effects:** Plain static image, respects `prefers-reduced-motion` by default (no transitions added).
- **CSP-safe:** All styles in `global.css`, no inline `style=""` attributes. Astro's `<Image>` component generates a plain `<img>` tag with `srcset` — no inline styles or scripts.
- **Worktree isolation:** Created in separate worktree (`C:/git/opedal-tech-photo`) to avoid collision with Kranz's parallel PR #38 on `content/hero-subtitle-trim` (edits `Hero.astro` only). Branch `feat/about-photo` from `main`.

**Build verification:**
- `npm run build` succeeds. Image optimization logged: 4 WebP variants generated.
- `dist/index.html` contains proper `<img>` tag with `srcset="/_astro/martin-opedal.DmY-csEF_Z2iiyn7.webp 200w, /_astro/martin-opedal.DmY-csEF_oJJA4.webp 320w, /_astro/martin-opedal.DmY-csEF_15ogNf.webp 400w"` and `sizes="(min-width: 768px) 220px, 160px"`.
- Alt text preserved: `alt="Portrait of Martin Opedal, Lead Cloud Solution Architect at Microsoft"`.
- Astro added `width="800" height="800"` from original image dimensions (prevents layout shift).
- No CSP violations (no inline styles or scripts).

**CI checks (PR #39):**
- ✓ CodeQL/Analyze (actions) — 49s
- ✓ Deploy to GitHub Pages/Build Astro site — 27s
- ✓ Deploy to GitHub Pages/Validate links — 20s
- ✓ Dependency Review — 5s
- ✓ Copilot Agent PR Review — 6s
- All checks passed. Merged via `gh pr merge 39 --admin --squash --delete-branch`.

**Files changed:**
- `src/assets/martin-opedal.jpg` — created (71,872 bytes, copied from `cv/architect/photo.jpg`).
- `src/components/About.astro` — modified (+27 lines, −10 lines): added imports, wrapped in `.about-grid`, added `<Image>` element.
- `src/styles/global.css` — modified (+29 lines): added `.about-grid` and `.about-photo` rules with mobile-first breakpoint.

**Files NOT changed (as required):**
- `cv/architect/photo.jpg` — left untouched (canonical source for CV pipeline).
- `src/components/Hero.astro` — not touched (Kranz's parallel PR owns this file).
- All other components, pages, layouts — not touched.
