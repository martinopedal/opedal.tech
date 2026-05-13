# opedal.tech

Personal website for [Martin Opedal](https://www.linkedin.com/in/martin-opedal) — Lead Cloud Solution Architect at Microsoft.

Hosted at **[opedal.tech](https://opedal.tech)** via GitHub Pages.

## URLs

| Purpose | URL | When it works |
| ------- | --- | ------------- |
| Live site (canonical) | <https://opedal.tech> | After DNS cutover at Domeneshop (see [SETUP.md §3](SETUP.md)) |
| `www` (redirects to apex) | <https://www.opedal.tech> | After DNS cutover |
| GitHub Pages preview | <https://martinopedal.github.io/opedal.tech/> | As soon as Pages is enabled in [SETUP.md §1](SETUP.md). Once DNS is live, this redirects to the canonical URL. |
| Local dev server | <http://localhost:4321> | While `npm run dev` is running |

The GitHub Pages preview URL is the fastest way to see the live build before DNS is wired up — it works the moment the `Deploy to GitHub Pages` workflow succeeds.

## Stack

- **Astro 5** (static output) — Markdown blog + component-based pages
- **Plain CSS** in `src/styles/global.css` (GitHub dark palette, no external fonts, no CDN)
- **Node 22** (CI only — no client-side runtime)
- **GitHub Pages** with custom domain `opedal.tech`
- **GitHub Actions** builds and deploys on every push to `main` (`.github/workflows/pages.yml`)

## Hosting & domain

| Concern         | Where                                                                    |
| --------------- | ------------------------------------------------------------------------ |
| Source code     | This repo (`martinopedal/opedal.tech`) — public                          |
| Build & deploy  | GitHub Actions → GitHub Pages                                            |
| Canonical URL   | `https://opedal.tech` (apex; `www` redirects here)                       |
| TLS certificate | Let's Encrypt, auto-issued and renewed by GitHub Pages                   |
| Domain registrar / DNS | [Domeneshop](https://domeneshop.no)                               |
| Apex DNS records | 4 × A + 4 × AAAA → GitHub Pages anycast IPs (see [SETUP.md](SETUP.md))  |
| `www` subdomain | `CNAME` → `martinopedal.github.io.`                                      |
| `CNAME` file    | Repo root — tells Pages the canonical host is `opedal.tech`              |

The full Domeneshop walkthrough, IP list, Windows verification commands, and order-of-operations cutover guide are in **[SETUP.md](SETUP.md)**.

## Repository visibility — public, by design

This repository is intentionally **public**. The decision and trade-offs:

- **GitHub Pages on a private repo requires a paid GitHub plan** (Pro/Team/Enterprise). On a Free account, Pages only deploys from public repos.
- **The rendered HTML is public regardless.** A static portfolio site does not gain meaningful security from a private source repo — the same content is served to anyone who hits the URL.
- **Public unlocks free security tooling** at the tier this repo is configured for: CodeQL, Dependabot security updates, secret scanning + push protection, and private vulnerability reporting.
- **The repo doubles as a portfolio artifact.** Visitors can audit the engineering rigor (CSP, SHA-pinned Actions, branch protection, CodeQL) — that is part of the message.
- **Risks are mitigated by policy, not visibility.** No secrets, no customer names, no PII; see `.github/copilot-instructions.md` "Content rules" and [SECURITY.md](SECURITY.md).

If you ever need to host private drafts or non-public content, keep them in a separate private repo or outside the build — don't flip this repo's visibility.

## Security

- CodeQL scanning on push, PR, and weekly schedule (`language: [actions]` — Astro/TS/CSS have no CodeQL extractor; this is expected)
- Dependabot for GitHub Actions and npm updates (weekly)
- SHA-pinned Actions throughout
- Content Security Policy enforced via `<meta http-equiv="Content-Security-Policy">` in `BaseLayout.astro` — `script-src 'none'`, no inline scripts, no external CDN
- HTTPS enforced via GitHub Pages — never link to HTTP resources
- See [SECURITY.md](SECURITY.md) for the vulnerability reporting process

## Local preview

```bash
npm ci
npm run dev      # http://localhost:4321 with HMR
npm run build    # static output to dist/
npm run preview  # serve the built dist/ locally
```

## Adding a blog post

Create `src/content/blog/my-post.md` with frontmatter:

```md
---
title: "Post title"
description: "One-sentence description"
pubDate: 2026-06-01
tags: ["Azure", "Terraform"]
---
```

The content collection schema lives in `src/content/config.ts`.

## Branch protection (`main`)

Configured in Settings → Branches; the full checklist is in [SETUP.md](SETUP.md). Summary:

- Require a pull request before merging (0 required reviewers — solo-maintained)
- Required status checks: `Analyze (actions)` (CodeQL) and `Build Astro site` (pages.yml)
- Require linear history; no force pushes; no deletions
- `enforce_admins = true`
- Signed commits **not** required (would break Dependabot and GitHub API commits)
