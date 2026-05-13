# Routing — opedal.tech

The coordinator picks the agent based on the file or surface mentioned. When the user names an agent directly, route there.

## File / surface routing

| Signal | Route to |
|---|---|
| `cv/architect/**`, `cv/templates/**`, `cv/build.py`, `.github/workflows/cv.yml`, anything PDF-output | **Aaron** |
| `src/pages/cv.astro`, `@media print` rules, `ProfilePage` schema | **Bales** |
| `src/pages/index.astro`, any `src/components/*.astro` (Hero, OpenSource, Work, Speaking, Contact, Nav), bulk of `src/styles/global.css` (section markers, repo rows, language borders) | **Kranz** |
| `src/pages/work.astro`, the `/work` CSS subsection in `global.css` | **Lovell** |
| `public/fonts/**`, `@font-face` rule, `public/og-default.png`, final `npm run build`, `pdftotext` checks, redaction grep, link audit, hardening regression checks | **Garman** |
| `.squad/orchestration-log/**`, `.squad/log/**`, decisions inbox merge, cross-agent history updates | **Scribe** (always background, never wait) |
| GitHub issues / PR queue triage, board status | **Ralph** |

## Cross-cutting requests

- **"redesign the homepage"** → Kranz primary; Lovell may be spawned in parallel if work-section evidence rows are touched.
- **"CV"** ambiguous → ask: PDF (Aaron), HTML (Bales), or content of `architect.yml` (coordinator authors directly with locked redactions).
- **"Add a font" / "verify the build" / "audit links"** → Garman.
- **"Sanity check before PR"** → Garman runs the full verification gate.

## Always-respect global rules (every spawn prompt MUST repeat)

- CSP is hard. No `<style>` blocks in `.astro` components. No `<script>` blocks except `<script type="application/ld+json">`. No `define:vars`. No external CDN.
- Every `target="_blank"` needs `rel="noopener noreferrer"`.
- All GitHub Actions must be SHA-pinned with a version comment.
- Co-author trailer on every commit: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
