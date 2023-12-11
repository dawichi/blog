import { defineCollection, z } from 'astro:content'

const blog = defineCollection({
    // Type-check frontmatter using a schema
    schema: z.object({
        title: z.string(),
        description: z.string(),
        // Transform string to Date object
        pubDate: z
            .string()
            .or(z.date())
            .transform(val => new Date(val)),
        heroImage: z.string(),
        tags: z.array(z.string()),
        visible: z.boolean(),
    }),
})

export const collections = { blog }
