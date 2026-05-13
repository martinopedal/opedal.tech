/**
 * link() — Base-path-aware internal link helper
 * 
 * Astro's BASE_URL is env-driven:
 *   - localhost:                                '/'
 *   - github.io project pages:                  '/opedal.tech/'
 *   - opedal.tech custom domain (post-cutover): '/'
 * 
 * Usage:
 *   <a href={link('cv')}>CV</a>           → /cv or /opedal.tech/cv
 *   <a href={link('work#aks')}>AKS</a>    → /work#aks or /opedal.tech/work#aks
 *   <a href={link('#contact')}>Contact</a> → #contact (anchor-only, no base)
 * 
 * Do NOT pass leading slashes: link('cv'), not link('/cv').
 */
export function link(path: string): string {
  // Anchor-only paths pass through unchanged
  if (path.startsWith('#')) {
    return path;
  }

  const base = import.meta.env.BASE_URL; // Astro provides this, trailing-slashed
  const clean = path.replace(/^\//, ''); // Strip leading slash if user added one
  return `${base}${clean}`;
}
