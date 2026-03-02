# DDR Authoring Guide (Templates)

Use the MDX templates in `src/content/templates/` to create consistent editorial posts quickly.

## Available templates

1. `bar-review-template.mdx`
2. `cocktail-feature-template.mdx`
3. `event-takeover-recap-template.mdx`
4. `listicle-guide-template.mdx`

## How to use

1. Copy the closest template into `src/content/posts/<category>/<city>/<year>/<month>/<slug>.mdx`.
2. Update frontmatter fields to satisfy the content schema:
   - `title`, `date`, `city`, `venue`, `category`, `tags`, `heroImage`, `heroImageAlt`, `readingTime`, `draft`
   - optional: `spiritCategory`
3. Keep `city`, `spiritCategory`, and slug values in lowercase-kebab-case for URL consistency.
4. Replace all placeholders in:
   - TL;DR block
   - tasting-notes bullets
   - optional menu highlight callouts
5. Set `draft: false` only when ready to publish.

## Template conventions

- **TL;DR block:** always at the top for quick scanning.
- **Suggested section headings:** keep or adapt as needed.
- **Tasting notes placeholders:** retain structure for editorial consistency.
- **Menu highlight callouts:** optional; use blockquote callouts when relevant.
