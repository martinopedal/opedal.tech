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

### PR C session (2025-06-04, feat/garman-hardening)

**SHA-pinning pattern for new GitHub Actions:**
```pwsh
# 1. Fetch latest release tag and commitish
gh api repos/{owner}/{repo}/releases/latest --jq '{tag_name, target_commitish}'
# 2. Resolve tag to commit SHA
gh api repos/{owner}/{repo}/git/refs/tags/{tag} --jq '.object.sha'
# 3. Use SHA in workflow with inline comment: `uses: owner/repo@<SHA> # vX.Y.Z`
```

Applied to:
- `ossf/scorecard-action@99c09fe975337306107572b4fdf4db224cf8e2f2 # v2.4.3`
- `reviewdog/action-actionlint@be0761e4c1bab7cfdfca56cd03d4bb6253e39a4a # v1.72.0`
- `actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294 # v5.0.0`
- `step-security/harden-runner@a5ad31d6a139d249332a2605b85202e8c0b78450 # v2.19.1`
- `actions/attest-build-provenance@a2bbfa25375fe432b6a289bc6b6cd05ecd0c4c32 # v4.1.0`

**JetBrains Mono variable font fallback:**
JetBrainsMono v2.304 ships no variable `.woff2` — only `.ttf` in `fonts/variable/`. Copied `JetBrainsMono-Regular.woff2` (90KB) as fallback, saved to `public/fonts/jetbrains-mono-variable.woff2`. Font-face rule simplified to single weight (400). Documented in THIRD_PARTY_NOTICES.md.

**OFL 1.1 attribution handling:**
Created `THIRD_PARTY_NOTICES.md` at repo root with source URL, license type, vendored path, usage scope, and link to full OFL text. Pattern: vendor the font, document attribution, never inline license text.

**CSP-safe font preload:**
Added `<link rel="preload" as="font" type="font/woff2" href="/fonts/jetbrains-mono-variable.woff2" crossorigin>` to `BaseLayout.astro` head. No `define:vars` — static path only. `crossorigin` required for font preload per spec.

**OG image generation with Pillow:**
Used Python Pillow to generate 1200×630 PNG. Brand colors: bg `#0d1117`, accent `#2f81f7`, text `#e6edf3`. Loaded JetBrains Mono TTF from extracted release for title. Final size: 23.36KB (well under 200KB limit).

**Git lock file trap on parallel commits:**
Parallel `git commit` calls hit `.git/index.lock` contention. Solution: serialize commits with `Start-Sleep -Milliseconds 500` between each, or batch all `git add` + single `git commit`. Sequential is safer for scripted workflows.

**Workflow permissions escalation for attestation:**
Added `attestations: write` and `id-token: write` to `pages.yml` build job's permissions block (previously inherited `contents: read` only). Required for `attest-build-provenance` action.

(append as work progresses)
