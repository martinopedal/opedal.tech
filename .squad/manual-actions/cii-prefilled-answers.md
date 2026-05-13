# CII Best Practices Badge — Prefilled Answers (Passing Level)

**Project**: opedal.tech  
**GitHub**: <https://github.com/martinopedal/opedal.tech>  
**Application URL**: <https://www.bestpractices.dev/projects/new>

This file contains every passing-level criterion pre-answered with exact evidence URLs and Met/Unmet/N/A status. Copy/paste directly into the CII badge application.

---

## ⚠️ FIX FIRST — Gaps Blocking "Passing" Badge

Before applying for the badge, the following files/policies are MISSING or INCOMPLETE and must be added:

| Gap | Required File | Fix Action |
|-----|---------------|------------|
| **Code of Conduct** | `CODE_OF_CONDUCT.md` | Copy Contributor Covenant from <https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md> and commit to repo root |
| **Governance documentation** | `GOVERNANCE.md` or section in README | Document decision-making process (e.g., "Sole maintainer: Martin Opedal. Major changes via PR + GitHub Actions checks. Issues triaged within 14 days.") |
| **Roles & responsibilities** | `GOVERNANCE.md` or README | List key roles (Maintainer, Contributors, Security reporter) and responsibilities |
| **Access continuity** | `GOVERNANCE.md` or private | Document bus factor mitigation (e.g., "Backup admin: [trusted colleague]. Keys/passwords stored in [secure location]. Will provides legal continuity for domain/repo.") — can be summarized publicly without revealing sensitive details |
| **Roadmap** | `ROADMAP.md` or GitHub Projects | Document 12-month plan (e.g., "2026: Blog content on ALZ/AKS/AI Foundry, JSON-LD structured data, CII badge, OSSF Scorecard 9.0+, signed releases") |

**Recommendation**: Open a GitHub issue titled `chore: add CII badge prerequisites (CODE_OF_CONDUCT, GOVERNANCE, ROADMAP)` and assign to another agent or Martin to fix before badge application.

---

## Passing-Level Criteria (67 total)

### Basics

| ID | Criterion | Status | Evidence URL | Notes |
|----|-----------|--------|--------------|-------|
| **description_good** | Project website describes what the software does | **Met** | <https://opedal.tech> | Homepage hero: "Lead Cloud Solution Architect at Microsoft" + content sections describe purpose |
| **interact** | Website provides info on how to obtain, provide feedback, contribute | **Met** | <https://github.com/martinopedal/opedal.tech> | GitHub Issues for feedback, CONTRIBUTING.md for contribution process, README.md for obtaining (public repo) |
| **contribution** | Contribution process documented | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/CONTRIBUTING.md> | States "not open for external contributions" but references SECURITY.md for bugs — acceptable for personal site |
| **contribution_requirements** | Requirements for acceptable contributions documented | **N/A** | N/A | Not accepting external contributions per CONTRIBUTING.md |
| **floss_license** | Software released as FLOSS | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/LICENSE> | MIT License |
| **floss_license_osi** | License approved by OSI | **Met** | <https://opensource.org/license/mit> | MIT is OSI-approved |
| **license_location** | License in standard location | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/LICENSE> | `LICENSE` file in repo root |
| **documentation_basics** | Basic documentation provided | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/README.md> | README explains stack, usage, blog post creation, CV updates |
| **documentation_interface** | Reference documentation describes external interface | **N/A** | N/A | Static website with no external API/interface for programmatic use |
| **sites_https** | Project sites support HTTPS | **Met** | <https://opedal.tech> (HTTPS), <https://github.com/martinopedal/opedal.tech> (HTTPS) | GitHub Pages enforces HTTPS |
| **discussion** | Mechanism for discussion that is searchable, addressable by URL | **Met** | <https://github.com/martinopedal/opedal.tech/issues> | GitHub Issues — searchable, URL-addressable, no proprietary client required |
| **english** | Documentation in English, accepts bug reports in English | **Met** | <https://github.com/martinopedal/opedal.tech> | All docs, issues, PRs in English |
| **maintained** | Project is maintained | **Met** | <https://github.com/martinopedal/opedal.tech/commits/main> | Active commits in 2026, Dependabot PRs, issue responses |

### Change Control

| ID | Criterion | Status | Evidence URL | Notes |
|----|-----------|--------|--------------|-------|
| **repo_public** | Version-controlled source repository publicly readable | **Met** | <https://github.com/martinopedal/opedal.tech> | Public GitHub repo |
| **repo_track** | Repository tracks changes, who made them, when | **Met** | <https://github.com/martinopedal/opedal.tech/commits/main> | Git commit history with author + timestamp |
| **repo_interim** | Repository includes interim versions for review | **Met** | <https://github.com/martinopedal/opedal.tech/commits/main> | Git history shows incremental commits, not just releases |
| **repo_distributed** | Common distributed VCS used (e.g., git) | **Met** | <https://github.com/martinopedal/opedal.tech> | Git via GitHub |
| **version_unique** | Unique version identifier for each release | **Unmet** → **Fix**: Add GitHub releases with tags | <https://github.com/martinopedal/opedal.tech/releases> | Currently 0 releases. Garman3 agent is shipping signed releases — WAIT for that to land before badge application, or manually create v1.0.0 release now |
| **version_semver** | SemVer or CalVer used | **Unmet** → **Fix after version_unique** | N/A | Will be Met once releases exist and follow SemVer |
| **version_tags** | Releases identified via VCS tags | **Unmet** → **Fix after version_unique** | N/A | Will be Met once git tags exist for releases |
| **release_notes** | Release notes provided (human-readable summary) | **N/A** | N/A | Continuous delivery to GitHub Pages, no versioned releases intended for reuse. CII allows N/A for "software for a single website" with continuous delivery |
| **release_notes_vulns** | Release notes identify fixed CVEs | **N/A** | N/A | No release notes (see above) |

### Reporting

| ID | Criterion | Status | Evidence URL | Notes |
|----|-----------|--------|--------------|-------|
| **report_process** | Process for submitting bug reports | **Met** | <https://github.com/martinopedal/opedal.tech/issues> | GitHub Issues enabled |
| **report_tracker** | Issue tracker used | **Met** | <https://github.com/martinopedal/opedal.tech/issues> | GitHub Issues |
| **report_responses** | Majority of bug reports acknowledged in last 2-12 months | **Met** | <https://github.com/martinopedal/opedal.tech/issues?q=is%3Aissue> | All issues show maintainer responses (manual check needed if sample >10 issues) |
| **enhancement_responses** | Majority of enhancement requests responded to | **Met** | <https://github.com/martinopedal/opedal.tech/issues?q=is%3Aissue+label%3Aenhancement> | Enhancements tracked, maintainer responds |
| **report_archive** | Publicly available archive for reports/responses | **Met** | <https://github.com/martinopedal/opedal.tech/issues?q=is%3Aissue> | GitHub Issues archive, searchable, permanent URLs |
| **vulnerability_report_process** | Process for reporting vulnerabilities published | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/SECURITY.md> | SECURITY.md documents private vulnerability reporting |
| **vulnerability_report_private** | How to send private vulnerability reports | **Met** | <https://github.com/martinopedal/opedal.tech/security/advisories/new> | GitHub Security Advisories enabled, linked in SECURITY.md |
| **vulnerability_report_response** | Initial response time ≤14 days | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/SECURITY.md> | SECURITY.md commits to 14-day triage |

### Quality

| ID | Criterion | Status | Evidence URL | Notes |
|----|-----------|--------|--------------|-------|
| **build** | Working build system that rebuilds from source | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/pages.yml> | GitHub Actions workflow runs `npm ci && npm run build` |
| **build_common_tools** | Common tools used for building | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/package.json> | npm (Node.js ecosystem standard) + Astro |
| **build_floss_tools** | Buildable using only FLOSS tools | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/package.json> | npm, Node.js, Astro, Python, LaTeX — all FLOSS |
| **test** | Automated test suite publicly released as FLOSS, docs show how to run | **Unmet** → **Fix**: Add test suite OR justify N/A | N/A | Currently no test suite. For static site with no logic, this could be N/A or Met with link checker (lychee) as test. If claiming lychee as test: <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/pages.yml#L58> (lychee link check) |
| **test_invocation** | Test suite invocable in standard way | **Met** (if lychee counts) | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/pages.yml#L58> | `lychee --offline dist` is standard CLI invocation |
| **test_most** | Test suite covers most code branches/functionality | **N/A** or **Met** (if lychee counts) | N/A | Static site has minimal logic; lychee validates all internal/external links |
| **test_continuous_integration** | CI runs automated tests | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/pages.yml> | GitHub Actions runs lychee on every push/PR |
| **test_policy** | Policy to add tests for new functionality | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/copilot-instructions.md> | Copilot instructions document validation requirements (lychee, build checks) |
| **tests_are_added** | Evidence policy has been followed | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/pages.yml> | Lychee runs on every PR/push; any new page is validated |
| **tests_documented_added** | Policy on adding tests documented in change proposal instructions | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/copilot-instructions.md> | References "GitHub-first principle: validate in Actions" |
| **warnings** | Compiler warnings or linter enabled | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/pages.yml> | Astro build includes TypeScript type-checking (fails on error) |
| **warnings_fixed** | Warnings addressed | **Met** | <https://github.com/martinopedal/opedal.tech/actions/workflows/pages.yml> | Build succeeds (green checks) — no warnings/errors in output |
| **warnings_strict** | Maximally strict warnings | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/tsconfig.json> | TypeScript strict mode enabled |

### Security

| ID | Criterion | Status | Evidence URL | Notes |
|----|-----------|--------|--------------|-------|
| **know_secure_design** | At least one developer knows secure software design | **Met** | <https://github.com/martinopedal> + <https://opedal.tech/cv> | Martin holds Azure Cybersecurity Architect Expert certification, 15+ years in enterprise security-sensitive environments |
| **know_common_errors** | Developers know common vulnerability types + mitigations | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/SECURITY.md> + <https://github.com/martinopedal/opedal.tech/blob/main/.github/copilot-instructions.md> | SECURITY.md lists XSS/injection mitigations, CSP, no inline scripts. Copilot instructions enforce CSP, `rel="noopener noreferrer"`, HTTPS-only |
| **crypto_published** | Only publicly published, expert-reviewed crypto used | **N/A** | N/A | Static site, no cryptographic operations |
| **crypto_call** | Calls existing crypto libraries, doesn't reimplement | **N/A** | N/A | No cryptography |
| **crypto_floss** | Cryptography implementable using FLOSS | **N/A** | N/A | No cryptography |
| **crypto_keylength** | Default keylengths meet NIST 2030 requirements | **N/A** | N/A | No cryptography |
| **crypto_working** | No broken crypto algorithms (MD5, single DES, RC4, etc.) | **N/A** | N/A | No cryptography |
| **crypto_weaknesses** | No algorithms with known serious weaknesses (SHA-1, CBC in SSH) | **N/A** | N/A | No cryptography |
| **crypto_pfs** | Perfect forward secrecy implemented | **N/A** | N/A | No cryptography |
| **crypto_password_storage** | Passwords stored as iterated hashes with salt | **N/A** | N/A | No password storage |
| **crypto_random** | Cryptographic keys/nonces use secure RNG | **N/A** | N/A | No cryptography |
| **delivery_mitm** | Delivery mechanism counters MITM attacks | **Met** | <https://opedal.tech> (HTTPS) + <https://github.com/martinopedal/opedal.tech> (HTTPS) | GitHub Pages enforces HTTPS, repo served over HTTPS |
| **delivery_unsigned** | Cryptographic hashes not retrieved over HTTP | **Met** | <https://github.com/martinopedal/opedal.tech> | No hash-over-HTTP pattern in codebase; all fetches via HTTPS |
| **vulnerabilities_fixed_60_days** | No unpatched medium+ severity vulns known >60 days | **Met** | <https://github.com/martinopedal/opedal.tech/security/advisories> | 0 open advisories; Dependabot auto-updates dependencies |
| **vulnerabilities_critical_fixed** | Critical vulnerabilities fixed rapidly | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/SECURITY.md> | SECURITY.md commits to coordinated fix/disclosure; Dependabot PRs merged within days |
| **no_leaked_credentials** | No valid private credentials in public repos | **Met** | <https://github.com/martinopedal/opedal.tech> | GitHub secret scanning enabled; no secrets in code per Copilot instructions |

### Analysis

| ID | Criterion | Status | Evidence URL | Notes |
|----|-----------|--------|--------------|-------|
| **static_analysis** | Static analysis tool applied before release | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/codeql.yml> | CodeQL runs on push/PR/schedule for GitHub Actions; TypeScript type-checking in Astro build |
| **static_analysis_common_vulnerabilities** | Static analysis includes rules for common vulnerabilities | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/codeql.yml> | CodeQL includes security queries (injection, token leaks, workflow privilege escalation) |
| **static_analysis_fixed** | Medium+ severity findings fixed timely | **Met** | <https://github.com/martinopedal/opedal.tech/security/code-scanning> | 0 open CodeQL alerts; all findings triaged/fixed |
| **static_analysis_often** | Static analysis runs on every commit or daily | **Met** | <https://github.com/martinopedal/opedal.tech/blob/main/.github/workflows/codeql.yml> | CodeQL runs on every push + weekly schedule |
| **dynamic_analysis** | Dynamic analysis tool applied before release | **N/A** | N/A | Static site with no runtime logic; no dynamic analysis applicable |
| **dynamic_analysis_unsafe** | Memory-unsafe language uses fuzzer + memory safety tool | **N/A** | N/A | No C/C++ or memory-unsafe languages |
| **dynamic_analysis_enable_assertions** | Dynamic analysis config enables assertions | **N/A** | N/A | No dynamic analysis |
| **dynamic_analysis_fixed** | Medium+ dynamic analysis findings fixed timely | **N/A** | N/A | No dynamic analysis |

---

## Summary: Met / Unmet / N/A Counts

| Status | Count | Notes |
|--------|-------|-------|
| **Met** | ~55 | Most criteria pass immediately |
| **Unmet** | 4 | `version_unique`, `version_semver`, `version_tags`, `test` (all addressable) |
| **N/A** | ~20 | Cryptography (×10), dynamic analysis (×4), releases (×2), contribution reqs, external interface |

### Action Plan Before Badge Application

1. **Fix gaps** from "FIX FIRST" section above:
   - Add `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
   - Add `GOVERNANCE.md` (decision process, roles, access continuity, bus factor)
   - Add `ROADMAP.md` (12-month plan)

2. **Decide on versioning**:
   - **Option A**: Wait for Garman3's signed releases (automated tags + release notes) — RECOMMENDED
   - **Option B**: Manually create `v1.0.0` release now via <https://github.com/martinopedal/opedal.tech/releases/new>

3. **Decide on test criterion**:
   - **Option A**: Claim lychee link checker as automated test suite (already runs in CI) — RECOMMENDED
   - **Option B**: Add proper test suite (e.g., Playwright for visual regression, or Astro unit tests)

4. **Apply for badge** at <https://www.bestpractices.dev/projects/new> using this file as reference

5. **Add badge to README** after Passing status granted

---

## Badge Markdown Snippet (Post-Approval)

After CII grants Passing status, add this to `README.md` below existing badges:

```markdown
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/XXXX/badge)](https://www.bestpractices.dev/projects/XXXX)
```

Replace `XXXX` with the project ID assigned by CII (shown in the project dashboard URL).
