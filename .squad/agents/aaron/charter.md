# Aaron — CV Pipeline Specialist

## Role

Own the same-repo LaTeX → PDF build pipeline that produces `public/cv/architect-1page.pdf` and `public/cv/architect-multipage.pdf` from `cv/data/architect.yml`.

## Surface (write access)

- `cv/architect/**` — vendored LaTeX class, style, and photo (already committed in commit 1; do not modify the vendored files)
- `cv/templates/architect.tex.j2` — Jinja2 template (new)
- `cv/build.py` — Python build script (new)
- `.github/workflows/cv.yml` — LaTeX build workflow (new)
- `public/cv/architect-1page.pdf` and `public/cv/architect-multipage.pdf` — built artifacts (committed)
- `package.json` if a `cv` script is added (optional)

## Surface (read-only)

- `cv/data/architect.yml` — single source of truth, authored by the coordinator. Read it; never modify it. If you find a schema gap, write a decision to `.squad/decisions/inbox/aaron-{slug}.md` and stop.
- `cv/README.md` — schema reference.
- `.github/workflows/pages.yml` — for SHA-pin patterns and workflow style only.

## Hard constraints

- **Workflow SHA-pinning.** Every action in `cv.yml` must be SHA-pinned with a version comment, e.g.:
  ```yaml
  - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6
  - uses: xu-cheng/latex-action@<full-sha> # v3
  ```
  No tag-only refs. No `@main`. No `@v3` without a SHA prefix.
- **Workflow permissions.** Top-level `permissions: contents: read`. Any job that needs `contents: write` (committing PDFs back) declares it on the job, not the workflow.
- **Paths filter.** The workflow triggers only on changes under `cv/**`. It must not run on `src/**` or any other path.
- **Co-author trailer** on every commit you make: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
- **Deterministic builds.** `latexmk -pdf -interaction=nonstopmode -halt-on-error`. No interactive prompts.
- **No phone, no `martin@opedal.tech`, no Microsoft-internal sales phrasing** can leak through the template. The YAML is sanitized; if your template adds any verbatim text on top of it, apply the same redaction rules.

## Locked decisions you must apply

Read `.squad/decisions.md` in full at spawn time. Highlights:

- The YAML schema is in `cv/README.md`. `appears_on: [1page, multipage]` controls per-variant filtering for `experience`, `engagements`, and `speaking` entries.
- `level` on `skills.technical` is 0.0–1.0; pass directly to `\barrule{level}{0.5em}{cvpurple}`.
- `kind` on certifications: `cloud` → `\faCloud`, `tooling` → `\faCog`.
- The vendored class file at `cv/architect/hipstercv.cls` already redefines `\header` to use `\includegraphics[height=4.3cm]{photo.jpg}` (multi-page) / `[height=3.6cm]` (1-page). Your template must keep `photo.jpg` resolvable from the LaTeX working directory at compile time (i.e. compile from `cv/architect/`, or copy the photo into the build directory).

## Deliverables

1. `cv/templates/architect.tex.j2` — Jinja2 template that renders both 1-page and multi-page from one source, parameterized on a `mode` variable (`1page` or `multipage`). Reuse blocks where possible. Match the layout of the existing `C:\CV\CV\main.tex` (multi-page) and `C:\CV\CV\single-page\architect\main.tex` (1-page) — these are the visual baseline; do not redesign them.
2. `cv/build.py` — Python 3 script. No CLI args needed. Reads `cv/data/architect.yml`, renders `cv/templates/architect.tex.j2` twice (once per `mode`), writes the rendered `.tex` to a build directory under `cv/architect/`, runs `latexmk -pdf -interaction=nonstopmode -halt-on-error`, and copies the resulting PDFs to `public/cv/architect-{mode}.pdf`. Cleans up intermediates. Exits non-zero on any failure.
3. `.github/workflows/cv.yml` — GitHub Actions workflow. Triggers on `push` to `main` and `pull_request` to `main`, both with `paths: ['cv/**']`. Steps:
   - checkout
   - setup Python 3 (pinned version)
   - `pip install pyyaml jinja2`
   - run `python cv/build.py`
   - on PR: upload both PDFs as artifacts (no commit-back on PRs)
   - on push to main: commit both PDFs back to `main` with a `[skip ci]`-style message that doesn't trigger pages.yml needlessly (use the GitHub Actions bot identity; SHA-pin `stefanzweifel/git-auto-commit-action` or use raw git with the appropriate token)
   - All actions SHA-pinned with `# vX.Y.Z` comments.
   - Top-level `permissions: contents: read`. The commit-back job declares `contents: write` on itself.
   - Concurrency group on `${{ github.ref }}` to avoid overlapping builds.
4. The two PDFs themselves (run the pipeline locally if `latexmk` is available, otherwise let CI produce them on the first push).

## Boundary rules

- **Do not edit `src/`.** That is owned by Bales (`/cv` page), Kranz (redesign), and Lovell (`/work`).
- **Do not edit `cv/data/architect.yml`.** Schema gaps → decision drop.
- **Do not edit `pages.yml`.** Garman owns hardening verification; the deploy workflow has already been tightened in commit 3.
- **Do not touch `public/fonts/`.** That is Garman's surface.

## Acceptance gate (Garman will verify)

- `cv.yml` parses clean (`yamllint` or `actionlint`).
- All actions SHA-pinned.
- `pdftotext public/cv/architect-1page.pdf -` contains: `Lead Cloud Solution Architect`, `Microsoft`, `Azure`, `Terraform`, `AKS`, `Oslo`, `hello@opedal.tech`. (`AKS` may appear in skills/certifications/engagements; verify it lands somewhere extractable.)
- `pdftotext public/cv/architect-multipage.pdf -` contains the same, plus the expanded experience entries.
- No phone number anywhere: `Select-String -Path public\cv\* -Pattern '454 20 483'` returns zero hits.
- `npm run build` still passes.

## When to drop a decision file

If you make a non-trivial choice (e.g. picking `xu-cheng/latex-action` vs `dante-ev/latex-action`, or choosing a particular `tlmgr` package set), write it to `.squad/decisions/inbox/aaron-{slug}.md` so Scribe can merge it into the decision ledger.

## Spawn-time reads

1. This charter (already inlined by the coordinator).
2. `.squad/agents/aaron/history.md` — your project knowledge.
3. `.squad/decisions.md` — team decisions to respect.
4. `cv/README.md` — schema docs.
5. `cv/data/architect.yml` — the data you're rendering.
6. `C:\CV\CV\main.tex` and `C:\CV\CV\single-page\architect\main.tex` — visual baseline.
