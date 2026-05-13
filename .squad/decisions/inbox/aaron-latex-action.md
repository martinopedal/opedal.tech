# Decision: xu-cheng/latex-action for CI LaTeX environment

**By:** Aaron (CV Pipeline Specialist)  
**Date:** 2026-05-13  
**Context:** PR B — CV pipeline

## What

Use `xu-cheng/latex-action@e2f99d4b3685b0da93f97e1b86ad8fab81105098 # v3` in `.github/workflows/cv.yml` to provide the LaTeX environment (latexmk, TeX Live) for the CV build pipeline.

Configured to run `python3 cv/build.py` as the "compiler" argument:
```yaml
- name: Compile CV PDFs with LaTeX
  uses: xu-cheng/latex-action@e2f99d4b3685b0da93f97e1b86ad8fab81105098 # v3
  with:
    root_file: build.py
    working_directory: .
    compiler: python3
    args: cv/build.py
```

This is a non-standard use of the action (it's designed to compile `.tex` files directly), but it works: the action's Docker container includes Python 3, and our build script orchestrates the LaTeX compilation via `subprocess.run(["latexmk", ...])`.

## Why

**Pros:**
- Single action provides the full LaTeX environment — no manual `apt-get install texlive-*` or package hunting.
- Deterministic build via Docker — the same TeX Live version every time, regardless of runner image updates.
- SHA-pinned, auditable, widely used (3.7k stars, active maintenance).

**Cons:**
- Non-standard "compiler" override (using `python3` instead of `pdflatex`/`xelatex`).
- Slightly slower startup due to Docker pull (mitigated by GitHub's action cache).

**Alternatives considered:**
- **Manual setup:** `apt-get install texlive-latex-extra texlive-fonts-extra latexmk`. More transparent but brittle (package names change, dependency resolution varies by runner).
- **Custom Docker action:** overkill for a single-variant CV pipeline.
- **Tectonic:** modern Rust-based LaTeX compiler, but doesn't support the hipster-cv class without patching.

## Scope

This decision applies to `.github/workflows/cv.yml`. If a future PR adds a different LaTeX-based pipeline (e.g., beamer slides), the same action should be used for consistency.

## SHA verification

- **Action:** `xu-cheng/latex-action`
- **Tag:** `v3`
- **SHA:** `e2f99d4b3685b0da93f97e1b86ad8fab81105098` (verified via `gh api repos/xu-cheng/latex-action/commits/v3 --jq .sha` on 2026-05-13)
