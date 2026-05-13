# Decisions — opedal.tech

Authoritative decision ledger. Append-only. Drop-box pattern: agents write to `.squad/decisions/inbox/{agent}-{slug}.md`; Scribe merges into this file.

---

## 2026-05-13: PR B kickoff — Apollo MOCR cast, three-commit bootstrap

**By:** Martin Opedal (via Copilot)
**What:** Stand up a five-specialist Squad for PR B (`feat/cv-and-redesign`) using the Apollo Mission Control universe. Cast: Aaron (CV pipeline), Bales (CV HTML page), Kranz (site redesign), Lovell (`/work` route), Garman (typography + verification). Bootstrap workspace in three sequential commits before specialists fan out.
**Why:** PR B is a checklist-heavy build pipeline plus a redesign with hard CSP flight rules and a verification gate. Apollo MOCR maps the work shape directly. Three commits (vendor LaTeX, define YAML, scaffold + harden) keep the diff readable for solo review.

## 2026-05-13: Locked content redactions for `cv/data/architect.yml`

**By:** Martin Opedal (via Copilot)
**What:**
- REMOVE phone `+47 454 20 483` everywhere (LaTeX, HTML CV, homepage Contact).
- Email switched to `hello@opedal.tech` alias (forwarded by Domeneshop to a private inbox).
- SOFTEN "Top revenue contributor with multi-million dollar targets, pipeline ownership, forecasting" → "Strategic accounts portfolio across regulated Nordic enterprises".
- Drop redundant "Revenue-accountable with multi-million dollar targets" sentence from professional summary.
- KEEP verbatim: 48M+ NOK consultant portfolio, Tier-1 Nordic Bank, Defense Contractor, Government Bodies, NIC speaker (94% approval, Level 300, live-streamed).
**Why:** No phone in public; no Microsoft-internal Connect-style sales-language phrasing in a public CV; verifiable anonymized metrics retained for credibility.

## 2026-05-13: Locked design decisions (3-model consensus)

**By:** Martin Opedal (via Copilot) — synthesizing review by Claude Opus 4.7, GPT-5.5, Claude Sonnet 4.6
**What:**
- KEEP hero eyebrow `Lead Cloud Solution Architect · Microsoft`.
- Primary CTA `View open source` → `/work` (or `#open-source`). Secondary CTA `Email me` → `mailto:hello@opedal.tech`.
- Multi-page site: add `/cv` and `/work` routes in addition to homepage. Skip `/now`.
- KEEP small/subtle name gradient (`#2f81f7 → #58a6ff`).
- DROP emoji on Work / OpenSource / Speaking cards. Do NOT replace with Octicons.
- OpenSource: replace card grid with grouped annotated rows by problem domain. Drop hardcoded star counts. 2px coloured left border per language extending the existing `.repo-lang.{terraform,python,powershell}` pattern.
- Work: replace card grid with annotated rows. Each work area gets `→ See [repo]` / `→ Read [post]` / `→ Watch [talk]` evidence links.
- Typography: KEEP system fonts for body. ADD JetBrains Mono self-hosted (~30KB woff2) for code blocks only. DO NOT add Inter/Geist.
- OG image: static one-time `og-default.png`. Skip Satori per-post (only 2 posts today).
- Section markers: thin mono labels and a thin accent rule under each `h2`. `01/02/03` numbering optional.
- Print stylesheet for `/cv`: hide nav, white background, black text, `page-break-before` on each `h2`.
**Why:** Recorded so all five specialists apply the same direction without re-deciding mid-PR.

## 2026-05-13: Repo grouping for OpenSource section

**By:** Martin Opedal (via Copilot)
**What:** Group `OpenSource.astro` rows by problem domain:
- **Azure governance & assessment**: `azure-analyzer`, `alz-graph-queries`
- **GitHub runners & private networking**: `terraform-azurerm-avm-ptn-cicd-agents-and-runners`, `ghec-vnet-runners-azure`, `terraform-azurerm-github-runners-alz-corp`
- **Terraform platform modules**: `terraform-azapi-aks-automatic`, `terraform-azurerm-avm-ptn-aiml-ai-foundry`
- **AKS automation**: `terraform-azapi-aks-automatic`, `aks-automatic-ingress-migration`
- **Other tooling**: `news-fetcher`, `linkedin-auto-poster`
**Why:** Sells the work as a coherent platform-engineering portfolio rather than a flat list.

## 2026-05-13: Hardening folded into bootstrap commit 3

**By:** Martin Opedal (via Copilot)
**What:** Pure-additive baseline hardening shipped with the squad scaffold:
- `public/.well-known/security.txt` (RFC 9116, 1-year Expires).
- `Permissions-Policy` meta in `BaseLayout.astro` head — denies all browser capabilities except `fullscreen=(self)`. Documented limitation: `<meta http-equiv>` ignored by Firefox/Safari, honoured by Chromium.
- `Referrer-Policy` meta in `BaseLayout.astro` head — `strict-origin-when-cross-origin`.
- `pages.yml` permissions tightening: top-level becomes `contents: read` only; `pages: write` and `id-token: write` scoped to `deploy` job.
**Why:** Defense-in-depth, RFC-conforming security contact channel, principle of least privilege on the deploy workflow. Zero risk to `npm run build`.

## 2026-05-13: PR C scope deferred (NOT to be touched in PR B)

**By:** Martin Opedal (via Copilot)
**What:** OpenSSF Scorecard, `actionlint`, `step-security/harden-runner` audit mode, `actions/attest-build-provenance`, `actions/dependency-review-action`. Queued for PR C after PR B merges.
**Why:** Scope discipline — no specialist drift into security tooling not on PR B's surface.

## 2026-05-13: `.squad/` ships in PR B

**By:** Martin Opedal (via Copilot)
**What:** The squad coordination state (`.squad/**`) is committed as part of PR B. The squash commit will absorb it cleanly.
**Why:** The team that built the PR ships with the PR. Cleaner than splitting into a tiny pre-PR.

## 2026-05-13: xu-cheng/latex-action for CI LaTeX environment

**By:** Aaron (CV Pipeline Specialist)  
**What:** Use `xu-cheng/latex-action@e2f99d4b3685b0da93f97e1b86ad8fab81105098 # v3` in `.github/workflows/cv.yml` to provide the LaTeX environment (latexmk, TeX Live) for the CV build pipeline. Configured to run `python3 cv/build.py` as the "compiler" argument (non-standard use, but the action's Docker container includes Python 3, and our build script orchestrates LaTeX compilation via `subprocess.run(["latexmk", ...])`).

**Why:** Single action provides full LaTeX environment — deterministic build via Docker, SHA-pinned, auditable, widely used (3.7k stars, active maintenance). Alternatives (manual apt-get install) are brittle; Tectonic doesn't support hipster-cv without patching.

**Scope:** Applies to `.github/workflows/cv.yml`. Future LaTeX-based pipelines should use the same action.

## 2026-05-13: Commit-back strategy for CV PDFs

**By:** Aaron (CV Pipeline Specialist)  
**What:** `.github/workflows/cv.yml` commits built PDFs back to the `main` branch via `stefanzweifel/git-auto-commit-action@b863ae1933cb653a53c021fe36dbb774e1fb9403 # v5`. PDFs are generated artifacts committed to repo (not uploaded separately); commit-back happens in a dedicated `commit` job with scoped `permissions: contents: write`. Workflow has concurrency group (`cv-${{ github.ref }}`) to prevent simultaneous builds on same ref from conflicting. File pattern: `public/cv/architect-*.pdf`. Commit message: `chore(cv): rebuild architect PDFs`.

**Why:** PDFs must be available at `/cv/architect-1page.pdf` and `/cv/architect-multipage.pdf` on deployed site. GitHub Pages serves `public/` as site root — PDFs must be in repo at deploy time. Separate `commit` job keeps `build` job read-only (principle of least privilege); `build` runs on PRs and pushes, `commit` runs only on push to `main`. Concurrency group prevents conflicts when two commits to `main` touch `cv/**` in quick succession.

**Scope:** Applies to `.github/workflows/cv.yml`. Future pipelines that need to commit generated files should use the same pattern.

## 2026-05-13: Jinja2 custom delimiters for LaTeX templating

**By:** Aaron (CV Pipeline Specialist)  
**What:** Use custom Jinja2 delimiters when embedding Jinja templates in LaTeX:
- Block delimiters: `((*` and `*))` (instead of `{%` and `%}`)
- Variable delimiters: `(((` and `)))` (instead of `{{` and `}}`)
- Comment delimiters: `((=` and `=))` (instead of `{#` and `#}`)

Set via `Environment()` parameters with `trim_blocks=True` and `lstrip_blocks=True`.

**Why:** LaTeX uses braces heavily (`\textbf{...}`, `\begin{...}`, etc.). Jinja's default `{{` and `{%` delimiters clash with LaTeX syntax, causing parser errors. Custom delimiters eliminate collision. The `((*`, `(((`, and `((=` patterns are visually distinct, unlikely to appear in LaTeX source, and bracket-style (loosely matching LaTeX's `\macro{arg}` convention).

**Scope:** Applies to all future Jinja templates targeting LaTeX output. `consultant.yml` or `speaker.yml` variants should use the same delimiter pattern.

## 2026-05-13: Language border colors and section marker scale

**By:** Kranz (PR B redesign session)  
**What:** Added language-specific colored left borders to repo rows in OpenSource section. Implemented as `.repo-row.lang-{language}` classes with 2px left border colors: terraform `#844fba`, python `#3fb950`, powershell `#5391fe`, typescript `#3178c6`, javascript `#f1e05a`, go `#00add8`, csharp `#178600`, all `var(--accent)`. Section marker styling: `.section-label` (mono font, 0.7rem, 0.15em letter-spacing, uppercase, muted color) and `section h2` (0.75rem padding-bottom, 1px solid border-bottom using `var(--border)`).

**Why:** Visual consistency with repo language palette; mono labels and accent rules provide visual hierarchy without emoji or Octicons.

## 2026-05-13: PR C scope deferred — coordinator decision on scope expansion

**By:** Coordinator (noting Garman spawn context)  
**What:** PR C will handle: OpenSSF Scorecard, `actionlint`, `step-security/harden-runner` audit mode, `actions/attest-build-provenance`, `actions/dependency-review-action` — queued after PR B merges.

**Why:** Scope discipline — no specialist drift into security tooling not on PR B's surface. Garman's PR C spawn (currently running) references this decision for scope boundaries.


# Reed — Live contrast audit

**By:** Reed (Visual Designer)  
**What:** Two surgical token fixes to address "hard to read" user feedback — bump text-dim luminance and flip btn-primary text to dark.  
**Why:** User feedback: colors hard to read. WCAG audit revealed one AA failure (btn-primary white-on-terracotta at 3.12:1) and text-dim hovering just below AAA.

## Pages audited

- **https://martinopedal.github.io/opedal.tech/** — Homepage renders fine for primary text. Hero tagline, section intros, card descriptions, and contact copy all use `--color-text-dim` on either `--color-bg` or `--color-surface`. Visually readable but on the edge—especially on alt-bg sections.
- **https://martinopedal.github.io/opedal.tech/blog/** — Blog hero tagline in text-dim. Blog cards show dates and excerpts in text-dim on surface. Same pattern.
- **https://martinopedal.github.io/opedal.tech/cv/** — CV page heavy with muted body copy (summary, job descriptions, engagement text). All use text-dim. Surface cards dominate.
- **https://martinopedal.github.io/opedal.tech/work/** — Similar pattern to homepage—work row descriptions in text-dim on surface cards.

**Key observation:** The site uses `--color-text-dim` extensively for body copy in cards and sections. On `--color-surface` (alt-bg sections), the current 6.35:1 ratio is AA-compliant but not AAA. User perception of "hard to read" is likely caused by this borderline contrast on the warmer, lighter surface background.

## Failure list (current palette)

| Pair | BG | FG | Ratio | WCAG |
|------|----|----|------:|------|
| text on bg | #14110f | #e8e2d8 | 14.60:1 | ✅ AAA |
| text on surface | #1f1b18 | #e8e2d8 | 13.27:1 | ✅ AAA |
| text-dim on bg | #14110f | #a39d92 | 6.98:1 | ✅ AA (borderline AAA) |
| **text-dim on surface** | #1f1b18 | #a39d92 | 6.35:1 | ✅ AA, ❌ AAA |
| accent on bg | #14110f | #d97757 | 6.02:1 | ✅ AA |
| accent on surface | #1f1b18 | #d97757 | 5.48:1 | ✅ AA |
| accent-hover on bg | #14110f | #e59677 | 8.02:1 | ✅ AAA |
| accent-hover on surface | #1f1b18 | #e59677 | 7.30:1 | ✅ AAA |
| **white on accent (btn-primary)** | #d97757 | #ffffff | 3.12:1 | ❌ **FAIL AA** |

**Critical failures:**
1. `.btn-primary` white text on terracotta fails AA (3.12:1 < 4.5:1) — this is the "View open source" and "Email me" CTA buttons.
2. `--color-text-dim` on `--color-surface` at 6.35:1 is technically AA-passing but sits below AAA, contributing to perceived difficulty.

## Proposed token changes

| Token | Before | After | New ratio on bg | New ratio on surface |
|-------|--------|-------|----------------:|---------------------:|
| `--color-text-dim` | #a39d92 | **#ada79d** | 7.87:1 (AAA ✅) | 7.16:1 (AAA ✅) |
| `.btn-primary { color }` | #ffffff | **#14110f** | n/a | n/a |
| `.btn-primary:hover { color }` | #ffffff | **#14110f** | n/a | n/a |

**Rationale:**
- **`#ada79d`** is the minimum brightness bump that achieves AAA (7:1+) on both bg and surface while preserving the warm taupe character. Visually indistinguishable warmth shift, measurable legibility gain.
- **`#14110f`** (existing `--color-bg`) as btn-primary text flips the button to dark-on-terracotta, achieving 6.02:1 contrast. This maintains the warm Architect Charcoal feel (dark brown on terracotta = classic warm aesthetic) without requiring a new token.

## Implementation notes for Kranz

Update `src/styles/global.css`:

### 1. Token change (line 17)
```css
/* Before */
--color-text-dim:    #a39d92;  /* Muted text */

/* After */
--color-text-dim:    #ada79d;  /* Muted text — AAA on both bg and surface */
```

### 2. Button text color (lines 216-226)
```css
/* Before */
.btn-primary {
  background: var(--accent);
  color: #fff;
  border: 1px solid var(--accent);
}

.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: #fff;
}

/* After */
.btn-primary {
  background: var(--accent);
  color: var(--color-bg);  /* Dark warm text for AA compliance */
  border: 1px solid var(--accent);
}

.btn-primary:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: var(--color-bg);  /* Keep dark on hover too */
}
```

### Summary of CSS changes
- Line 17: `#a39d92` → `#ada79d`
- Line 218: `color: #fff;` → `color: var(--color-bg);`
- Line 225: `color: #fff;` → `color: var(--color-bg);`

## Non-color findings (spot-check)

1. **Section markers (`.section-label`)** — 0.7rem at 600 weight with 0.15em letter-spacing on warm charcoal. Legible but tight. Consider bumping to 0.75rem or 650 weight if user feedback persists.

2. **Prose line-height** — `.prose` at 1.8 line-height is generous and readable. No change needed.

3. **Code blocks** — System mono stack at 0.875rem. JetBrains Mono not yet loaded (per decisions.md, self-hosted woff2 planned). Once added, verify weight 400–500 renders crisply on dark backgrounds.

4. **Button hit-area** — `.btn` padding of `0.65rem 1.4rem` creates adequate 44px+ touch target vertically. Acceptable.

5. **Focus-visible ring** — No explicit `:focus-visible` styles found in global.css. Browsers apply default outline (typically blue). Consider adding `outline: 2px solid var(--accent); outline-offset: 2px;` to `:focus-visible` for better cohesion with the terracotta palette. (Non-blocking for this audit.)

6. **Mobile nav background** — Line 724 uses `rgba(13, 17, 23, 0.98)` (GitHub dark) instead of the Architect Charcoal bg. Minor visual inconsistency on mobile nav dropdown. Consider `rgba(20, 17, 15, 0.98)` to match.

## Verification

After implementation, all text pairs will pass WCAG AA minimum. `--color-text-dim` and `--color-text` will both hit AAA on both background surfaces. The terracotta accent remains recognizably terracotta (no hue shift). The warm Architect Charcoal direction is preserved.


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

