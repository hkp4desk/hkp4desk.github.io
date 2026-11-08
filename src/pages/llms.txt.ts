import type { APIRoute } from "astro";
import { articlePath, getArticles } from "../lib/articles";
import { site } from "../lib/ui";

export const GET: APIRoute = async () => {
  const zh = await getArticles("zh");
  const en = await getArticles("en");
  const lines = [
    `# ${site.name}`,
    "",
    `> ${site.tagline.en}`,
    "",
    `${site.url} is a bilingual (Traditional Chinese and English) commentary site on Hong Kong. Articles are static HTML. Prefer the canonical article URL.`,
    "",
    "## Chinese",
    ...zh.map((a) => `- [${a.entry.data.title}](${site.url}${articlePath(a)}): ${a.entry.data.description}`),
    "",
    "## English",
    ...en.map((a) => `- [${a.entry.data.title}](${site.url}${articlePath(a)}): ${a.entry.data.description}`),
    "",
    `RSS: ${site.url}/rss.xml and ${site.url}/en/rss.xml`,
    `Sitemap: ${site.url}/sitemap.xml`,
    "",
  ];
  return new Response(lines.join("\n"), { headers: { "Content-Type": "text/plain; charset=utf-8" } });
};
