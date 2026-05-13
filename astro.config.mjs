import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// `base` is env-driven so the same config works for:
//   - localhost:                                base = '/'
//   - github.io project pages preview:          base = '/opedal.tech'
//   - opedal.tech custom domain (post-cutover): base = '/'
// The Pages workflow sets GITHUB_PAGES_BASE_PATH from `actions/configure-pages`
// output, which auto-detects whether a CNAME is present.
const base = process.env.GITHUB_PAGES_BASE_PATH || '/';

export default defineConfig({
  site: 'https://opedal.tech',
  base,
  integrations: [sitemap()],
  output: 'static',
});
