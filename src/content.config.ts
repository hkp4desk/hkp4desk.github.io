import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const articles = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/articles" }),
  schema: z.object({
    title: z.string(),
    description: z.string().default(""),
    pubDate: z.coerce.date(),
    p: z
      .array(z.enum(["prosperity", "projection", "prospect", "potential"]))
      .default([]),
    image: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { articles };
