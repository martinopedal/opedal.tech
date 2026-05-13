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

### Linkcheck gate session (2025-06-13, feat/ci-linkcheck)

**Lychee configuration for Astro static site:**
- Used `lycheeverse/lychee-action@8646ba30535128ac92d33dfc9133794bfdd9b411 # v2.8.0`
- Config in `lychee.toml` at repo root — DO NOT use `base = "dist"` option (invalid TOML key)
- Must pass `--base dist/` as CLI arg to resolve root-relative links (`/cv`, `/blog`, `/fonts/...`)
- Config keys that worked: `max_concurrency`, `timeout`, `max_retries`, `user_agent`, `scheme`, `exclude`, `accept`, `include_fragments`

**Upload-pages-artifact tarball extraction gotcha:**
`actions/upload-pages-artifact` packages `dist/` as `artifact.tar`, not raw files. Linkcheck job must:
1. Download artifact with `actions/download-artifact@v8`
2. Extract: `mkdir -p dist && tar -xf dist-artifact/artifact.tar -C dist`
3. Then run lychee on extracted `dist/`

**Deploy gating pattern (linkcheck between build and deploy):**
```yaml
jobs:
  build:
    steps:
      - name: Upload artifact
        if: github.event_name == 'push' || github.event_name == 'workflow_dispatch' || github.event_name == 'pull_request'
        uses: actions/upload-pages-artifact@SHA
        with:
          path: dist/

  linkcheck:
    needs: build
    if: github.event_name == 'push' || github.event_name == 'workflow_dispatch' || github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@SHA
      - uses: actions/download-artifact@SHA
        with:
          name: github-pages
          path: dist-artifact
      - run: tar -xf dist-artifact/artifact.tar -C dist
      - uses: lycheeverse/lychee-action@SHA
        with:
          args: --base dist/ --config lychee.toml --no-progress dist/
          fail: true

  deploy:
    needs: [build, linkcheck]  # blocks deploy if linkcheck fails
    if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
```

Conditional match: upload artifact on PRs so linkcheck can validate before merge, but deploy only on push/workflow_dispatch.

**Social media domain exclusion for CI link checkers:**
LinkedIn, Twitter/X, Instagram, Facebook all return 999/403 to crawler user agents. Must exclude in `lychee.toml`:
```toml
exclude = [
  "^https?://(www\\.)?linkedin\\.com",
  "^https?://(www\\.)?twitter\\.com",
  "^https?://(www\\.)?x\\.com",
  "^https?://(www\\.)?instagram\\.com",
  "^https?://(www\\.)?facebook\\.com",
]
accept = [200, 201, 202, 203, 204, 206, 301, 302, 304, 308, 999]
```

**Lychee report artifact path:**
Action outputs to `lychee/out.md` by default, but uploads just `out.md` to artifact root. Download with:
```yaml
- uses: actions/upload-artifact@SHA
  if: always()
  with:
    name: lychee-report
    path: lychee/out.md
```

### Fact-check system session (2025-06-13, chore/fact-check-ci)

**Registry-plus-regex pattern for tenure claims:**
Created `content/facts.yml` as source of truth for career timeline and life-facts, paired with `scripts/check-facts.mjs` that walks `src/` and applies targeted regex checks. Registry mirrors `cv/data/architect.yml` (the authoritative source for career data) and computes derived facts at run-time (years_with_azure_entra_m365, years_at_microsoft, years_at_teknograd). Checker validates:
- Tenure claims (`(\d+|word)\+?\s*years?`) — flags any numeric or word-form claim that doesn't match a known derived value
- Employer-specific claims (`(\d+)\s+years?\s+at\s+(\w+)`) — cross-checks against YAML
- Venture counts (`co-?founded\s+(\w+)\s+brewer`) — validates against `ventures.breweries_cofounded`

**Word-to-number mapping critical for natural prose:**
Initial regex only caught digits (`\d+`), missed word-form claims like "thirty years" or "nine years". Added `wordToNum` map covering one through fifty, updated tenure regex to `(\d+|one|two|...|fifty)\+?\s*years?`. Prose naturally uses words for small numbers (nine, fifteen, two), digits for larger ones (2024, 135). Checker must handle both.

**High-signal exclusion patterns prevent false positives:**
Excluded CSS numeric values (`width|height|padding|...:\s*\d+`), ISO dates in blog frontmatter (`\d{4}-\d{2}-\d{2}`), Node versions in workflows (`node-version:\s*\d+`). False-positive rate must stay near-zero or the check gets ignored. Pattern: exclude by regex, not by line number (more maintainable as files evolve).

**Source-of-truth split: content/facts.yml mirrors cv/data/architect.yml:**
Career timeline facts (microsoft_start_year, teknograd_start_year) live in `cv/data/architect.yml` (parsed by both LaTeX pipeline and /cv HTML page). `content/facts.yml` mirrors them for the fact-checker. When both files contain the same fact, `architect.yml` is authoritative. Minimizes drift surface: one editor updates both, or updates `architect.yml` and the fact-checker re-validates copy against the new value.

**Fact-check complements cspell, not replaces semantic review:**
Martin caught "I ran datacenters for nine years before joining Microsoft" — numerically correct (Teknograd 2011–2020 = 9 years), semantically wrong (he worked *with* datacenters, Azure, M365, and Entra simultaneously, not in sequence). The fact-checker validates numeric claims against a registry; it doesn't parse meaning. Connell fixes the semantic issue in `content/about-timeline-fix`. The checker is the second line of defense after human verification, catching future hallucinations when an agent or Martin writes "30 years at Microsoft" or "co-founded five breweries."

**CI workflow paired with npm script for local pre-flight:**
`.github/workflows/fact-check.yml` triggers on `pull_request` and `push` for `src/**`, `content/**`, `cv/data/**` changes. Runs `node scripts/check-facts.mjs` (exit 0 = pass, exit 1 = fail with report). Added `"check:facts": "node scripts/check-facts.mjs"` to `package.json` so Martin can run locally before pushing. Pattern: every CI gate should have a local-run equivalent.

**Zero false positives on first test run:**
Ran checker against current `src/` tree — passed cleanly. Injected fake claim "thirty years" — caught and reported with file path, line number, claimed value, and expected values. Reverted to "nine years" — passed again. No tuning iterations needed; exclusion patterns were sufficient out of the gate.

(append as work progresses)
