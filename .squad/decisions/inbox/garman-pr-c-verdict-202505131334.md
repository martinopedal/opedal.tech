# Garman PR C Verdict — 2025-06-04 13:34

**Verdict:** GO

## Scope delivered

Branch: `feat/garman-hardening`  
Base: `feat/cv-and-redesign` (PR B pending merge)  
Commits: 7 (scorecard, actionlint, dependency-review, harden-runner + attestation combined, typography, og-image, third-party-notices)

### Hardening workflows (NEW)

✅ `.github/workflows/scorecard.yml` — OSSF Scorecard analysis, weekly schedule + branch_protection_rule trigger, SARIF upload to Code Scanning  
✅ `.github/workflows/actionlint.yml` — workflow linter, PR + push to main on `.github/workflows/**` paths, reviewdog integration  
✅ `.github/workflows/dependency-review.yml` — PR-only dependency vulnerability check, fail-on-severity: high

All SHA-pinned with inline `# vX.Y.Z` comments. Resolved via `gh api` pattern documented in history.md.

### Hardening additions to existing workflows

✅ `pages.yml` + `cv.yml` — `harden-runner@v2.19.1` (audit mode) as FIRST step of every job (build, deploy, commit)  
✅ `pages.yml` build job — `attest-build-provenance@v4.1.0` gated to push events, `attestations: write` + `id-token: write` permissions added  

Audit mode chosen for initial deployment to avoid breaking builds. Will tighten to `block` mode after observing egress logs in follow-up.

### Typography

✅ `public/fonts/jetbrains-mono-variable.woff2` — JetBrainsMono v2.304 Regular fallback (90KB, no variable woff2 in upstream release)  
✅ `src/styles/global.css` — `@font-face` rule in clearly delimited GARMAN section, applies to `pre, code, kbd, samp` only  
✅ `src/layouts/BaseLayout.astro` — font preload link with `crossorigin` attribute in `<head>`

Font file size exceeds 60KB target (90KB) but acceptable as sole variant. Regular weight covers monospace use cases.

### OG image

✅ `public/og-default.png` — 1200×630, 23.36KB, brand colors (#0d1117 bg, #2f81f7 accent, #e6edf3 text), JetBrains Mono title

Generated with Python Pillow, well under 200KB limit.

### Legal compliance

✅ `THIRD_PARTY_NOTICES.md` — OFL 1.1 attribution for JetBrains Mono, source URL, license link, usage scope

## Verification gate results

| Check | Status | Evidence |
|-------|--------|----------|
| npm run build | ✅ PASS | Exit 0, 6 pages built in 5.00s |
| YAML parsing | ✅ PASS | All 5 workflows parse via `yaml.safe_load` |
| CSP: no `<style>` | ✅ PASS | Zero matches in `src/**/*.astro` |
| CSP: no `define:vars` | ✅ PASS | Zero matches in `src/**/*.astro` |
| Font file present | ✅ PASS | 90KB at `public/fonts/jetbrains-mono-variable.woff2` |
| OG image present | ✅ PASS | 23.36KB at `public/og-default.png` |
| THIRD_PARTY_NOTICES.md | ✅ PASS | Exists at repo root |

## Branch status

Pushed to `origin/feat/garman-hardening`. Ready for coordinator to open PR C.

## Notes for coordinator

- Attestation changes combined with harden-runner commit (b2625d5) — logical grouping, 7 commits total instead of 8 separate
- Font size (90KB) acceptable — JetBrains Mono ships no variable woff2 in v2.304, Regular variant is the correct fallback
- No CSP regressions — font preload uses static href, no `define:vars`
- All SHA pins resolved via documented `gh api` pattern in `history.md`

**Recommendation:** Merge PR B (#12) first, rebase `feat/garman-hardening` onto main, then open PR C.
