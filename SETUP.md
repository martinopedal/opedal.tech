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

---

## 3. Configure Domeneshop DNS → GitHub Pages

GitHub Pages IPs for custom domains (A records):

```
A    opedal.tech    185.199.108.153
A    opedal.tech    185.199.109.153
A    opedal.tech    185.199.110.153
A    opedal.tech    185.199.111.153
```

AAAA records for IPv6:

```
AAAA opedal.tech    2606:50c0:8000::153
AAAA opedal.tech    2606:50c0:8001::153
AAAA opedal.tech    2606:50c0:8002::153
AAAA opedal.tech    2606:50c0:8003::153
```

For `www` redirect (optional — redirects www.opedal.tech to opedal.tech):

```
CNAME www.opedal.tech    martinopedal.github.io
```

**Domeneshop steps:**

1. Log in to [domeneshop.no](https://domeneshop.no)
2. Go to **DNS** for `opedal.tech`
3. Delete any existing A/AAAA records for the apex domain
4. Add the 4 A records and 4 AAAA records above
5. Optionally add the CNAME for `www`
6. TTL: use 3600 (1 hour) initially; lower to 300 during cutover if needed

**Propagation:** DNS changes typically propagate within 1–24 hours.
GitHub Pages will issue a free Let's Encrypt TLS certificate automatically once DNS resolves.

Verify with:
```bash
dig opedal.tech +short
# Should return the 4 GitHub Pages IPs above
curl -I https://opedal.tech
# Should return HTTP 200
```

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

## 6. Squad Labels

Create these labels in **Issues → Labels → New label** (or the auto-label workflow
will create `squad` automatically on the first issue):

| Label | Color | Description |
|-------|-------|-------------|
| `squad` | `#0075ca` | Squad-tracked issue |
| `copilot` | `#8957e5` | Assigned to GitHub Copilot coding agent |
| `enhancement` | `#a2eeef` | New feature or section |
| `content` | `#fef3c7` | Text/copy update |
| `bug` | `#d73a4a` | Something broken |
| `chore` | `#e4e669` | Maintenance, CI, deps |
| `documentation` | `#0075ca` | Docs update |
| `dependencies` | `#0366d6` | Dependency update (Dependabot) |

---

## 7. Copilot Code Review (optional but recommended)

**Settings → Copilot → Code review → Enable automatic code review**

This makes `copilot-pull-request-reviewer` available as a reviewer target —
required for the `copilot-agent-pr-review.yml` workflow to request reviews.

---

## Done ✅

Once all steps above are complete:
- `https://opedal.tech` is live over HTTPS
- All PRs require CI green before merge
- Squad labels and Copilot agent are wired up
- Dependabot keeps Actions up to date
