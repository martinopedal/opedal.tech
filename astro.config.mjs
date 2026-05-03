import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://opedal.tech',
  integrations: [sitemap()],
  output: 'static',
});
