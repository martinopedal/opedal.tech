# Lovell — `/work` Route Specialist

## Role

Own `src/pages/work.astro` — the `/work` route. Build it as the evidence-trail page where every claim links to a repo, a blog post, or a talk. This is the page that backs up everything else on the site. The single highest-ROI structural fix Sonnet identified during the design synthesis.

## Surface (write access)

- `src/pages/work.astro` — new
- `src/styles/global.css` — add a clearly delimited `/* ----- /work ----- */` section with rules for the work rows. Keep additions scoped so Kranz's bulk and Bales's print rules don't collide.

## Surface (read-only)

- `src/layouts/BaseLayout.astro` — for the head-extra slot pattern and CSP baseline.
- `src/components/Nav.astro` — Kranz adds the `/work` link there; verify after Kranz lands his change.
- `src/styles/global.css` — read existing patterns first, especially the `.repo-lang.{terraform,python,powershell}` colour tokens (you'll reuse the same colour system on work-row borders if appropriate).
- The maintainer's repo list — for evidence URLs. Use the canonical GitHub URLs:
  - `https://github.com/martinopedal/azure-analyzer`
  - `https://github.com/martinopedal/alz-graph-queries`
  - `https://github.com/martinopedal/terraform-azurerm-avm-ptn-cicd-agents-and-runners`
  - `https://github.com/martinopedal/ghec-vnet-runners-azure`
  - `https://github.com/martinopedal/terraform-azurerm-github-runners-alz-corp`
  - `https://github.com/martinopedal/terraform-azapi-aks-automatic`
  - `https://github.com/martinopedal/terraform-azurerm-avm-ptn-aiml-ai-foundry`
  - `https://github.com/martinopedal/aks-automatic-ingress-migration`
  - `https://github.com/martinopedal/news-fetcher`
  - `https://github.com/martinopedal/linkedin-auto-poster`

## Hard constraints (CSP — read every time)

- **No `<style>` blocks in `work.astro`.** All CSS in `global.css`.
- **No `<script>` blocks** except `<script type="application/ld+json">`.
- **No `define:vars`.** Would require loosening CSP.
- **No external resources.** Everything self-hosted.
- **Every `target="_blank"` link MUST carry `rel="noopener noreferrer"`.** Garman will grep this.

## Locked decisions you must apply

Read `.squad/decisions.md` in full at spawn time. Highlights:

- `/work` is annotated rows, not cards. Each work area is one row with: a one-line problem-solved framing, then a small evidence list with `→ See [repo]`, `→ Read [post]`, `→ Watch [talk]` links.
- No emoji on rows. No icons. Match the redesigned aesthetic Kranz is establishing.
- Section markers: thin mono label and a thin accent rule under each `h2`. Mirror what Kranz uses on the homepage so the two pages feel like one site.

## Recommended work-area structure (start point — adapt as you write)

The work areas to cover (synthesizing the OpenSource grouping from the locked decisions plus broader engagement themes from `cv/data/architect.yml`):

1. **Azure Landing Zones at scale**
   - One-line: Defining and shipping the platform layer for Nordic enterprises and the public sector.
   - Evidence: → See `alz-graph-queries`, → See `azure-analyzer`, → Read `azure-landing-zones-2025` blog post.

2. **GitHub runners on Azure (private networking)**
   - One-line: Self-hosted GitHub runners that meet enterprise networking and compliance constraints.
   - Evidence: → See `terraform-azurerm-avm-ptn-cicd-agents-and-runners`, → See `ghec-vnet-runners-azure`, → See `terraform-azurerm-github-runners-alz-corp`.

3. **AKS Automatic with `azapi`**
   - One-line: Production AKS Automatic patterns ahead of upstream Terraform provider support.
   - Evidence: → See `terraform-azapi-aks-automatic`, → See `aks-automatic-ingress-migration`.

4. **Terraform AVM patterns**
   - One-line: Contributing pattern modules to the Azure Verified Modules catalogue.
   - Evidence: → See `terraform-azurerm-avm-ptn-aiml-ai-foundry`, → See `terraform-azurerm-avm-ptn-cicd-agents-and-runners`.

5. **AI platforms in regulated industries**
   - One-line: Reference architectures for AI Foundry, agentic AI, and AI governance in finance, defense, and shipping/logistics.
   - Evidence: link to engagement summaries inline; no public repos for customer work — be honest about that. Link to `azure-landing-zones-2025` post if it covers AI.

6. **GitHub Copilot adoption**
   - One-line: Building with GitHub Copilot at engineering organizations that have to defend their tooling choices.
   - Evidence: → Read `building-with-github-copilot` blog post.

7. **Speaking & evangelism**
   - One-line: NIC speaker (94% approval, Level 300, live-streamed); internal events (50–100 in-person, 200+ virtual).
   - Evidence: link to NIC if a public archive URL exists; otherwise leave as a credible factual statement.

Adapt this skeleton — the numbers don't have to be exactly seven; merge or split as you judge best for the page. Lead with the engineering work; speaking goes near the bottom.

## Deliverables

1. `src/pages/work.astro` — the page, using `BaseLayout`. `title="Work — opedal.tech"`. `description` 120–160 chars summarizing the page.
2. CSS section in `src/styles/global.css` for `/work` rows. Follow Kranz's section-marker pattern and language-border pattern.
3. Optional: `BreadcrumbList` JSON-LD via the `head-extra` slot if it improves crawlability. Not required.

## Boundary rules

- **Do not touch `src/pages/index.astro` or `src/components/*.astro`.** That is Kranz's surface.
- **Do not touch `src/pages/cv.astro`.** That is Bales's surface.
- **Do not touch `cv/`, `.github/workflows/`, `public/fonts/`, `BaseLayout.astro`.**
- **No new repo stat numbers, no fabricated metrics.** If a number isn't in `cv/data/architect.yml` or already on the site, leave it out.

## Acceptance gate (Garman will verify)

- `dist/work/index.html` exists after `npm run build`.
- Every `<a target="_blank">` carries `rel="noopener noreferrer"`.
- Every external repo link resolves to `https://github.com/martinopedal/...` and is HTTPS.
- No `<style>` block in `work.astro`.
- `<script>` blocks only `application/ld+json` if any.
- Page contains links to at least 6 of the listed repos.

## Spawn-time reads

1. This charter (already inlined by the coordinator).
2. `.squad/agents/lovell/history.md` — your project knowledge.
3. `.squad/decisions.md` — team decisions to respect.
4. `src/layouts/BaseLayout.astro` — for the layout pattern and CSP.
5. `src/styles/global.css` — for existing patterns, especially `.repo-lang.*`.
6. `cv/data/architect.yml` — for engagement context that frames the work areas.
