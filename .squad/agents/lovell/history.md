# Lovell — history

## Core Context

- **Project:** `martinopedal/opedal.tech` — personal site for Martin Opedal (Lead Cloud Solution Architect at Microsoft, Oslo).
- **Stack:** Astro 5 (static), GitHub dark palette, JS-free.
- **Maintainer:** Martin Opedal (`martinopedal`).
- **My role:** `/work` Route Specialist. I own `src/pages/work.astro` and the corresponding CSS section.
- **My branch context:** working on `feat/cv-and-redesign` (PR B).

## Why `/work` exists

The homepage Work component currently links nowhere. Sonnet flagged it as the highest-ROI structural fix. `/work` is the evidence-trail page that backs every claim with a repo, blog post, or talk link. Annotated rows, not cards.

## What I know about the work areas

The maintainer's public repos (canonical URLs `https://github.com/martinopedal/{name}`):
- `azure-analyzer` — 30-tool Azure assessment runner with Schema 2.2 unified findings.
- `alz-graph-queries` — ARG queries for ALZ checklist gaps.
- `terraform-azurerm-avm-ptn-cicd-agents-and-runners` — AVM pattern for CI/CD runners.
- `ghec-vnet-runners-azure` — GitHub-hosted runners with Azure VNET integration.
- `terraform-azurerm-github-runners-alz-corp` — self-hosted runners on ACA for ALZ Corp.
- `terraform-azapi-aks-automatic` — AKS Automatic with `azapi` provider.
- `terraform-azurerm-avm-ptn-aiml-ai-foundry` — AVM pattern for AI Foundry.
- `aks-automatic-ingress-migration` — AKS automation tooling.
- `news-fetcher` — Azure news fetcher and LinkedIn post drafter.
- `linkedin-auto-poster` — LinkedIn posting automation.

Blog posts already in the site:
- `azure-landing-zones-2025`
- `building-with-github-copilot`

Speaking credibility (from `cv/data/architect.yml`):
- NIC speaker: 94% approval, Level 300, live-streamed.
- Microsoft internal events: 50–100 in-person, 200+ virtual.

## What I do NOT touch

- `src/components/*.astro` and `src/pages/index.astro` — Kranz.
- `src/pages/cv.astro` — Bales.
- `cv/`, `.github/workflows/`, `public/fonts/`, `BaseLayout.astro`.

## Hygiene

- Every `target="_blank"` carries `rel="noopener noreferrer"`. Garman will grep this.
- No fabricated metrics. If a number isn't in `architect.yml` or already on the site, leave it out.

## Learnings

- **PR B shipped:** `/work` route live in PR #12. Evidence-trail page backs work areas with annotated rows + evidence links (`→ See [repo]` / `→ Read [post]` / `→ Watch [talk]`). Replaced card grid design per consensus direction.
- **Section markers:** thin mono labels + thin accent rule under each `h2`. Language-specific 2px left borders on repo rows (terraform `#844fba`, python `#3fb950`, powershell `#5391fe`, etc.).

