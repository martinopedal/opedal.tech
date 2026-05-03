# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository or the opedal.tech website, please report it privately:

- Use GitHub's [private vulnerability reporting](../../security/advisories/new)

Do NOT open a public issue for security vulnerabilities.

## Security Measures

- No secrets committed to source code — all sensitive values managed via GitHub Secrets
- SHA-pinned GitHub Actions (never tag-only pins)
- Dependabot enabled for GitHub Actions and npm dependency updates and security alerts
- CodeQL scanning on push, PR, and weekly schedule
- Secret scanning and push protection enabled
- Content Security Policy (CSP) enforced via `<meta http-equiv="Content-Security-Policy">` in every page — `script-src 'none'`, no inline scripts, no external CDN
- HTTPS enforced via GitHub Pages (no HTTP)
