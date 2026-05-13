# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository or in the live site at `opedal.tech`, please report it privately:

- Use GitHub's [private vulnerability reporting](https://github.com/martinopedal/opedal.tech/security/advisories/new)

Do **not** open a public issue for a security vulnerability.

You can expect:

- An acknowledgement within 5 business days
- A triage outcome (accepted / declined / out-of-scope) within 14 days of acknowledgement
- A coordinated fix and disclosure for accepted reports

## Scope

In scope:

- Cross-site scripting or content-injection in the rendered site
- Subresource integrity issues introduced by the build pipeline
- Supply-chain compromise of dependencies declared in `package.json` or workflow actions
- Misconfiguration of GitHub Pages / DNS / TLS that affects users of `opedal.tech`
- Workflow privilege-escalation, secret-exfiltration, or token-leak vectors in `.github/workflows/`

Out of scope:

- Findings in third-party services that the site links to (LinkedIn, GitHub, Microsoft Learn, etc.)
- Social engineering, phishing, or physical attacks
- Reports requiring privileged access already granted to the maintainer
- Best-practice findings that don't translate to an exploitable issue (e.g. missing HSTS preload, theoretical clickjacking on a JS-free page)

## Security Measures

- No secrets committed to source code — all sensitive values managed via GitHub Secrets
- SHA-pinned GitHub Actions (never tag-only pins); Dependabot keeps the pins fresh
- Dependabot enabled for GitHub Actions and npm, including security-update PRs
- Vulnerability alerts and private vulnerability reporting both enabled
- Secret scanning + push protection enforced on all branches
- CodeQL scanning of GitHub Actions workflows on push, PR, and a weekly schedule
- Content Security Policy (CSP) enforced via `<meta http-equiv="Content-Security-Policy">` in every page: `script-src 'none'`, no inline scripts, no external CDN
- Every external link uses `rel="noopener noreferrer"`
- HTTPS enforced via GitHub Pages; HTTP is never referenced in source

## OSSF Scorecard

This repository is monitored by [OSSF Scorecard](https://securityscorecards.dev/). Current aggregate score and per-check breakdown: [securityscorecards.dev/viewer/?uri=github.com/martinopedal/opedal.tech](https://api.securityscorecards.dev/projects/github.com/martinopedal/opedal.tech)

**Target score: ~8.5/10** (realistic ceiling for a solo-maintained static site with no releases)

### Score Plateau Reality

This repo will plateau at ~8.5/10 due to unavoidable constraints:

- **Contributors (3/10)**: Solo-maintained by @martinopedal. No external contributors from multiple organizations. This is expected for a personal site.
- **Code-Review (varies)**: Copilot code review provides automated analysis. Human review happens only on Copilot-authored PRs. Solo repos don't have multi-org reviewer diversity that Scorecard weights heavily.
- **Maintained (0/10)**: Repo < 90 days old (created 2026-02-13). Auto-fixes to 10/10 after 2026-08-11.
- **Fuzzing (0/10)**: Static site with no server runtime, no binaries, no parsers processing untrusted input. Fuzzing is N/A. Documented below.
- **CII-Best-Practices (0/10)**: Badge application is manual. Self-assessment checklist exists in `.squad/decisions/inbox/loomis-cii-checklist-2026-05-13.md` but badge requires human submission.
- **Signed-Releases (-1)**: No releases (continuous deployment from `main`). `-1` means "no signal", not a deduction.
- **Packaging (-1)**: No package publishing workflow (static site, not a library). `-1` means "no signal", not a deduction.
- **Vulnerabilities (8/10)**: 2 dismissed Astro alerts (false positives for static output mode). Should clear on next scan.

### Branch Protection (rulesets + review gate)

**Migrated 2026-05-13**: Classic branch protection → GitHub rulesets (ID 16364777) + 1 required approving review.

**Active ruleset**:
- ✅ Require 1 approving review before merge (Martin or Copilot)
- ✅ Require status checks: `Analyze (actions)`, `Build Astro site`, `request-copilot-review`
- ✅ Only allow squash merges (no merge commits, no rebase)
- ✅ Require linear history
- ✅ Block force pushes (`non_fast_forward`)
- ✅ Block branch deletion
- ❌ Require signed commits: **disabled** (breaks Dependabot auto-merge and GitHub API commits)

**No bypass actors**: Even admins (Martin) must follow the gate. No `--admin` overrides.

**Review process**:
1. **Martin's PRs**: Copilot code review auto-analyzes the diff and approves if no concerns. If Copilot flags issues, Martin reviews the feedback and either fixes or overrides via manual review.
2. **Copilot-authored PRs** (@copilot or copilot-swe-agent[bot]): Martin reviews manually via GitHub web UI.

To verify: `gh api repos/martinopedal/opedal.tech/rulesets/16364777`

**Why rulesets?**
- Classic branch protection requires `admin` scope to read via API, causing Scorecard's `GITHUB_TOKEN` to fail with `-1`
- Rulesets are readable with default `contents: read` workflow permissions
- Functionally equivalent protection, better token visibility

### Fuzzing (0/10)

This project does **not** use fuzzing, and Scorecard correctly reports 0/10. Rationale:

- **No server runtime**: This is a static Astro site compiled to HTML/CSS at build time and served via GitHub Pages CDN. No Node.js, Python, or server-side code runs in production.
- **No binary attack surface**: The site generates plain HTML files with no executable binaries, no parsers processing untrusted input at runtime, and no client-side JavaScript (`script-src 'none'` CSP).
- **Build-time only**: The build pipeline (`npm run build`) processes Markdown and Astro components in a controlled CI environment, not user input.

Fuzzing targets programs that parse untrusted input at runtime (compilers, parsers, image decoders, network protocols). A static website with no runtime input processing and no binaries does not benefit from fuzz testing.

### Signed-Releases (-1) and Packaging (-1)

**Signed-Releases**: This repo uses continuous deployment from `main` to GitHub Pages. No formal releases are cut. Score `-1` means "no signal" (Scorecard skips this check), not a deduction from the aggregate.

**Packaging**: This is a static website, not a published package or library. No npm/PyPI/Maven publishing workflow exists. Score `-1` means "no signal", not a deduction.

### CII Best Practices Badge (0/10)

This project is working toward the [OpenSSF Best Practices Badge](https://www.bestpractices.dev/). Application is pending. See `.squad/decisions/inbox/loomis-cii-checklist-2026-05-13.md` for the self-assessment checklist.

Badge URL (once approved): `https://www.bestpractices.dev/projects/<ID>`