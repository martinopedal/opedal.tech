# Orchestration: Coordinator-Direct-Edits — Emergency LaTeX fixes

**Session:** PR B execution (`feat/cv-and-redesign`)  
**Date:** 2026-05-13T13:27Z  
**Role:** Squad Coordinator (boundary violation flag)

## Context

Three urgent commits to Aaron's surface (CV pipeline) made before the Squad system prompt was active. Copilot CLI was operating in plain mode, not via task spawn. Logged here as a learning: future sessions should route all CV fixes via Aaron's task spawn rather than coordinator direct-edits.

## Commits

1. **`c688775` fix(cv): hyperref option clash via PassOptionsToPackage**
   - `cv/templates/architect.tex.j2`
   - LaTeX symptom: `! Option clash for package hyperref` during pdflatex compile
   - Root cause: hyperref options were being set twice (once by hipster-cv.cls, again by document preamble)
   - Fix: Wrapped option setting in `\PassOptionsToPackage{…}{hyperref}` before `\documentclass`

2. **`f144c32` fix(cv): close \bgupper brace in \header invocation**
   - `cv/templates/architect.tex.j2`
   - LaTeX symptom: undefined control sequence or TeX grouping error
   - Root cause: `\bgupper{…}` macro call was missing its closing brace
   - Fix: Ensured proper brace pairing in header section

3. **`39c0009` fix(cv): escape LaTeX special chars via Jinja finalize**
   - `cv/build.py`
   - LaTeX symptom: `! Undefined control sequence` when YAML fields contained `_` or `&` unescaped
   - Root cause: Special characters were rendered directly into LaTeX without escaping
   - Fix: Added Jinja `finalize` filter to escape LaTeX special chars (`_` → `\_`, `&` → `\&`, etc.)

## Outcome

All three fixes applied; CV Build CI ✅. Documented as boundary violation so Aaron knows to own these patterns going forward (hyperref, brace hygiene, LaTeX escaping via finalize).

## Learning

Coordinator-direct-edits should be reserved for merge conflicts or trivial type corrections. Substantive domain work (LaTeX, CV schema, pipeline orchestration) routes through the relevant specialist via task spawn.
