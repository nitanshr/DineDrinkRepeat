# DDR Publishing Workflow (Google Docs → Site)

This repo supports two ways to publish from Google Docs.

## Option A) Manual copy/paste + checklist (lowest risk)

1. In Google Docs, finalize draft structure.
2. Copy content into the appropriate MDX template from `src/content/templates/`.
3. Save file to:
   - `src/content/posts/<category>/<city>/<year>/<month>/<post-slug>.mdx`
4. Fill frontmatter fields and keep `draft: true` until review.
5. Run checklist:
   - `npm run format`
   - `npm run lint`
   - verify tags/category match schema in `src/content/config.ts`
   - verify slug/city/spiritCategory are lowercase-kebab-case
6. When approved, set `draft: false`.

## Option B) Semi-automated `.docx` conversion (implemented)

Use a local script (no paid services, no external APIs) to convert a `.docx` export into a starter post.

### How it works

- Export Google Doc as `.docx`.
- Script reads OOXML (`word/document.xml`) directly.
- Converts paragraphs/headings/bullets to Markdown-like output.
- Generates DDR frontmatter with `draft: true`.
- Writes file into the SEO folder path.

### Command

```bash
python3 scripts/docx_to_post.py <path-to-docx> \
  --category bars \
  --city delhi \
  --venue "Venue Placeholder" \
  --spirit-category gin \
  --tags "bar-review,menu,delhi" \
  --reading-time 8 \
  --year 2026 \
  --month 04 \
  --out-ext mdx
```

Or via npm script:

```bash
npm run convert:docx -- <path-to-docx> --category bars --city delhi
```

### Output path

`src/content/posts/<category>/<city>/<year>/<month>/<docx-filename-slug>.mdx`

### Post-conversion checklist

- Replace placeholder `heroImage`, `heroImageAlt`, and `venue`.
- Validate tag values against allowed tags in `src/content/config.ts`.
- Review heading levels and bullet formatting.
- Run:
  - `npm run format`
  - `npm run lint`

## Recommendation

- Use **Option A** for high-touch feature stories.
- Use **Option B** for fast first-pass ingestion from Google Docs, then edit with templates before publish.
