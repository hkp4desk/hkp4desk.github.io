import { getCollection, type CollectionEntry } from "astro:content";
import { type Locale } from "./ui";

export type Article = {
  slug: string;
  locale: Locale;
  entry: CollectionEntry<"articles">;
};

function toArticle(e: CollectionEntry<"articles">, locale: Locale): Article {
  return { slug: e.id.slice(locale.length + 1), locale, entry: e };
}

export async function getArticles(locale: Locale): Promise<Article[]> {
  const all = await getCollection("articles", (e) => !e.data.draft);
  return all
    .filter((e) => e.id.startsWith(locale + "/"))
    .map((e) => toArticle(e, locale))
    .sort(
      (a, b) =>
        b.entry.data.pubDate.getTime() - a.entry.data.pubDate.getTime()
    );
}

export function findArticle(
  articles: Article[],
  slug: string
): Article | undefined {
  return articles.find((a) => a.slug === slug);
}

export function articlePath(a: Article): string {
  return a.locale === "en" ? `/en/articles/${a.slug}/` : `/articles/${a.slug}/`;
}
