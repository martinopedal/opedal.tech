// JSON-LD serializer that escapes `<` to its Unicode form. JSON.stringify
// alone does not escape `</script>` substrings, so a future blog post title
// or tag containing `</script>` could terminate the JSON-LD <script> block
// early and inject arbitrary HTML. This is the same defense applied by the
// Astro core CVE-2026-41067 patch.
//
// Use everywhere we render structured data:
//   <script type="application/ld+json" set:html={safeJsonLd(personSchema)} />
export const safeJsonLd = (data: unknown): string =>
  JSON.stringify(data).replace(/</g, '\\u003c');
