/**
 * link() — Base-path-aware internal link helper
 * 
 * Astro's BASE_URL is env-driven (NOTE: NOT guaranteed trailing-slashed):
 *   - localhost (no env):                       '/'
 *   - github.io project pages (via env):        '/opedal.tech' (no trailing slash)
 *   - opedal.tech custom domain (post-cutover): '/'
 * 
 * This helper normalizes to guarantee exactly one slash between base and path.
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

  const base = import.meta.env.BASE_URL.replace(/\/$/, ''); // Strip trailing slash if any
  const clean = path.replace(/^\//, ''); // Strip leading slash if any
  // For the home path (empty after cleaning), return base + '/' so we get '/' or '/opedal.tech/'
  if (clean === '') {
    return base + '/';
  }
  return `${base}/${clean}`;
}
