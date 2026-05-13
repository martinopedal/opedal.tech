// Redirect /sitemap.xml to /sitemap-index.xml for bots that only check the standard location
export async function GET() {
  return new Response(null, {
    status: 301,
    headers: {
      Location: '/sitemap-index.xml',
    },
  });
}
