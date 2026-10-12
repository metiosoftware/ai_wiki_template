#!/usr/bin/env python3
"""
Wiki Get: Web content fetcher and markdown snapshot tool.
Downloads an external web page, extracts the readable text, and saves it
as an immutable snapshot in raw/ ready for ingestion.

Zero external dependencies (uses standard library urllib and html.parser).
"""

import sys
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


class SimpleHTMLToMarkdownParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.title = ""
        self._in_title = False
        self._in_script_or_style = False
        self._in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ("script", "style", "noscript"):
            self._in_script_or_style = True
        elif tag.lower() == "title":
            self._in_title = True
        elif tag.lower() in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag.lower() == "p":
            self.output.append("\n\n")
        elif tag.lower() == "br":
            self.output.append("\n")
        elif tag.lower() == "li":
            self.output.append("\n- ")
        elif tag.lower() == "pre":
            self._in_pre = True
            self.output.append("\n\n```\n")
        elif tag.lower() == "code" and not self._in_pre:
            self.output.append("`")

    def handle_endtag(self, tag):
        if tag.lower() in ("script", "style", "noscript"):
            self._in_script_or_style = False
        elif tag.lower() == "title":
            self._in_title = False
        elif tag.lower() == "pre":
            self._in_pre = False
            self.output.append("\n```\n")
        elif tag.lower() == "code" and not self._in_pre:
            self.output.append("`")

    def handle_data(self, data):
        if self._in_script_or_style:
            return
        if self._in_title:
            self.title += data.strip()
        else:
            self.output.append(data)

    def get_markdown(self) -> str:
        raw_text = "".join(self.output)
        # Collapse excessive newlines
        cleaned = re.sub(r"\n{3,}", "\n\n", raw_text).strip()
        return cleaned


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", slug).strip("-")[:60] or "snapshot"


def fetch_url(url: str, output_dir: Path) -> Path:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AIWikiFetcher/1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content_bytes = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            html_text = content_bytes.decode(charset, errors="replace")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}")

    parser = SimpleHTMLToMarkdownParser()
    parser.feed(html_text)
    body_md = parser.get_markdown()
    page_title = parser.title or "Web Snapshot"

    slug = slugify(page_title)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    header = f"""<!--
Source URL: {url}
Fetched: {timestamp}
Original Title: {page_title}
-->

# {page_title}

"""
    full_content = header + body_md + "\n"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{slug}.md"

    # Avoid overwriting
    counter = 1
    while out_file.exists():
        out_file = output_dir / f"{slug}-{counter}.md"
        counter += 1

    out_file.write_text(full_content, encoding="utf-8")
    return out_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_url.py <URL> [output_dir]")
        sys.exit(1)

    url = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("raw")

    try:
        saved_path = fetch_url(url, out_dir)
        print(f"✓ Fetched snapshot saved to: {saved_path}")
        print("Tip: Run /wiki-ingest to analyze and incorporate into wiki/")
    except Exception as ex:
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
