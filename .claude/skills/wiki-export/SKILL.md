---
name: wiki-export
description: Convert any Markdown wiki page, proposal, ADR, or draft into rich text with 1-click clipboard copy for Google Docs, Confluence, Notion, LinkedIn, or email.
---

# Wiki Export Skill

Use this skill when preparing to publish or share wiki documentation, specifications, architecture records, or articles in external tools (Google Docs, Notion, Confluence, LinkedIn Article, email).

## Workflow

1. **Convert to Rich Text Preview**:
   ```bash
   python .claude/skills/wiki-export/scripts/export_doc.py wiki/<path-to-file>.md --open
   ```

2. **1-Click Publishing**:
   - The generated HTML tool opens in the browser.
   - Click **„📋 Copy Rich Text“** to place formatted HTML onto the clipboard.
   - Paste (`Ctrl+V` / `Cmd+V`) into your target WYSIWYG editor. Headings, code blocks, bullet points, blockquotes, and bolding are preserved natively with zero raw markdown syntax.
