# Now — opedal.tech

**Active branch:** `main` (no in-flight PRs).

**Goal:** Maximum-effort organic ranking for "Martin Opedal" + voice-rule-conformant prose across every customer-facing surface. Site is shipped, schemas are live, OSSF Scorecard is green.

**Status:** PRs #66–#72 merged (SEO + AI discoverability + voice rules + post-deploy polish). Live site verifies at 92/100 on the post-deploy report. All 12 surface URLs return 200. Voice rules now ship with the repo via `.github/copilot-instructions.md` and are referenced in `.squad/skills/voice-rules/SKILL.md`.

**Authoritative reference:** `.squad/decisions.md` (consolidated team decisions), `content/facts.yml` (life-fact source of truth — Martin started with Azure/M365/Entra in 2011, so tenure is 15 years as of 2026), `.github/copilot-instructions.md` (voice rules, security policy, branch protection).

**Open backlog (low-effort, high-leverage):**
- Em-dash sweep across `README.md` and `.github/copilot-instructions.md` (the latter is ironic — it contains the no-em-dash rule but predates it)
- Scribe drain: 22 unmerged decision inbox files in `.squad/decisions/inbox/` need merging into `decisions.md`
- Backlink-recon Tier 1 author signatures on upstream contributions (AVM, ALZ Terraform, AKS modules)
- Sitemap.xml meta-refresh → server-level 301 (cosmetic; current behavior works for major crawlers)

**Martin's manual queue (blocked on him, in `.squad/manual-actions/`):**
1. Apply GitHub profile README (cmd in `github-profile-readme-howto.md`)
2. Sessionize: add opedal.tech to website field (3 min)
3. Bluesky `@opedal.tech` claim via DNS TXT
4. GSC verification + sitemap submit; Bing WMT 1-click import
5. Microsoft Tech Community profile
6. Cervisiam: ask team to add him to team page
