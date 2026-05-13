# Aaron — history

## Core Context

- **Project:** `martinopedal/opedal.tech` — personal site for Martin Opedal (Lead Cloud Solution Architect at Microsoft, Oslo).
- **Stack:** Astro 5 (static, `npm run build` → `dist/`), Markdown blog, plain CSS, GitHub Pages, Node 22.
- **Maintainer:** Martin Opedal (`martinopedal`). Solo-maintained.
- **My role:** CV Pipeline Specialist. I own the LaTeX → PDF build for the Architect CV.
- **My branch context:** working on `feat/cv-and-redesign` (PR B).

## What I know about the CV inputs

- **Vendored upstream:** `cv/architect/{hipstercv.cls, hipstercv.sty, photo.jpg}` came from `C:\CV\CV\` on the maintainer's machine. The class and style are MIT-licensed `latex-ninja/hipster-cv`. Don't modify them.
- **Source of truth:** `cv/data/architect.yml` — sanitized, locked. Phone removed. Email is `hello@opedal.tech` (the public alias). Sales-language softened to "Strategic accounts portfolio across regulated Nordic enterprises".
- **Schema docs:** `cv/README.md` is the schema reference. Read it before authoring the template.
- **Visual baseline:** the unmodified LaTeX at `C:\CV\CV\main.tex` (multi-page) and `C:\CV\CV\single-page\architect\main.tex` (1-page) is what my Jinja-rendered output should visually match. The visuals are not being redesigned in PR B — only the data source and build pipeline.

## Conventions to respect

- All GitHub Actions are SHA-pinned with `# vX.Y.Z` comments. See `.github/workflows/pages.yml` for the canonical pattern.
- Top-level workflow `permissions:` are minimum; jobs declare what they need.
- Co-author trailer on every commit: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.

## Learnings

(append as work progresses)
