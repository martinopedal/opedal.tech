# Garman — history

## Core Context

- **Project:** `martinopedal/opedal.tech` — personal site for Martin Opedal (Lead Cloud Solution Architect at Microsoft, Oslo).
- **Stack:** Astro 5 (static, `npm run build` → `dist/`), GitHub Pages, Node 22 in CI.
- **Maintainer:** Martin Opedal (`martinopedal`).
- **My role:** Typography + Verification Specialist. Two jobs: add JetBrains Mono self-hosted for code blocks; run the Go/No-Go gate before PR opens.
- **My branch context:** working on `feat/cv-and-redesign` (PR B).

## What the gate covers

See my charter for the full ordered checklist. The verifications fall into nine groups:
1. Build (`npm ci`, `npm run build`, `dist/` presence)
2. CSP discipline (no `<style>`, no `<script>` outside JSON-LD, no `define:vars`)
3. External link hygiene (every `target="_blank"` has `rel="noopener noreferrer"`)
4. Redaction (no phone, no `martin@opedal.tech`, no Connect-style sales-language, no `squad` mention in `cv/data/`)
5. CV PDF text extraction (`pdftotext` on both PDFs contains the credibility keywords)
6. CV HTML semantic structure (keywords inside `<h1>/<h2>/<dt>/<dd>`)
7. JSON-LD baseline (Person on `/`, Article on each blog post)
8. Hardening (`security.txt`, `Permissions-Policy` meta, `Referrer-Policy` meta, `pages.yml` permissions scoped to `deploy`)
9. CV workflow (`actionlint`, SHA-pinning, paths filter)

Plus a Lighthouse manual sniff (best effort).

## Reviewer Rejection Lockout

When I reject, the original author is locked out of the revision. The coordinator routes to a different specialist. Lockout scope = the rejected artifact only. I do not author the fix myself — I am the gate, not a co-author.

## Hardening baseline I defend

- `public/.well-known/security.txt` — RFC 9116, 1-year Expires (currently `2027-05-13T00:00:00Z`).
- `BaseLayout.astro` head: `Permissions-Policy` meta (denies all browser capabilities except `fullscreen=(self)`), `Referrer-Policy` meta (`strict-origin-when-cross-origin`).
- `pages.yml` top-level: `permissions: contents: read`. `pages: write` and `id-token: write` ONLY under `deploy.permissions`.

PR C (deferred) will add OpenSSF Scorecard, actionlint workflow, harden-runner audit mode, attest-build-provenance, dependency-review-action. NOT my surface in PR B.

## Learnings

(append as work progresses)
