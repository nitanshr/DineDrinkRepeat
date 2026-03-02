import { defineCollection, z } from 'astro:content';

export const ddrCategories = ['bars', 'cocktails', 'spirits', 'guides'] as const;

export const ddrTags = [
  'gin',
  'whisky',
  'vodka',
  'rum',
  'tequila',
  'delhi',
  'gurgaon',
  'bar-review',
  'menu',
  'event',
  'tasting-notes'
] as const;

const slugPart = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const posts = defineCollection({
  type: 'content',
  schema: ({ image }) =>
    z.object({
      title: z.string().min(5).max(120),
      date: z.coerce.date(),
      city: z
        .string()
        .toLowerCase()
        .regex(slugPart, 'Use lowercase-kebab-case city slugs, e.g. delhi or gurgaon'),
      venue: z.string().min(2).max(80),
      category: z.enum(ddrCategories),
      spiritCategory: z
        .string()
        .toLowerCase()
        .regex(slugPart, 'Use lowercase-kebab-case spirit category slugs, e.g. single-malt-whisky')
        .optional(),
      tags: z.array(z.enum(ddrTags)).min(1).max(8),
      heroImage: image(),
      heroImageAlt: z.string().min(10).max(180),
      readingTime: z.number().positive().max(60),
      draft: z.boolean().default(false)
    })
});

export const collections = {
  posts
};
