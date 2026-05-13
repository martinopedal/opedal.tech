import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sorted = posts.sort(
    (a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime()
  );

  return rss({
    title: 'opedal.tech',
    description:
      'Field notes on Azure Landing Zones, AKS Automatic with Terraform, IaC security patterns, GitHub Copilot CLI, and AI-assisted platform engineering.',
    site: context.site,
    items: sorted.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.slug}/`,
      author: 'hello@opedal.tech (Martin Opedal)',
    })),
    customData: '<language>en</language>',
  });
}
