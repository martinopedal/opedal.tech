# Setup Checklist — opedal.tech

This file documents the manual GitHub settings steps that cannot be automated via committed files.
Complete these after merging the initial PR to `main`.

---

## 1. Enable GitHub Pages

**Settings → Pages**

- Source: **GitHub Actions** (not "Deploy from a branch")
- Custom domain: `opedal.tech` (pre-filled from the `CNAME` file)
- ✅ Enforce HTTPS

The `pages.yml` workflow deploys on every push to `main`.
Verify by navigating to the Actions tab and checking **Deploy to GitHub Pages**.

---

## 2. Configure Branch Protection on `main`

**Settings → Branches → Add rule → Branch name pattern: `main`**

```
✅ Require a pull request before merging
   Required approving reviews: 0  (solo-maintained)
✅ Require status checks to pass before merging
   Required checks:
     - Analyze (actions)          ← CodeQL workflow
     - Build Astro site           ← pages.yml build job
✅ Require branches to be up to date before merging
✅ Require linear history (no merge commits)
✅ Include administrators (enforce_admins)
❌ Require signed commits        (breaks Dependabot + API commits)
❌ Allow force pushes
❌ Allow deletions
```

> **Note (drift):** as of the last audit the live protection on `main` only requires **1 approving review** with `enforce_admins=false`, no required status checks, and no linear-history requirement. To bring the live settings in line with the table above, run:
>
> ```bash
> gh api -X PUT repos/martinopedal/opedal.tech/branches/main/protection \
>   -F required_status_checks.strict=true \
>   -F 'required_status_checks.contexts[]=Analyze (actions)' \
>   -F 'required_status_checks.contexts[]=Build Astro site' \
>   -F enforce_admins=true \
>   -F required_pull_request_reviews.required_approving_review_count=0 \
>   -F required_linear_history=true \
>   -F restrictions= \
>   -F allow_force_pushes=false \
>   -F allow_deletions=false
> ```
>
> Side effect: with `enforce_admins=true`, future admin-merges (like `gh pr merge --admin`) will need every required check to be green first. The `Build Astro site` check runs on PRs only after the workflow change in commit history is in place.

---

## 3. Configure Domeneshop DNS → GitHub Pages

> **Current state at the time of writing:** `opedal.tech` and `www.opedal.tech` resolve to Domeneshop's parking IPs (`185.134.245.113` / `2a01:5b40:0:bc03::1`). Until the records below are in place, the site is not yet served by GitHub Pages.

> **Order of operations (important):**
> 1. Enable GitHub Pages first (Step 1 above) and confirm the workflow deploys to `https://martinopedal.github.io/opedal.tech/` *or* that the Pages tab shows `opedal.tech` queued for DNS check.
> 2. Then update DNS in Domeneshop.
> 3. After DNS propagates, GitHub auto-issues a Let's Encrypt TLS cert (usually 10 minutes – a few hours).
> 4. Finally, tick **Enforce HTTPS** in Settings → Pages.

### 3a. Records to set

GitHub Pages IPs for custom **apex** domains (A records — IPv4):

```
A    @    185.199.108.153
A    @    185.199.109.153
A    @    185.199.110.153
A    @    185.199.111.153
```

AAAA records for IPv6 (recommended — GitHub serves both stacks):

```
AAAA @    2606:50c0:8000::153
AAAA @    2606:50c0:8001::153
AAAA @    2606:50c0:8002::153
AAAA @    2606:50c0:8003::153
```

`www` subdomain (recommended — Pages will redirect `www.opedal.tech` → `opedal.tech` because the `CNAME` file in the repo holds the apex):

```
CNAME www    martinopedal.github.io.
```

> The trailing dot on `martinopedal.github.io.` makes it an absolute name. Domeneshop accepts the value with or without it; both resolve identically. **Do not** use `martinopedal.github.io/opedal.tech` — Pages requires the bare host.

### 3b. Domeneshop UI walkthrough

1. Log in to [domeneshop.no](https://domeneshop.no).
2. Click your domain → **DNS** tab for `opedal.tech`.
3. **Delete** the existing apex A record (`185.134.245.113`) and apex AAAA record (`2a01:5b40:0:bc03::1`) — these point at Domeneshop's parking page.
4. Also delete any existing `www` A/AAAA records that point at the same parking IPs.
5. Click **Legg til DNS-oppføring** (Add record) and add each row from 3a:
   - **Type** = `A` / `AAAA` / `CNAME`
   - **Vert** (Host) = `@` for the apex, `www` for the subdomain
   - **Data / Verdi** (Value) = the IP or hostname from 3a
   - **TTL** = `3600` (1 hour) for steady state. Drop to `300` during cutover if you want faster rollback.
6. Leave any unrelated records (MX for mail, TXT for SPF/DMARC, etc.) untouched.

> **DNSSEC**: If Domeneshop has DNSSEC enabled on the zone, leave it on — it is fully compatible with GitHub Pages.

### 3c. Optional — CAA records

If you have or plan to add CAA records, you must whitelist the CAs GitHub Pages uses or certificate issuance will fail. The minimum safe set today:

```
CAA  @  0 issue "letsencrypt.org"
CAA  @  0 issue "pki.goog"
```

If no CAA records exist on the zone, all CAs are allowed by default and you can skip this step.

### 3d. Verify (Windows / PowerShell)

```powershell
# Should return the 4 GitHub Pages anycast IPs above
Resolve-DnsName opedal.tech -Type A    | Select-Object Name, IPAddress
Resolve-DnsName opedal.tech -Type AAAA | Select-Object Name, IPAddress

# www should be an alias to martinopedal.github.io
Resolve-DnsName www.opedal.tech | Select-Object Name, Type, NameHost, IPAddress

# Once GitHub has issued the cert, this should return HTTP 200
Invoke-WebRequest -Uri https://opedal.tech -Method Head -UseBasicParsing |
  Select-Object StatusCode, Headers
```

Cross-platform equivalent:

```bash
dig opedal.tech +short
dig AAAA opedal.tech +short
dig www.opedal.tech +short
curl -I https://opedal.tech
```

GitHub's own DNS check is in **Settings → Pages → Custom domain** — it will show ✅ once the records propagate.

---

## 4. Enable CodeQL / Security Features

**Settings → Security → Code security and analysis**

- ✅ Dependency graph — Enable
- ✅ Dependabot alerts — Enable
- ✅ Dependabot security updates — Enable
- ✅ CodeQL analysis — CodeQL is configured via `.github/workflows/codeql.yml`
  (it runs automatically; no extra settings toggle needed)
- ✅ Secret scanning — Enable
- ✅ Push protection — Enable

---

## 5. Enable Private Vulnerability Reporting

**Settings → Security → Private vulnerability reporting → Enable**

This allows the security contact link in `SECURITY.md` to work.

---

## 6. Issue Labels (optional)

Create these labels in **Issues → Labels → New label** as needed. GitHub creates a
default set on repo creation; the only addition worth making is `copilot`:

| Label | Color | Description |
|-------|-------|-------------|
| `copilot` | `#8957e5` | Assigned to the GitHub Copilot coding agent |
| `enhancement` | `#a2eeef` | New feature or section |
| `content` | `#fef3c7` | Text/copy update |
| `bug` | `#d73a4a` | Something broken |
| `chore` | `#e4e669` | Maintenance, CI, deps |
| `documentation` | `#0075ca` | Docs update |
| `dependencies` | `#0366d6` | Dependency update (Dependabot) |

---

## 7. Copilot Code Review (optional)

**Settings → Copilot → Code review → Enable automatic code review**

Makes `copilot-pull-request-reviewer` available as a reviewer target if you want
Copilot reviews requested automatically on every PR.

---

## Done ✅

Once all steps above are complete:
- `https://opedal.tech` is live over HTTPS
- All PRs require CI green before merge
- Dependabot keeps GitHub Actions and npm packages up to date
- Secret scanning, push protection, and private vulnerability reporting are on
