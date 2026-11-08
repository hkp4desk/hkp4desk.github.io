import type { APIRoute } from "astro";
import { articlePath, getArticles } from "../lib/articles";
import { site } from "../lib/ui";

const STATIC = [
  "/",
  "/en/",
  "/articles/",
  "/en/articles/",
  "/about/",
  "/en/about/",
  "/donate/",
  "/en/donate/",
  "/p/prosperity/",
  "/p/projection/",
  "/p/prospect/",
  "/p/potential/",
  "/en/p/prosperity/",
  "/en/p/projection/",
  "/en/p/prospect/",
  "/en/p/potential/",
];

function loc(path: string, lastmod?: Date) {
  const mod = lastmod ? `<lastmod>${lastmod.toISOString().slice(0, 10)}</lastmod>` : "";
  return `<url><loc>${site.url}${path}</loc>${mod}</url>`;
}

export const GET: APIRoute = async () => {
  const zh = await getArticles("zh");
  const en = await getArticles("en");
  const urls = [
    ...STATIC.map((p) => loc(p)),
    ...zh.map((a) => loc(articlePath(a), a.entry.data.pubDate)),
    ...en.map((a) => loc(articlePath(a), a.entry.data.pubDate)),
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join("\n")}
</urlset>`;
  return new Response(xml, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
};
