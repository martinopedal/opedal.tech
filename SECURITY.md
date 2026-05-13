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

### Branch Protection Score (now using rulesets)

**Migration completed 2026-05-13**: Converted from classic branch protection to GitHub rulesets. Rulesets are readable by default workflow tokens (no admin scope required), which should resolve the Scorecard `-1` token visibility issue.

**Active ruleset** (ID 16364777, `main branch protection`):
- ✅ Require pull request before merging (0 required reviewers, solo-maintained)
- ✅ Require status checks: `Analyze (actions)`, `Build Astro site`, `request-copilot-review`
- ✅ Require linear history (`required_linear_history`)
- ✅ Block force pushes (`non_fast_forward`)
- ✅ Block branch deletion (`deletion`)
- ❌ Require signed commits: **disabled** (breaks Dependabot auto-merge and GitHub API commits)

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

### CII Best Practices Badge (0/10)

This project is working toward the [OpenSSF Best Practices Badge](https://www.bestpractices.dev/). Application is pending. See `.squad/decisions/inbox/loomis-cii-checklist-2026-05-13.md` for the self-assessment checklist.

Badge URL (once approved): `https://www.bestpractices.dev/projects/<ID>`