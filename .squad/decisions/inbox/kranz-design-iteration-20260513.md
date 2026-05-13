# Design Iteration — Kranz decisions (2026-05-13)

**By:** Kranz (Site Redesign Specialist), responding to maintainer feedback post PR B merge

## Tag column removal (About section)

**Decision:** Drop the `.about-tags` column entirely. Full-width prose only.

**Rationale:**
- Maintainer flagged the tag tree as "weird/wonky"
- Research of senior-engineer sites (Julia Evans, Dan Abramov, Sindre Sorhus, Lee Robinson) shows they skip keyword boxes entirely — prose-first
- The About prose already names "Azure Landing Zones, AKS Automatic, Terraform, IaC security, sovereign cloud deployments" naturally
- Duplication is awkward; prose reads better solo

**Eliminated generic terms:** Container Apps, ALZ Checklist, GitHub Actions, Azure Policy (maintainer specifically called out)

**Kept if ever revisiting:** Azure Landing Zones, AKS Automatic, Terraform, IaC Security, Sovereign Cloud, GitHub Copilot (6 distinctive terms max)

## Em dash removal (site-wide UI)

**Decision:** Replace all ` — ` (space-emdash-space) in UI surfaces with colons, hyphens, or middle dots.

**Before:** 44 em dashes across components, pages, layouts  
**After:** 0 em dashes (verified via grep)

**Pattern:**
- Title separators: ` — ` → ` · ` (Martin Opedal · opedal.tech)
- List descriptions: ` — ` → `: ` (repo-name: description)
- Prose separators: ` — ` → `: ` or sentence rewrite
- Comments: ` — ` → ` - `

**Scope:** Components, pages, layouts. Blog post markdown content untouched (author's authentic voice).

## Color palette refresh (Architect Charcoal)

**Decision:** Replace GitHub Dark blues (#2f81f7) with Architect Charcoal (warm near-black + terracotta).

**New palette:**
- Base: `#14110f` (warm near-black, from `#0d1117` cold)
- Surface: `#1f1b18` (warm, from `#161b22` cold)
- Text: `#e8e2d8` (warm, from `#e6edf3` cold)
- Text dim: `#a39d92` (warm, from `#8b949e` cold)
- Accent: `#d97757` (terracotta, from `#2f81f7` blue)
- Accent hover: `#e59677` (lighter terracotta, from `#58a6ff` blue)

**Rationale:**
- Maintainer said GitHub blue too close to Microsoft Azure brand
- Warmth distinguishes from cold MS blues
- Matches "datacenters + breweries" tactile identity (warm, grounded, organic)
- Terracotta distinctive, senior-architect signal

**Changes:**
- `:root` CSS custom properties + legacy vars for compatibility
- Hero h1 gradient: `#2f81f7→#58a6ff` → `#d97757→#e59677`
- `theme-color` meta: `#0d1117` → `#14110f`
- Nav background RGBA: `rgba(13,17,23,0.92)` → `rgba(20,17,15,0.92)`

## Nav cleanup (5 items max)

**Decision:** Reduce nav from 8 items to 5 max.

**Old structure:**
- Homepage: About / Work / Open Source / Speaking / Contact (5 section anchors) + Work / CV / Blog (3 page links) = 8 total
- Other pages: Home + Work / CV / Blog = 4 total

**New structure:**
- Homepage: Home / Work / CV / Blog / Contact (5 items, Contact anchor only on homepage)
- Other pages: Home / Work / CV / Blog (4 items)

**Rationale:** Section anchors (About, Open Source, Speaking) reachable by scrolling on homepage. Dedicated page links (Work, CV, Blog) provide cross-page navigation. Contact anchor kept on homepage only for quick access to email CTA.

## Hero CTA alignment

**Decision:** Change label from "View open source" to "See selected work" (destination remains `/work`).

**Rationale:** The label said "open source" but `/work` page is broader (includes ALZ, AKS, IaC, CI/CD, AI, Copilot, Speaking). "See selected work" matches destination.

## Future palette swap pattern

The new CSS uses `--color-*` variables (e.g., `--color-bg`, `--color-accent`) with legacy compatibility aliases (`--bg`, `--accent`). Future palette swaps should:

1. Update the 8 `--color-*` variables in `:root`
2. Update hero gradient (if accent changes)
3. Update `theme-color` meta (if base changes)
4. Update nav RGBA background (if base changes)
5. Test build and verify no hardcoded hex colors leaked

This pattern makes palette swaps surgical and traceable.

## Scope boundaries respected

Per charter, did NOT touch:
- `cv/` (Aaron)
- `.github/workflows/` (Aaron / Garman)
- `public/fonts/`, `public/og-default.png`, `THIRD_PARTY_NOTICES.md` (Garman)
- Blog post markdown content in `src/content/blog/*.md` (maintainer's voice)

**One-PR cross-surface grant:** Em dash scrub authorized on `src/pages/cv.astro` and `src/pages/work.astro` (Bales and Lovell surfaces) as text-only substitution. No layout or styling changes.

## Verification

Build succeeded:
- `npm run build` exits 0
- `dist/index.html` contains eyebrow "Lead Cloud Solution Architect · Microsoft"
- `dist/index.html`, `dist/cv/index.html`, `dist/blog/index.html` all load CSS and emit JSON-LD
- 6 HTML pages generated (index, cv, work, blog index, 2 blog posts)

All acceptance gates passed:
- Em dash count (UI surfaces): 0 (target: 0)
- Generic terms removed: PASS
- No inline `<style>` blocks: PASS
- `.about-tags` / `.tag` classes removed: PASS

