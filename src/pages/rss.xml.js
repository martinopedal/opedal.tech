import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sorted = posts.sort(
    (a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime()
  );

  // Generate items with content:encoded using simple markdown-to-HTML conversion
  const items = sorted.map((post) => {
    // Basic markdown to HTML conversion for common patterns
    let htmlContent = post.body
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em>$1</em>')
      .replace(/```([^`]+)```/gims, '<pre><code>$1</code></pre>')
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2">$1</a>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>');
    
    htmlContent = '<p>' + htmlContent + '</p>';
    
    return {
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.slug}/`,
      author: 'hello@opedal.tech (Martin Opedal)',
      customData: `<content:encoded><![CDATA[${htmlContent}]]></content:encoded>`,
    };
  });

  return rss({
    title: 'opedal.tech',
    description:
      'Field notes on Azure Landing Zones, AKS Automatic with Terraform, IaC security patterns, GitHub Copilot CLI, and AI-assisted platform engineering.',
    site: context.site,
    items,
    customData: '<language>en</language>',
    xmlns: {
      content: 'http://purl.org/rss/1.0/modules/content/',
    },
  });
}
