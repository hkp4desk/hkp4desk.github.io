import rss from "@astrojs/rss";
import type { APIRoute } from "astro";
import { site } from "../../lib/ui";
import { getArticles } from "../../lib/articles";

export const GET: APIRoute = async () => {
  const articles = await getArticles("en");
  return rss({
    title: site.title.en,
    description: site.tagline.en,
    site: site.url,
    customData: `<language>en</language>`,
    items: articles.map((a) => ({
      title: a.entry.data.title,
      description: a.entry.data.description,
      pubDate: a.entry.data.pubDate,
      link: `/en/articles/${a.slug}/`,
      guid: `en-${a.slug}`,
    })),
  });
};
