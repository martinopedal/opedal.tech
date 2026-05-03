# opedal.tech

Personal website for [Martin Opedal](https://www.linkedin.com/in/martin-opedal) — Lead Cloud Solution Architect at Microsoft.

Hosted at **[opedal.tech](https://opedal.tech)** via GitHub Pages.

## Stack

- Static HTML + CSS — no build system, no npm, no Jekyll
- Custom domain: `opedal.tech`
- Deployed via GitHub Actions on every push to `main`

## Security

- CodeQL scanning on push, PR, and weekly schedule
- Dependabot for GitHub Actions updates
- SHA-pinned Actions throughout
- See [SECURITY.md](SECURITY.md) for the vulnerability reporting process

## Local preview

Open `index.html` in a browser — no build step required.

## Branch protection

Configure in Settings → Branches → main:
- Require status checks: `Analyze (actions)`
- Require linear history
- Include administrators
