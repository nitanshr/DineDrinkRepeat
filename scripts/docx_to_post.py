#!/usr/bin/env python3
"""
Convert a .docx draft into Markdown/MDX content for DDR posts.

No paid services. No external Python dependencies.
Uses OOXML parsing from the .docx zip container.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = {"w": W_NS}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "untitled-post"


def parse_docx(document_path: Path) -> list[str]:
    with zipfile.ZipFile(document_path, "r") as zf:
        xml_bytes = zf.read("word/document.xml")

    root = ET.fromstring(xml_bytes)
    body = root.find("w:body", XML_NS)
    if body is None:
        return []

    lines: list[str] = []

    for paragraph in body.findall("w:p", XML_NS):
        style = paragraph.find("w:pPr/w:pStyle", XML_NS)
        style_val = style.attrib.get(f"{{{W_NS}}}val", "") if style is not None else ""

        texts: list[str] = []
        for run in paragraph.findall("w:r", XML_NS):
            text_nodes = run.findall("w:t", XML_NS)
            text = "".join(t.text or "" for t in text_nodes)
            if not text:
                continue

            run_props = run.find("w:rPr", XML_NS)
            is_bold = run_props is not None and run_props.find("w:b", XML_NS) is not None
            is_italic = run_props is not None and run_props.find("w:i", XML_NS) is not None

            if is_bold and is_italic:
                text = f"***{text}***"
            elif is_bold:
                text = f"**{text}**"
            elif is_italic:
                text = f"*{text}*"

            texts.append(text)

        full_text = "".join(texts).strip()
        if not full_text:
            continue

        if style_val in {"Heading1", "Title"}:
            lines.append(f"# {full_text}")
        elif style_val == "Heading2":
            lines.append(f"## {full_text}")
        elif style_val == "Heading3":
            lines.append(f"### {full_text}")
        else:
            # rough bullet detection
            if paragraph.find("w:pPr/w:numPr", XML_NS) is not None:
                lines.append(f"- {full_text}")
            else:
                lines.append(full_text)

    return lines


def build_frontmatter(args: argparse.Namespace, title: str) -> str:
    today = dt.date.today().isoformat()
    post_date = args.date or today
    tags = args.tags.split(",") if args.tags else ["menu"]
    tags = [t.strip() for t in tags if t.strip()]

    tag_lines = "\n".join(f"  - {t}" for t in tags)

    return f"""---
title: '{title}'
date: {post_date}
city: {args.city}
venue: {args.venue}
category: {args.category}
spiritCategory: {args.spirit_category}
tags:
{tag_lines}
heroImage: ../../../../_assets/sidecar-exterior.svg
heroImageAlt: 'Replace with a descriptive alt text for the chosen hero image.'
readingTime: {args.reading_time}
draft: true
---
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert .docx to DDR markdown post")
    parser.add_argument("docx", type=Path, help="Path to .docx file")
    parser.add_argument("--category", required=True, choices=["bars", "cocktails", "spirits", "guides"])
    parser.add_argument("--city", required=True, help="kebab-case city slug, e.g. delhi")
    parser.add_argument("--venue", default="Venue Placeholder")
    parser.add_argument("--spirit-category", default="gin")
    parser.add_argument("--tags", default="menu", help="Comma-separated tags")
    parser.add_argument("--date", help="YYYY-MM-DD")
    parser.add_argument("--reading-time", type=int, default=7)
    parser.add_argument("--year", default=str(dt.date.today().year))
    parser.add_argument("--month", default=f"{dt.date.today().month:02d}")
    parser.add_argument("--out-ext", choices=["md", "mdx"], default="mdx")
    args = parser.parse_args()

    if not args.docx.exists():
      print(f"Input file not found: {args.docx}", file=sys.stderr)
      return 1

    lines = parse_docx(args.docx)
    if not lines:
        print("No parseable text found in .docx", file=sys.stderr)
        return 1

    heading_line = next((ln for ln in lines if ln.startswith('#')), None)
    title_line = next((ln for ln in lines if ln and not ln.startswith('#')), None)
    title = heading_line or title_line or args.docx.stem.replace('-', ' ').title()
    title = re.sub(r"^#+\s*", "", title).strip()

    slug = slugify(args.docx.stem)
    target_dir = Path("src/content/posts") / args.category / args.city / args.year / args.month
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{slug}.{args.out_ext}"

    frontmatter = build_frontmatter(args, title)
    markdown_body = "\n\n".join(lines)

    target_file.write_text(frontmatter + "\n" + markdown_body + "\n", encoding="utf-8")
    print(f"Created: {target_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
