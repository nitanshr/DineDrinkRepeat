# DineDrinkRepeat

Minimal, mobile-first Astro starter for DineDrinkRepeat.

## Stack

- Astro + TypeScript
- Markdown + MDX content collections
- ESLint + Prettier

## DDR Content Architecture

### Categories

- `bars`
- `cocktails`
- `spirits`
- `guides`

### Tags

Allowed tags:

- `gin`, `whisky`, `vodka`, `rum`, `tequila`
- `delhi`, `gurgaon`
- `bar-review`, `menu`, `event`, `tasting-notes`

### Post frontmatter schema

```yaml
title: string
date: YYYY-MM-DD
city: kebab-case string
venue: string
category: bars | cocktails | spirits | guides
spiritCategory: kebab-case string (optional)
tags: [allowed tags]
heroImage: local image path
heroImageAlt: string
readingTime: number (minutes)
draft: boolean
```

### SEO-friendly URL structure

Content file path drives slug. Posts are stored as:

`src/content/posts/<category>/<city>/<year>/<month>/<post-slug>.md(x)`

Published route:

`/stories/<category>/<city>/<year>/<month>/<post-slug>/`

Example:

`/stories/bars/delhi/2026/03/sidecar-delhi-bar-review/`

## Routes

- /
- /bars
- /cocktails
- /spirits
- /guides
- /about
- /newsletter
- /posts (archive)
- /stories/[...slug]

## Commands

```bash
npm install
npm run dev
npm run lint
npm run format
npm run build
```


## Publishing workflow

See `docs/publishing-workflow.md` for Google Docs → site publishing options (manual and semi-automated `.docx` conversion).
