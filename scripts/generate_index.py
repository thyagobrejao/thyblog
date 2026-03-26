#!/usr/bin/env python3
"""
Generate the main index pages for the Hugo blog:
  - content/_index.md    (Português do Brasil)
  - content/_index.en.md (English)

Scans all markdown files in content/, extracts frontmatter metadata,
groups posts by year/month, and generates a chronological listing
with the most recent posts first.

Usage:
    python scripts/generate_index.py
"""

import os
import re
import sys
from datetime import datetime
from collections import defaultdict

# Project root is one level up from the scripts directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(PROJECT_ROOT, "content")
INDEX_FILE_PT = os.path.join(CONTENT_DIR, "_index.md")
INDEX_FILE_EN = os.path.join(CONTENT_DIR, "_index.en.md")

# Files and directories to skip
SKIP_FILES = {"_index.md", "_index.en.md", "about.md", "about.en.md"}
SKIP_DIRS = {".git", "public", "themes", "static", "assets"}

MONTH_NAMES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

MONTH_NAMES_EN = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}


def parse_frontmatter(filepath):
    """Extract frontmatter fields from a markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return None

    # Match YAML frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)
    data = {}

    # Parse simple YAML key-value pairs
    for line in frontmatter_text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("-"):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip("'\"")
            data[key] = value

    # Parse tags (list format)
    tags_match = re.search(
        r"tags:\s*\n((?:\s*-\s*.+\n?)+)", frontmatter_text
    )
    if tags_match:
        tags = re.findall(r"-\s*(.+)", tags_match.group(1))
        data["tags"] = [t.strip().strip("'\"") for t in tags]

    return data


def parse_date(date_str):
    """Parse a date string from frontmatter into a datetime object."""
    if not date_str:
        return None

    # Try ISO 8601 with timezone
    for fmt in [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]:
        try:
            return datetime.strptime(date_str.replace("'", "").replace('"', ""), fmt)
        except ValueError:
            continue

    # Handle timezone offset like -03:00
    cleaned = re.sub(r"([+-]\d{2}):(\d{2})$", r"\1\2", date_str)
    try:
        return datetime.strptime(cleaned, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def get_en_filepath(filepath):
    """Get the English translation filepath for a given pt-br file."""
    base, ext = os.path.splitext(filepath)
    return base + ".en" + ext


def collect_posts():
    """Walk the content directory and collect all post metadata (pt-br and en)."""
    posts_pt = []
    posts_en = []

    for root, dirs, files in os.walk(CONTENT_DIR):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            if not filename.endswith(".md"):
                continue
            if filename in SKIP_FILES:
                continue
            # Skip English translations (processed alongside pt-br)
            if filename.endswith(".en.md"):
                continue

            filepath = os.path.join(root, filename)
            frontmatter = parse_frontmatter(filepath)
            if not frontmatter:
                continue

            # Skip drafts
            if frontmatter.get("draft", "false").lower() == "true":
                continue

            # Skip coming soon pages
            if frontmatter.get("coming_soon", "false").lower() == "true":
                continue

            title_pt = frontmatter.get("title", os.path.splitext(filename)[0])
            date = parse_date(frontmatter.get("date", ""))
            tags_pt = frontmatter.get("tags", [])

            # Calculate relative path from content dir for the link
            rel_path = os.path.relpath(filepath, CONTENT_DIR)
            # Convert file path to Hugo URL path
            url_path = os.path.splitext(rel_path)[0]
            # Handle index files
            if url_path.endswith("/index"):
                url_path = url_path[:-6]
            # Handle _index files (section pages)
            if url_path.endswith("/_index") or url_path == "_index":
                continue

            url = "/" + url_path.replace(os.sep, "/") + "/"

            posts_pt.append({
                "title": title_pt,
                "date": date,
                "tags": tags_pt,
                "url": url,
            })

            # Try to get English translation
            en_filepath = get_en_filepath(filepath)
            title_en = title_pt  # fallback to pt-br title
            tags_en = tags_pt    # fallback to pt-br tags
            if os.path.exists(en_filepath):
                en_frontmatter = parse_frontmatter(en_filepath)
                if en_frontmatter:
                    title_en = en_frontmatter.get("title", title_pt)
                    tags_en = en_frontmatter.get("tags", tags_pt)

            posts_en.append({
                "title": title_en,
                "date": date,
                "tags": tags_en,
                "url": url,
            })

    # Sort by date, most recent first
    posts_pt.sort(key=lambda p: p["date"] or datetime.min, reverse=True)
    posts_en.sort(key=lambda p: p["date"] or datetime.min, reverse=True)
    return posts_pt, posts_en


def generate_index(posts, lang="pt"):
    """Generate the _index.md content with posts grouped by year/month."""
    lines = []
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")

    if lang == "en":
        month_names = MONTH_NAMES_EN
        title = "Blog Thyago.dev.br"
        header = "## 📝 Latest Posts"
        empty_msg = "No published posts yet. Stay tuned! 🚀"
        no_date = "### 📅 No date"
        date_fmt = "%m/%d/%Y"
    else:
        month_names = MONTH_NAMES_PT
        title = "Blog Thyago.dev.br"
        header = "## 📝 Últimos Posts"
        empty_msg = "Nenhum post publicado ainda. Em breve teremos novidades! 🚀"
        no_date = "### 📅 Sem data"
        date_fmt = "%d/%m/%Y"

    # Frontmatter
    lines.append("---")
    lines.append(f"date: '{now}'")
    lines.append("draft: false")
    lines.append(f"title: '{title}'")
    lines.append("cascade:")
    lines.append("  type: docs")
    lines.append("---")
    lines.append("")
    lines.append(header)
    lines.append("")

    if not posts:
        lines.append(empty_msg)
        return "\n".join(lines) + "\n"

    # Group by year/month
    grouped = defaultdict(list)
    for post in posts:
        if post["date"]:
            key = (post["date"].year, post["date"].month)
        else:
            key = (0, 0)
        grouped[key].append(post)

    # Sort keys by date descending
    sorted_keys = sorted(grouped.keys(), reverse=True)

    for year, month in sorted_keys:
        if year == 0:
            lines.append(no_date)
        else:
            month_name = month_names.get(month, "")
            lines.append(f"### 📅 {month_name} {year}")
        lines.append("")

        for post in grouped[(year, month)]:
            date_str = ""
            if post["date"]:
                date_str = post["date"].strftime(date_fmt)

            tag_str = ""
            if post["tags"]:
                tag_str = " — " + ", ".join(f"`{t}`" for t in post["tags"])

            lines.append(f"- [{post['title']}]({post['url']}) *({date_str})*{tag_str}")

        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    print("🔍 Scanning content directory...")
    posts_pt, posts_en = collect_posts()
    print(f"📄 Found {len(posts_pt)} published post(s)")

    # Generate pt-br index
    content_pt = generate_index(posts_pt, lang="pt")
    with open(INDEX_FILE_PT, "w", encoding="utf-8") as f:
        f.write(content_pt)
    print(f"✅ Index generated (pt-br): {INDEX_FILE_PT}")

    # Generate en index
    content_en = generate_index(posts_en, lang="en")
    with open(INDEX_FILE_EN, "w", encoding="utf-8") as f:
        f.write(content_en)
    print(f"✅ Index generated (en): {INDEX_FILE_EN}")


if __name__ == "__main__":
    main()
