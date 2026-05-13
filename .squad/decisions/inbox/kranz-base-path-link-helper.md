# Decision: Base path link helper pattern

**By:** Kranz (Site Redesign Specialist)  
**Date:** 2026-05-13  
**Status:** Adopted — apply this pattern to all future internal links

## Problem

Astro's `base` path is env-driven via `GITHUB_PAGES_BASE_PATH` (set by `actions/configure-pages`):
- github.io preview: base = `/opedal.tech/`
- apex domain (post-cutover): base = `/`

Absolute internal links (`href="/cv"`, `href="/work"`, `href="/blog"`) bypass the base path. When deployed to the github.io preview, these render as `https://martinopedal.github.io/cv` (404) instead of `https://martinopedal.github.io/opedal.tech/cv` (200). Once DNS cuts over and base flips back to `/`, the absolute hrefs would work again — but the site MUST render correctly in BOTH environments.

## Solution

Created `src/utils/link.ts` with a helper function:
```ts
export function link(path: string): string {
  if (path.startsWith('#')) return path; // Anchor-only, no base
  const base = import.meta.env.BASE_URL; // Trailing-slashed by Astro
  const clean = path.replace(/^\//, '');
  return `${base}${clean}`;
}
```

### Usage
```astro
---
import { link } from '../utils/link';
---
<a href={link('cv')}>CV</a>             <!-- /cv or /opedal.tech/cv -->
<a href={link('work#aks')}>AKS</a>      <!-- /work#aks or /opedal.tech/work#aks -->
<a href={link('#contact')}>Contact</a>  <!-- #contact (anchor-only, no base) -->
```

**CRITICAL:** Pass paths WITHOUT leading slashes: `link('cv')`, NOT `link('/cv')`. The helper strips them if present, but prefer the no-slash convention for consistency.

## Verification approach

Build with both env modes and grep the output:
```powershell
# With base path
$env:GITHUB_PAGES_BASE_PATH = '/opedal.tech/'; npm run build
Get-Content dist\index.html | Select-String -Pattern 'href="/opedal\.tech/(cv|work|blog)'
# Should show: /opedal.tech/cv, /opedal.tech/work, /opedal.tech/blog

# Without base path (default)
Remove-Item Env:\GITHUB_PAGES_BASE_PATH; npm run build
Get-Content dist\index.html | Select-String -Pattern 'href="/(cv|work|blog)'
# Should show: /cv, /work, /blog
```

## Already applied to

- `src/components/Nav.astro`
- `src/components/Hero.astro`
- `src/components/Work.astro` (homepage component)
- `src/pages/blog/index.astro`
- `src/layouts/BlogLayout.astro`
- `src/pages/cv.astro`

## Lovell action required

`src/pages/work.astro` has two broken absolute internal links that were out of Kranz's scope:
- Line ~56: `<a href="/blog/azure-landing-zones-2025/">Azure Landing Zones 2025</a>`
- Line ~136: `<a href="/blog/building-with-github-copilot/">Building with GitHub Copilot</a>`

Apply the same helper pattern:
```astro
---
import { link } from '../utils/link';
// ...existing imports
---
<!-- Update both links: -->
<a href={link('blog/azure-landing-zones-2025/')}>Azure Landing Zones 2025</a>
<a href={link('blog/building-with-github-copilot/')}>Building with GitHub Copilot</a>
```

## Future guidance

All future internal page links MUST use this helper. External links (`https://...`) and `mailto:` links are unaffected. Anchor-only links (`#section-id`) work with or without the helper, but passing them through is harmless and keeps the pattern consistent.

If a new route is added (e.g., `/speaking`), update that page's components to use `link('speaking')` everywhere.

## CSP compatibility

This pattern is CSP-safe: no inline style or script required. The helper is pure TS imported at build time; Astro evaluates it during static generation.
