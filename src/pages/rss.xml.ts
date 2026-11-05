import rss from "@astrojs/rss";
import type { APIRoute } from "astro";
import { site } from "../lib/ui";
import { getArticles } from "../lib/articles";

export const GET: APIRoute = async () => {
  const articles = await getArticles("zh");
  return rss({
    title: site.title.zh,
    description: site.tagline.zh,
    site: site.url,
    customData: `<language>zh-Hant</language>`,
    items: articles.map((a) => ({
      title: a.entry.data.title,
      description: a.entry.data.description,
      pubDate: a.entry.data.pubDate,
      link: `/articles/${a.slug}/`,
      guid: `zh-${a.slug}`,
    })),
  });
};
