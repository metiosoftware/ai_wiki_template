#!/usr/bin/env python3
"""
Wiki Rich Text Exporter.
Converts any Markdown page or draft into a standalone interactive HTML preview
with 1-click Clipboard API rich-text copying for Google Docs, Notion, Confluence,
LinkedIn Articles, emails, and CMS editors.

Zero external dependencies.
"""

import sys
import os
import re
import html
import argparse
import webbrowser
from pathlib import Path


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


def extract_title_and_body(content: str) -> tuple[str, str]:
    """Extract page title and markdown body."""
    # Check frontmatter title first
    fm_title = None
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].splitlines():
                if line.startswith("title:"):
                    fm_title = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break

    cleaned = strip_frontmatter(content)

    # Check for # H1
    h1_match = re.search(r"^#\s+(.+)$", cleaned, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        body = cleaned[h1_match.end():].strip()
    elif fm_title:
        title = fm_title
        body = cleaned
    else:
        first_line = cleaned.splitlines()[0] if cleaned.splitlines() else "Document"
        title = re.sub(r"^[#\s*]+", "", first_line).strip()
        body = cleaned

    return title, body


def clean_markdown_inline(text: str) -> str:
    """Convert inline markdown formatting to safe styled HTML."""
    escaped = html.escape(text)

    # Inline code: `code`
    escaped = re.sub(
        r"`([^`]+)`",
        r'<code style="background-color: #f1f5f9; color: #0f172a; padding: 2px 6px; border-radius: 4px; font-family: Consolas, Monaco, ui-monospace, monospace; font-size: 0.88em;">\1</code>',
        escaped,
    )

    # Bold + Italic: ***text*** or ___text___
    escaped = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", escaped)

    # Bold: **text**
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)

    # Italic: *text* or _text_
    escaped = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"<em>\1</em>", escaped)

    # Strikethrough: ~~text~~
    escaped = re.sub(r"~~(.+?)~~", r"<del>\1</del>", escaped)

    # Links: [text](url)
    def link_replacer(match):
        link_text = match.group(1)
        url = match.group(2).strip()
        if url.startswith(("http://", "https://", "mailto:")):
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #2563eb; text-decoration: underline;">{link_text}</a>'
        # Relative internal wiki links -> preserve as strong text
        return f"<strong>{link_text}</strong>"

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replacer, escaped)
    return escaped


def markdown_to_rich_html(title: str, body_md: str) -> str:
    """Converts markdown body into formatted rich text HTML."""
    lines = body_md.splitlines()

    html_parts: list[str] = []
    in_code_block = False
    code_block_lines: list[str] = []

    in_list_type = None  # 'ul' or 'ol'
    list_items: list[str] = []

    in_blockquote = False
    blockquote_lines: list[str] = []

    def flush_list():
        nonlocal in_list_type, list_items
        if in_list_type and list_items:
            tag = in_list_type
            tag_style = "margin: 0.8em 0 1.2em 1.5em; padding-left: 0.5em; line-height: 1.6;"
            items_html = "".join(f'<li style="margin-bottom: 0.4em;">{it}</li>' for it in list_items)
            html_parts.append(f'<{tag} style="{tag_style}">{items_html}</{tag}>')
            in_list_type = None
            list_items = []

    def flush_blockquote():
        nonlocal in_blockquote, blockquote_lines
        if in_blockquote and blockquote_lines:
            combined = "<br>".join(blockquote_lines)
            style = "border-left: 4px solid #2563eb; padding: 8px 16px; margin: 1.2em 0; color: #334155; font-style: italic; background-color: #f8fafc;"
            html_parts.append(f'<blockquote style="{style}">{combined}</blockquote>')
            in_blockquote = False
            blockquote_lines = []

    for line in lines:
        stripped = line.strip()

        # Handle Code Fences
        if stripped.startswith("```"):
            if in_code_block:
                code_text = "\n".join(code_block_lines)
                code_escaped = html.escape(code_text)
                pre_style = (
                    "background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; "
                    "padding: 14px; overflow-x: auto; font-family: Consolas, Monaco, ui-monospace, monospace; "
                    "font-size: 13.5px; line-height: 1.5; white-space: pre; margin: 1.2em 0;"
                )
                html_parts.append(f'<pre style="{pre_style}"><code>{code_escaped}</code></pre>')
                in_code_block = False
                code_block_lines = []
            else:
                flush_list()
                flush_blockquote()
                in_code_block = True
                code_block_lines = []
            continue

        if in_code_block:
            code_block_lines.append(line)
            continue

        # Blank line triggers container flush
        if not stripped:
            flush_list()
            flush_blockquote()
            continue

        # Horizontal rule
        if re.match(r"^(\*{3,}|-{3,}|_{3,})$", stripped):
            flush_list()
            flush_blockquote()
            html_parts.append('<hr style="border: none; border-top: 1px solid #cbd5e1; margin: 2em 0;">')
            continue

        # Headings
        h_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if h_match:
            flush_list()
            flush_blockquote()
            level = len(h_match.group(1))
            h_text = clean_markdown_inline(h_match.group(2))

            if level == 1:
                html_parts.append(f'<h1 style="font-size: 26px; font-weight: 700; line-height: 1.3; margin: 1.5em 0 0.5em 0; color: #0f172a;">{h_text}</h1>')
            elif level == 2:
                html_parts.append(f'<h2 style="font-size: 22px; font-weight: 700; line-height: 1.35; margin: 1.4em 0 0.5em 0; color: #1e293b;">{h_text}</h2>')
            elif level == 3:
                html_parts.append(f'<h3 style="font-size: 18px; font-weight: 600; line-height: 1.4; margin: 1.2em 0 0.4em 0; color: #334155;">{h_text}</h3>')
            else:
                html_parts.append(f'<h4 style="font-size: 16px; font-weight: 600; line-height: 1.4; margin: 1em 0 0.3em 0; color: #475569;">{h_text}</h4>')
            continue

        # Blockquote
        if stripped.startswith(">"):
            flush_list()
            in_blockquote = True
            quote_content = re.sub(r"^>\s*", "", stripped)
            blockquote_lines.append(clean_markdown_inline(quote_content))
            continue
        elif in_blockquote:
            flush_blockquote()

        # Unordered list item
        ul_match = re.match(r"^[-*+]\s+(.+)$", stripped)
        if ul_match:
            if in_list_type != "ul":
                flush_list()
                in_list_type = "ul"
            list_items.append(clean_markdown_inline(ul_match.group(1)))
            continue

        # Ordered list item
        ol_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ol_match:
            if in_list_type != "ol":
                flush_list()
                in_list_type = "ol"
            list_items.append(clean_markdown_inline(ol_match.group(1)))
            continue

        # Normal text / paragraph
        flush_list()
        p_text = clean_markdown_inline(stripped)
        if line.endswith("  "):
            p_text += "<br>"

        html_parts.append(f'<p style="font-size: 16px; line-height: 1.65; margin: 0 0 1.1em 0; color: #1e293b;">{p_text}</p>')

    flush_list()
    flush_blockquote()
    return "\n".join(html_parts)


def build_standalone_preview_html(title: str, body_html: str, filename: str) -> str:
    """Wraps article HTML into an interactive preview with clipboard actions."""
    text_content = re.sub(r"<[^>]+>", " ", body_html)
    words = len(text_content.split())
    reading_time = max(1, round(words / 180))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} — Wiki Export</title>
  <style>
    :root {{
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: #0f172a;
      color: #f8fafc;
      padding: 12px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .topbar-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .badge {{
      background: var(--primary);
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .meta-text {{
      font-size: 12px;
      color: #94a3b8;
    }}
    .actions {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .btn {{
      appearance: none;
      border: none;
      cursor: pointer;
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .btn-primary {{
      background: var(--primary);
      color: #fff;
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}
    .btn-secondary {{
      background: #334155;
      color: #f8fafc;
    }}
    .btn-secondary:hover {{
      background: #475569;
    }}
    #toast {{
      display: none;
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999;
      background: #059669;
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }}
    .container {{
      max-width: 860px;
      margin: 32px auto 60px auto;
      padding: 0 20px;
    }}
    .sheet {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 48px 56px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.03);
    }}
    .header {{
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 2px solid var(--bg);
    }}
    .header h1 {{
      font-size: 32px;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.25;
    }}
    .header-info {{
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}
    @media (max-width: 640px) {{
      .sheet {{ padding: 24px 20px; }}
      .topbar {{ flex-direction: column; align-items: stretch; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-brand">
      <span class="badge">AI WIKI</span>
      <div>
        <div style="font-weight: 600; font-size: 14px;">Rich Text Exporter</div>
        <div class="meta-text">{html.escape(filename)} &bull; {words} words &bull; ~{reading_time} min read</div>
      </div>
    </div>
    <div class="actions">
      <button class="btn btn-secondary" onclick="copyTitle()">📝 Copy Title</button>
      <button class="btn btn-primary" onclick="copyRichText()">📋 Copy Rich Text</button>
    </div>
  </header>

  <div id="toast">✓ Copied to clipboard! Ready to paste into Google Docs / Notion / Confluence / LinkedIn.</div>

  <main class="container">
    <article class="sheet">
      <header class="header">
        <div class="header-info">Document &bull; {words} words &bull; {reading_time} min read</div>
        <h1 id="export-title">{html.escape(title)}</h1>
      </header>
      <div id="export-body">
{body_html}
      </div>
    </article>
  </main>

  <script>
    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => {{ t.style.display = 'none'; }}, 3500);
    }}

    async function copyTitle() {{
      const title = document.getElementById('export-title').innerText.trim();
      await navigator.clipboard.writeText(title);
      showToast('✓ Title copied to clipboard!');
    }}

    async function copyRichText() {{
      const bodyEl = document.getElementById('export-body');
      const htmlContent = bodyEl.innerHTML;
      const plainText = bodyEl.innerText;

      if (navigator.clipboard && window.ClipboardItem) {{
        try {{
          const blobHtml = new Blob([htmlContent], {{ type: 'text/html' }});
          const blobText = new Blob([plainText], {{ type: 'text/plain' }});
          const item = new ClipboardItem({{
            'text/html': blobHtml,
            'text/plain': blobText
          }});
          await navigator.clipboard.write([item]);
          showToast('✓ Rich text copied! Paste via Ctrl+V into Google Docs, Confluence, Notion or LinkedIn.');
          return;
        }} catch (e) {{
          console.warn('Clipboard API fallback:', e);
        }}
      }}

      const range = document.createRange();
      range.selectNodeContents(bodyEl);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      document.execCommand('copy');
      sel.removeAllRanges();
      showToast('✓ Rich text copied! Paste via Ctrl+V.');
    }}
  </script>
</body>
</html>
"""


def export_document(file_path: Path, output_path: Path = None, open_browser: bool = False) -> Path:
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    title, body_md = extract_title_and_body(content)
    body_html = markdown_to_rich_html(title, body_md)
    preview_html = build_standalone_preview_html(title, body_html, file_path.name)

    if output_path is None:
        exports_dir = file_path.parent / "exports"
        exports_dir.mkdir(parents=True, exist_ok=True)
        safe_stem = re.sub(r"[#\s]+", "-", file_path.stem).strip("-")
        output_path = exports_dir / f"{safe_stem}.preview.html"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(preview_html, encoding="utf-8")

    if open_browser:
        webbrowser.open(output_path.as_uri())

    return output_path


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Convert Markdown page into rich text / HTML export.")
    parser.add_argument("file", type=str, help="Path to markdown file.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Custom output HTML path.")
    parser.add_argument("--open", action="store_true", help="Open generated HTML in browser.")

    args = parser.parse_args()
    input_path = Path(args.file)

    try:
        out = export_document(input_path, Path(args.output) if args.output else None, open_browser=args.open)
        print(f"✓ Rich text export generated successfully: {out}")
        print("  Tip: Open the file in your browser to 1-click copy native rich text to your clipboard.")
    except Exception as ex:
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
