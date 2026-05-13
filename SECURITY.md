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
