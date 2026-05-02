# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository or the opedal.tech website, please report it privately:

- Use GitHub's [private vulnerability reporting](../../security/advisories/new)

Do NOT open a public issue for security vulnerabilities.

## Security Measures

- No secrets committed to source code — all sensitive values managed via GitHub Secrets
- SHA-pinned GitHub Actions (never tag-only pins)
- Dependabot enabled for GitHub Actions dependency updates
- CodeQL scanning on push, PR, and weekly schedule
- Content Security Policy headers configured in GitHub Pages
- HTTPS enforced via GitHub Pages (no HTTP)
