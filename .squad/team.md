# Squad — opedal.tech

## Project Context

- **Repo:** `martinopedal/opedal.tech` — personal site for Martin Opedal (Lead Cloud Solution Architect at Microsoft, Oslo).
- **Stack:** Astro 5 (static output), Markdown blog, plain CSS in `src/styles/global.css`, GitHub Pages, Node 22 in CI.
- **Maintainer:** Martin Opedal (`martinopedal`). Solo-maintained.
- **Current PR:** PR B on branch `feat/cv-and-redesign` — redesign + `/cv` route + same-repo LaTeX → PDF pipeline for the Architect CV. Details in `.squad/identity/now.md`.

## Members

| Cast name | Role | Universe | Surface owned |
|---|---|---|---|
| Aaron | ⚙️ CV Pipeline Specialist | apollo-mocr | `cv/architect/**`, `cv/templates/architect.tex.j2`, `cv/build.py`, `.github/workflows/cv.yml`, output PDFs in `public/cv/` |
| Bales | ⚛️ CV HTML Page Specialist | apollo-mocr | `src/pages/cv.astro`, `@media print` block in `src/styles/global.css`, `ProfilePage` JSON-LD in the `head-extra` slot |
| Kranz | 🏗️ Site Redesign Specialist | apollo-mocr | `src/components/{Hero,OpenSource,Work,Speaking,Contact,Nav}.astro`, `src/pages/index.astro` recomposition, the bulk of `src/styles/global.css` (section markers, repo rows, work rows, language borders) |
| Lovell | 📝 `/work` Route Specialist | apollo-mocr | `src/pages/work.astro` (annotated evidence rows for every work area), corresponding CSS section in `src/styles/global.css` |
| Garman | 🧪 Typography + Verification Specialist | apollo-mocr | `public/fonts/jetbrains-mono-variable.woff2` + `@font-face` rule, `public/og-default.png` slot, final `npm run build`, `pdftotext` keyword grep, link audit, redaction grep, hardening verification |
| Scribe | 📋 Memory, decisions, session logs | exempt | `.squad/orchestration-log/**`, `.squad/log/**`, `.squad/decisions.md` (merge from inbox), cross-agent history updates |
| Ralph | 🔄 Work Monitor | exempt | Issue/PR scan, work-check cycle, idle-watch |

## Boundaries

- **No cross-writes between specialists** without coordinator handoff. Aaron does not edit `src/`. Bales does not edit `cv/`. Kranz does not edit `src/pages/cv.astro` or `src/pages/work.astro`. Lovell does not touch components other than what is needed by `work.astro`. Garman is read-only on production code unless adding `public/fonts/jetbrains-mono-variable.woff2` and the matching `@font-face` rule, or fixing a verification-gate-blocking issue with explicit coordinator approval.
- **Scribe is silent.** No domain output, no advice. Logs and decisions only.
- **Ralph is monitor-only.** Does not write production code.

## Reviewer Chain

- **Garman is the lockout reviewer** for the verification gate (`npm run build`, `pdftotext` keyword grep, redaction grep, link audit). On reject, the original specialist is locked out per Reviewer Rejection Protocol; a different specialist (or fresh spawn) does the fix.
- **Kranz reviews cross-component design judgment** when two specialists disagree on shared CSS surface area in `global.css`.
