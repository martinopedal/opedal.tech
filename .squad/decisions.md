# Decisions — opedal.tech

Authoritative decision ledger. Append-only. Drop-box pattern: agents write to `.squad/decisions/inbox/{agent}-{slug}.md`; Scribe merges into this file.

---

## 2026-05-13: PR B kickoff — Apollo MOCR cast, three-commit bootstrap

**By:** Martin Opedal (via Copilot)
**What:** Stand up a five-specialist Squad for PR B (`feat/cv-and-redesign`) using the Apollo Mission Control universe. Cast: Aaron (CV pipeline), Bales (CV HTML page), Kranz (site redesign), Lovell (`/work` route), Garman (typography + verification). Bootstrap workspace in three sequential commits before specialists fan out.
**Why:** PR B is a checklist-heavy build pipeline plus a redesign with hard CSP flight rules and a verification gate. Apollo MOCR maps the work shape directly. Three commits (vendor LaTeX, define YAML, scaffold + harden) keep the diff readable for solo review.

## 2026-05-13: Locked content redactions for `cv/data/architect.yml`

**By:** Martin Opedal (via Copilot)
**What:**
- REMOVE phone `+47 454 20 483` everywhere (LaTeX, HTML CV, homepage Contact).
- Email switched to `hello@opedal.tech` alias (forwarded by Domeneshop to a private inbox).
- SOFTEN "Top revenue contributor with multi-million dollar targets, pipeline ownership, forecasting" → "Strategic accounts portfolio across regulated Nordic enterprises".
- Drop redundant "Revenue-accountable with multi-million dollar targets" sentence from professional summary.
- KEEP verbatim: 48M+ NOK consultant portfolio, Tier-1 Nordic Bank, Defense Contractor, Government Bodies, NIC speaker (94% approval, Level 300, live-streamed).
**Why:** No phone in public; no Microsoft-internal Connect-style sales-language phrasing in a public CV; verifiable anonymized metrics retained for credibility.

## 2026-05-13: Locked design decisions (3-model consensus)

**By:** Martin Opedal (via Copilot) — synthesizing review by Claude Opus 4.7, GPT-5.5, Claude Sonnet 4.6
**What:**
- KEEP hero eyebrow `Lead Cloud Solution Architect · Microsoft`.
- Primary CTA `View open source` → `/work` (or `#open-source`). Secondary CTA `Email me` → `mailto:hello@opedal.tech`.
- Multi-page site: add `/cv` and `/work` routes in addition to homepage. Skip `/now`.
- KEEP small/subtle name gradient (`#2f81f7 → #58a6ff`).
- DROP emoji on Work / OpenSource / Speaking cards. Do NOT replace with Octicons.
- OpenSource: replace card grid with grouped annotated rows by problem domain. Drop hardcoded star counts. 2px coloured left border per language extending the existing `.repo-lang.{terraform,python,powershell}` pattern.
- Work: replace card grid with annotated rows. Each work area gets `→ See [repo]` / `→ Read [post]` / `→ Watch [talk]` evidence links.
- Typography: KEEP system fonts for body. ADD JetBrains Mono self-hosted (~30KB woff2) for code blocks only. DO NOT add Inter/Geist.
- OG image: static one-time `og-default.png`. Skip Satori per-post (only 2 posts today).
- Section markers: thin mono labels and a thin accent rule under each `h2`. `01/02/03` numbering optional.
- Print stylesheet for `/cv`: hide nav, white background, black text, `page-break-before` on each `h2`.
**Why:** Recorded so all five specialists apply the same direction without re-deciding mid-PR.

## 2026-05-13: Repo grouping for OpenSource section

**By:** Martin Opedal (via Copilot)
**What:** Group `OpenSource.astro` rows by problem domain:
- **Azure governance & assessment**: `azure-analyzer`, `alz-graph-queries`
- **GitHub runners & private networking**: `terraform-azurerm-avm-ptn-cicd-agents-and-runners`, `ghec-vnet-runners-azure`, `terraform-azurerm-github-runners-alz-corp`
- **Terraform platform modules**: `terraform-azapi-aks-automatic`, `terraform-azurerm-avm-ptn-aiml-ai-foundry`
- **AKS automation**: `terraform-azapi-aks-automatic`, `aks-automatic-ingress-migration`
- **Other tooling**: `news-fetcher`, `linkedin-auto-poster`
**Why:** Sells the work as a coherent platform-engineering portfolio rather than a flat list.

## 2026-05-13: Hardening folded into bootstrap commit 3

**By:** Martin Opedal (via Copilot)
**What:** Pure-additive baseline hardening shipped with the squad scaffold:
- `public/.well-known/security.txt` (RFC 9116, 1-year Expires).
- `Permissions-Policy` meta in `BaseLayout.astro` head — denies all browser capabilities except `fullscreen=(self)`. Documented limitation: `<meta http-equiv>` ignored by Firefox/Safari, honoured by Chromium.
- `Referrer-Policy` meta in `BaseLayout.astro` head — `strict-origin-when-cross-origin`.
- `pages.yml` permissions tightening: top-level becomes `contents: read` only; `pages: write` and `id-token: write` scoped to `deploy` job.
**Why:** Defense-in-depth, RFC-conforming security contact channel, principle of least privilege on the deploy workflow. Zero risk to `npm run build`.

## 2026-05-13: PR C scope deferred (NOT to be touched in PR B)

**By:** Martin Opedal (via Copilot)
**What:** OpenSSF Scorecard, `actionlint`, `step-security/harden-runner` audit mode, `actions/attest-build-provenance`, `actions/dependency-review-action`. Queued for PR C after PR B merges.
**Why:** Scope discipline — no specialist drift into security tooling not on PR B's surface.

## 2026-05-13: `.squad/` ships in PR B

**By:** Martin Opedal (via Copilot)
**What:** The squad coordination state (`.squad/**`) is committed as part of PR B. The squash commit will absorb it cleanly.
**Why:** The team that built the PR ships with the PR. Cleaner than splitting into a tiny pre-PR.
