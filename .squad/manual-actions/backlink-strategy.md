# Backlink Strategy — 90-Day Earned Media Plan

**Context**: opedal.tech currently has ~0 organic backlinks beyond LinkedIn/GitHub. These actions build a sustainable earned media pipeline using Martin's existing content (blog drafts from Schmitt2) and reputation as a Microsoft Lead CSA + NIC speaker.

**Goal**: 15–25 high-quality backlinks within 90 days from Nordic/Azure/infrastructure communities, developer forums, and industry publications.

**Coordination**: This plan assumes Schmitt2 (blog content agent) ships ALZ Terraform, AKS Automatic, and AI Foundry blog posts within 30 days. If drafts are delayed, delay backlink submissions until content is live.

---

## Phase 1: Direct Submissions (Days 1–30)

### 1.1 Nordic Tech Publications (Target: 3 backlinks)

These are Norwegian/Nordic publications with tech sections. Martin's local credentials (Microsoft Norway, 15+ years, NIC speaker) give him credibility for pitches.

| Publication | Audience | Pitch Angle | Contact Method |
|-------------|----------|-------------|----------------|
| **Kode24** (<https://www.kode24.no>) | Norwegian developers, 200K+ monthly readers | "Why Norwegian banks are moving to Azure Landing Zones: a Lead CSA's field notes" — 800-word piece on ALZ adoption in FSI | Email: <tips@kode24.no> OR submit via <https://www.kode24.no/tips-oss> |
| **Computerworld Norway** (<https://www.cw.no>) | IT decision-makers, enterprise architects | "AKS Automatic in regulated industries: lessons from Nordic defense contractors" — 1000-word technical deep dive | Email: <redaksjon@cw.no> OR LinkedIn DM to editors (Martin already connected?) |
| **Microsoft Norge Blog** (<https://news.microsoft.com/nb-no/>) | Microsoft customers, partners, local ecosystem | "Landing Zones and AI Foundry: a Norwegian Lead CSA's toolkit" — guest post or interview | Contact local Microsoft Norge PR team (Martin has internal contacts) |
| **Cloud Native Norway Meetup** (<https://www.meetup.com/cloud-native-norway/>) | DevOps/K8s community | Submit talk proposal for 2026 Q3/Q4: "AKS Automatic vs DIY AKS: a production readiness comparison" — blog post becomes speaker page bio link | Email organizers via Meetup OR post in Slack (if Martin is member) |
| **Nordic APIs** (<https://nordicapis.com>) | API architects, platform engineers | "Securing AKS with Azure Firewall + GitHub Actions: a reference architecture" — technical tutorial | Submit via <https://nordicapis.com/write-for-us/> |

**Action steps**:
1. Draft pitch emails using Martin's plain voice (no "leveraging," no humble-brag)
2. Include 2–3 sentence bio + link to opedal.tech/cv as credibility anchor
3. Mention NIC talk (94% approval, Level 300, live-streamed) + Microsoft Lead CSA role in every pitch
4. If accepted, ensure byline includes "Martin Opedal is a Lead Cloud Solution Architect at Microsoft Norway. Read more at opedal.tech."

**Template pitch email** (adapt per publication):

```
Subject: Guest post pitch: [specific title relevant to their audience]

Hi [Editor Name],

I'm Martin Opedal, Lead Cloud Solution Architect at Microsoft Norway. I've spent 15 years architecting Azure platforms for Nordic banks, government agencies, and defense contractors. I spoke at Nordic Infrastructure Conference this year on Terraform and infrastructure-as-code security (94% approval rating, Level 300 session).

I'd like to pitch a [600/800/1000]-word piece for [Publication Name] on [specific topic]:

[2-3 sentence outline — what the piece covers, why it matters to their audience, what readers will learn]

I write at opedal.tech about Landing Zones, AKS, and platform engineering. I can deliver the draft within [timeframe] and include code samples, architecture diagrams, or customer anonymized case studies as needed.

Would this fit your editorial calendar?

Martin Opedal
opedal.tech | linkedin.com/in/martin-opedal
```

---

### 1.2 Developer Communities (Target: 5 backlinks)

These are high-traffic forums where Martin's blog posts can be submitted as standalone links (not promotional spam — genuine technical content with discussion value).

| Platform | Audience | Submission Strategy | URL |
|----------|----------|---------------------|-----|
| **Hacker News** (<https://news.ycombinator.com>) | 500K+ daily developers, startup founders | Submit "Azure Landing Zones with Terraform: a field guide from 50+ customer engagements" with title "Show HN: Field notes on ALZ adoption in Nordic FSI" | <https://news.ycombinator.com/submit> |
| **Reddit /r/AZURE** (<https://www.reddit.com/r/AZURE/>) | 150K+ Azure practitioners | Submit ALZ Terraform post as "I'm a Microsoft Lead CSA. Here's what I've learned from 50+ Landing Zone deployments." — include AMA offer in comments | Direct link post |
| **Reddit /r/devops** (<https://www.reddit.com/r/devops/>) | 400K+ DevOps engineers | Submit AKS Automatic post as "AKS Automatic vs DIY AKS: production readiness comparison from Nordic defense contractors" | Direct link post |
| **Reddit /r/kubernetes** (<https://www.reddit.com/r/kubernetes/>) | 200K+ K8s users | Submit AKS + GitHub Actions post as "Securing AKS egress with Azure Firewall + GitHub self-hosted runners: reference architecture" | Direct link post |
| **Lobsters** (<https://lobste.rs>) | 10K+ senior engineers (invite-only, but high quality) | Submit AI Foundry post as "AI Foundry in air-gapped environments: lessons from Nordic government" — request invite from existing member (Martin may know someone via NIC network) | <https://lobste.rs/submit> (requires invite) |

**Rules**:
- **Do NOT submit all posts on the same day** — space submissions 7–14 days apart to avoid looking like a promotional campaign
- **Engage in comments** — Martin should reply to technical questions, offer follow-up links to GitHub repos, acknowledge critiques
- **No self-promotion in titles** — focus on value ("Here's what I learned") not credentials ("I'm a Lead CSA")
- **Timing**: Submit during US East Coast work hours (14:00–18:00 CET) for HN/Reddit to maximize initial upvotes

---

### 1.3 "Awesome" Lists and Curated Directories (Target: 3 backlinks)

These are GitHub repos that curate links to high-quality resources. PRs to add opedal.tech are accepted if the content is genuinely valuable.

| List | Audience | PR Strategy | URL |
|------|----------|-------------|-----|
| **awesome-azure** (<https://github.com/kristofferandreasen/awesome-azure>) | 5K+ stars, Azure developers | Add opedal.tech to "Blogs" section under "Personal blogs by Azure practitioners" — include 1-sentence description: "Lead CSA at Microsoft Norway writing about Landing Zones, AKS, and Terraform" | Fork → edit `README.md` → PR |
| **awesome-terraform** (<https://github.com/shuaibiyy/awesome-terraform>) | 5K+ stars, Terraform users | Add opedal.tech/work to "Community Modules" or "Blogs" section — link to specific Terraform repos (AVM patterns, AKS module, ALZ tooling) | Fork → edit `README.md` → PR |
| **awesome-aks** (<https://github.com/kristofferandreasen/awesome-aks>) | 1K+ stars, AKS practitioners | Add opedal.tech to "Blogs" section — include note: "Field notes from a Microsoft Lead CSA on AKS Automatic, security, and ALZ integration" | Fork → edit `README.md` → PR |

**PR template**:

```markdown
### Add opedal.tech to Blogs section

**Description**: Personal blog by Martin Opedal, Lead Cloud Solution Architect at Microsoft Norway. Covers Azure Landing Zones, AKS Automatic, Terraform patterns, and AI Foundry deployments from 15+ years in Nordic FSI/government/defense.

**Why this addition is valuable**: 
- Field notes from 50+ Landing Zone engagements
- Production-tested AKS + Terraform modules (all open-source)
- Speaker at Nordic Infrastructure Conference (94% approval, Level 300)

**Link**: https://opedal.tech  
**Sample posts**: 
- [ALZ Terraform field guide] (link when live)
- [AKS Automatic production readiness] (link when live)
- [AI Foundry in air-gapped environments] (link when live)
```

---

## Phase 2: Speaking and Events (Days 30–60)

### 2.1 Conference Speaker Pages (Target: 2–3 backlinks)

Martin has already spoken at NIC. These actions convert past talks into permanent backlinks.

| Conference | Action | Timeline |
|------------|--------|----------|
| **Nordic Infrastructure Conference (NIC)** | Email organizers requesting speaker page with opedal.tech link (see `seo-cheatsheet.md` #9) | Days 1–7 |
| **Microsoft internal events** | If Martin has spoken at Microsoft-hosted external events (e.g., Azure Immersion Workshops, FastTrack sessions open to customers), request speaker bios include opedal.tech | Days 30–45 |
| **Future conference CFPs** | Submit proposals to NDC Oslo, KubeCon EU (Copenhagen 2027?), or CloudNative Nordics with opedal.tech in speaker bio | Days 45–60 (for 2027 conferences) |

---

### 2.2 Podcast/Interview Outreach (Target: 2 backlinks)

Nordic/Azure podcasts often seek Microsoft employees as guests. Martin's Lead CSA + NIC speaker credentials make him an attractive guest.

| Podcast | Audience | Pitch Angle | Contact |
|---------|----------|-------------|---------|
| **Azure DevOps Podcast** (<https://azuredevopspodcast.clear-measure.com>) | Azure practitioners | "Landing Zones at scale: lessons from Nordic enterprises" — 30-min episode | Contact via website or LinkedIn (Jeffrey Palermo, host) |
| **Ship It!** by Changelog (<https://changelog.com/shipit>) | DevOps/infrastructure engineers | "AKS Automatic: when managed K8s is ready for production" — 45-min deep dive | Submit pitch: <https://changelog.com/submit> |
| **Konsulentkaffe** (Norwegian IT consultant podcast) | Norwegian consultants, architects | "Fra datacenter til Azure: 15 år med skyarkitektur" (From datacenter to Azure: 15 years of cloud architecture) | Contact via podcast website (if exists) or LinkedIn |

**Pitch template**:

```
Subject: Podcast guest pitch: [specific episode topic]

Hi [Host Name],

I'm Martin Opedal, Lead Cloud Solution Architect at Microsoft Norway. I've architected Azure Landing Zones for 50+ Nordic enterprises across banking, government, and defense. I spoke at Nordic Infrastructure Conference this year on infrastructure-as-code security (94% approval, Level 300 session).

I'd love to join [Podcast Name] to discuss [specific topic]:

[2-3 bullet points — key insights, war stories, lessons learned that would resonate with your audience]

I write about this work at opedal.tech. Happy to share architecture diagrams, code samples, or anonymized case studies during the episode.

Would this fit your editorial calendar? I'm flexible on timing and format (live/pre-recorded, 30/45/60 min).

Martin Opedal
opedal.tech | linkedin.com/in/martin-opedal
```

---

## Phase 3: Strategic Content Syndication (Days 60–90)

### 3.1 Medium Cross-Posting (Target: 3 backlinks)

Martin can cross-post his opedal.tech blog content to Medium with canonical links pointing back to opedal.tech. This doesn't create backlinks in the SEO sense (Medium uses `rel="canonical"`), but it increases brand visibility and drives referral traffic.

| Action | Why It Matters |
|--------|----------------|
| Create Medium profile: <https://medium.com/@martinopedal> | Medium posts rank well in Google for Azure/Terraform/AKS queries |
| Cross-post ALZ Terraform post with canonical link to opedal.tech | Medium's 200M+ monthly readers discover Martin's content |
| Tag posts with `#Azure`, `#Terraform`, `#Kubernetes`, `#DevOps` | Medium algorithm surfaces content to relevant subscribers |
| Include byline: "Originally published at opedal.tech" + link | Drives referral traffic back to site |

**Note**: Use Medium's "Import a story" feature (<https://medium.com/p/import>) to preserve canonical link and avoid duplicate content penalties.

---

### 3.2 Dev.to Cross-Posting (Target: 2 backlinks)

Dev.to is similar to Medium but more developer-focused. Cross-posting here reaches a different audience.

| Action | Why It Matters |
|--------|----------------|
| Create Dev.to profile: <https://dev.to/martinopedal> | Dev.to posts rank well for technical tutorials |
| Cross-post AKS Automatic and AI Foundry posts with canonical links | Dev.to's 1M+ monthly developers discover content |
| Engage with comments — Dev.to has active discussion threads | Builds Martin's reputation as helpful practitioner |

---

### 3.3 LinkedIn Articles (Target: 1–2 backlinks)

LinkedIn allows long-form articles (different from posts). These are indexed by Google and appear in LinkedIn search results.

| Action | Why It Matters |
|--------|----------------|
| Publish abridged version of ALZ Terraform post as LinkedIn article | LinkedIn's algorithm promotes articles to Martin's 1st-degree connections + followers |
| Include "Read the full version at opedal.tech" with link | Drives referral traffic + signals to LinkedIn that opedal.tech is Martin's primary platform |
| Tag Microsoft colleagues, NIC organizers, Azure MVPs in the article | Increases visibility via LinkedIn's network effects |

---

## Phase 4: GitHub Repo Visibility (Days 0–90, ongoing)

### 4.1 README Badges and Links (Target: 5+ backlinks)

Every repo Martin maintains should link back to opedal.tech. This creates a backlink network across GitHub's high-authority domain.

| Repo | Action | Example |
|------|--------|---------|
| **All existing repos** | Add "Author" section to README with link to opedal.tech | `## Author\n\nMartin Opedal — [opedal.tech](https://opedal.tech) \| [LinkedIn](https://linkedin.com/in/martin-opedal)` |
| **AVM pattern modules** | Link to opedal.tech/work in module documentation | `This module is maintained by Martin Opedal. See [opedal.tech/work](https://opedal.tech/work) for related projects.` |
| **Azure governance tooling** | Add "Learn more" section linking to relevant opedal.tech blog posts | `## Learn More\n\n- [ALZ at scale: field notes](https://opedal.tech/blog/alz-terraform) (Martin's blog)\n- [AKS Automatic production guide](https://opedal.tech/blog/aks-automatic)` |

---

### 4.2 GitHub Discussions and Issue Participation (Ongoing)

Martin should participate in Azure/Terraform/AKS discussions on popular repos, with opedal.tech in his GitHub profile bio. This doesn't create backlinks but increases brand visibility.

| Repo | Participation Strategy |
|------|------------------------|
| **Azure/terraform-azurerm-caf-enterprise-scale** | Answer questions about ALZ deployment, link to opedal.tech blog posts when relevant |
| **hashicorp/terraform-provider-azurerm** | File issues for bugs Martin encounters in customer engagements, reference opedal.tech for context |
| **Azure/AKS** | Comment on roadmap issues (e.g., AKS Automatic features), share opedal.tech blog posts as field feedback |

---

## Measurement: Tracking Backlink Success

### Tools

1. **Google Search Console** (after verification via `seo-cheatsheet.md`)
   - Check "Links" report for new referring domains
   - Target: 15+ referring domains within 90 days

2. **Ahrefs Free Backlink Checker** (<https://ahrefs.com/backlink-checker>)
   - Enter `opedal.tech`, get list of backlinks
   - Target: Domain Rating (DR) 20+ within 90 days (starting from ~0)

3. **Google Search**
   - Query: `link:opedal.tech -site:opedal.tech`
   - Note: Google's link operator is deprecated but still shows some backlinks

### Weekly Check-In (Days 7, 14, 21, 30, 60, 90)

| Metric | Target (90 days) | How to Measure |
|--------|------------------|----------------|
| Total referring domains | 15–25 | Google Search Console → Links → Top linking sites |
| High-authority backlinks (DR 50+) | 3–5 | Ahrefs (LinkedIn, GitHub, Microsoft.com, Medium) |
| Reddit/HN submissions with >10 upvotes | 2–3 | Check post karma on submitted links |
| Podcast appearances | 1–2 | Calendar/LinkedIn posts |
| Accepted guest posts | 1–2 | Published articles on Kode24, Computerworld, Nordic APIs |
| Awesome list PRs merged | 2–3 | GitHub notifications |

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| **Guest post pitches rejected** | Start with lowest-friction targets (Reddit, Awesome lists) first. Guest posts are bonus, not critical path. |
| **Reddit/HN submissions get no traction** | Post during peak traffic hours (US East Coast afternoons). Engage in comments immediately after posting. Accept that not every post will trend — aim for 1 in 3 to get >10 upvotes. |
| **Blog content from Schmitt2 is delayed** | Use existing opedal.tech/work page + GitHub repos as submission targets until blog posts are live. Pivot to "I built X" instead of "I wrote about X." |
| **Podcast/conference outreach gets no replies** | Follow up once after 14 days. If no response, move on. These are high-value but low-probability — don't block on them. |
| **PRs to Awesome lists rejected for "not notable enough"** | Strengthen PR descriptions with metrics (50+ Landing Zone engagements, NIC speaker, Microsoft Lead CSA, X GitHub stars). If rejected, accept gracefully and move to next list. |

---

## 90-Day Calendar (Summary)

| Days | Focus | Actions | Expected Backlinks |
|------|-------|---------|---------------------|
| **1–7** | Quick wins | LinkedIn updates, GitHub profile README, NIC speaker bio email, Awesome list PRs | 3–5 |
| **8–30** | Publication pitches + Reddit submissions | Email Kode24/Computerworld/Nordic APIs, submit ALZ post to HN/r/AZURE, cross-post to Medium/Dev.to | 5–8 |
| **31–60** | Podcast outreach + conference CFPs | Pitch Azure DevOps Podcast, Ship It!, submit NDC Oslo CFP for 2027, engage in GitHub discussions | 3–5 |
| **61–90** | Content syndication + follow-ups | Cross-post remaining blog posts, follow up on guest post pitches, track GSC backlink growth | 4–7 |
| **Total** | | | **15–25 backlinks** |

---

## Success Looks Like (Day 90)

- Google search `"Martin Opedal"` → opedal.tech appears in top 5 results (currently beyond page 30)
- Google search `"Martin Opedal Azure"` → opedal.tech appears in top 3 results
- Google Search Console shows 15–25 referring domains (up from ~0)
- At least 1 guest post published on Nordic tech publication
- At least 1 blog post on opedal.tech has >50 Reddit/HN upvotes
- At least 2 PRs to Awesome lists merged
- Martin's GitHub profile README has 100+ views (tracked via GitHub Insights)
- opedal.tech receives 500+ monthly organic visitors (tracked via GSC Performance report)

---

## Long-Term Flywheel (Beyond 90 Days)

Once the initial backlink foundation is built, the flywheel sustains itself:

1. **Blog posts rank in Google** → drive organic traffic
2. **Organic traffic grows** → more developers discover Martin's work
3. **More discovery** → more conference invitations, podcast requests, guest post invitations
4. **More speaking/writing** → more backlinks
5. **More backlinks** → higher domain authority → blog posts rank higher
6. **Loop continues**

**Key insight**: The first 15 backlinks are the hardest. After that, the site's authority grows exponentially. Focus on Phase 1 (quick wins) to build momentum.
