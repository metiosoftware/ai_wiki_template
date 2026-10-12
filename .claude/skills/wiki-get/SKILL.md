---
name: wiki-get
description: Fetch web articles, blog posts, documentation, API specs, or research papers from URLs and store them as raw Markdown snapshots in raw/ for ingestion.
---

# Wiki Get Skill

Use this skill to fetch external articles, partner documentation, technical specs, or research papers from the web and capture them into `raw/`.

## Procedure

1. **Fetch Content via Automation**:
   Run the zero-dependency fetch script:
   ```bash
   python .claude/skills/wiki-get/scripts/fetch_url.py <URL> raw/
   ```
   Or extract content using web reading tools and save directly to `raw/<kebab-slug>.md`.

2. **Snapshot Header Conventions**:
   Every fetched web snapshot in `raw/` must record:
   - Source URL
   - Timestamp of retrieval
   - Original page title

3. **Hand-off to Ingestion**:
   - Immediately prompt or proceed to run `wiki-ingest` to extract relevant insights, architectural patterns, or glossary terms into `wiki/`.
