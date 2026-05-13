# Decision: Jinja2 custom delimiters for LaTeX templating

**By:** Aaron (CV Pipeline Specialist)  
**Date:** 2026-05-13  
**Context:** PR B — CV pipeline

## What

Use custom Jinja2 delimiters when embedding Jinja templates in LaTeX:
- Block delimiters: `((*` and `*))` (instead of `{%` and `%}`)
- Variable delimiters: `(((` and `)))` (instead of `{{` and `}}`)
- Comment delimiters: `((=` and `=))` (instead of `{#` and `#}`)

Set via `Environment()` parameters:
```python
env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    block_start_string="((*",
    block_end_string="*))",
    variable_start_string="(((",
    variable_end_string=")))",
    comment_start_string="((=",
    comment_end_string="=))",
    trim_blocks=True,
    lstrip_blocks=True,
)
```

## Why

LaTeX uses braces heavily (`\textbf{...}`, `\begin{...}`, etc.). Jinja's default `{{` and `{%` delimiters clash, causing parser errors when Jinja tries to interpret LaTeX syntax as template directives. Custom delimiters eliminate the collision.

The `((*`, `(((`, and `((=` patterns are visually distinct, unlikely to appear in LaTeX source, and bracket-style (matching LaTeX's `\macro{arg}` convention loosely).

## Alternatives considered

- **Escape every LaTeX brace:** fragile, error-prone, and unreadable.
- **Render LaTeX fragments separately:** breaks single-source-of-truth for layout, complicates conditional logic.
- **Use a LaTeX-native templating language:** no mature Python-based option; Jinja is widely understood.

## Scope

This decision applies to all future Jinja templates targeting LaTeX output in this repository. If a `consultant.yml` or `speaker.yml` variant is added, the same delimiter pattern should be used for consistency.
