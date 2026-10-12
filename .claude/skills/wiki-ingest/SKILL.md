---
name: wiki-ingest
description: Ingest and compile raw source documents (notes, transcripts, specifications, exports, research) from raw/ into structured Markdown pages under wiki/.
---

# Wiki Ingest Skill

Use this skill when importing new material from `raw/` into the living `wiki/`.

## Ingest Procedure

1. **Locate & Inspect Source**:
   - Check `raw/` for incoming files (`.md`, `.txt`, `.csv`, `.docx`, `.xlsx`, `.pdf`).
   - If the file is binary (PDF, Word, Excel), convert to plain text or clean Markdown first (using `doc-reader`).

2. **Analyze & Extract**:
   - Review the document to extract key concepts, architecture diagrams, technical decisions, specifications, or processes.
   - Map information into the relevant category:
     - `wiki/architecture/`: System design, data flow, mental models, technology stacks.
     - `wiki/decisions/`: Architectural Decision Records (ADRs) with rationale, options considered, and consequences.
     - `wiki/requirements/`: Functional and non-functional specifications, user stories, scopes.
     - `wiki/guides/`: Operational playbooks, developer guides, setup steps, processes.
     - `wiki/concepts/` or `wiki/analysis/`: Deep-dives, domain analysis, benchmarks.
     - `wiki/glossary/`: Ubiquitous language, definitions, acronyms.

3. **Format Markdown with Frontmatter**:
   - Every generated page must contain complete YAML frontmatter:
     ```yaml
     ---
     title: "Document Title"
     category: architecture | decision | requirement | guide | process | concept | analysis | glossary
     status: draft | review | approved | evergreen
     relevance: strategic | tactical | reference | both
     tags: [tag1, tag2]
     sources: [raw/source-filename.ext]
     created: YYYY-MM-DD
     updated: YYYY-MM-DD
     author: username
     ---
     ```

4. **Update Catalog & Log**:
   - Add the new page link and a concise 1-line summary to `wiki/index.md`.
   - Append an entry to `wiki/log.md` with timestamp, author, source, pages created/updated, and summary.

5. **Archive Source**:
   - Move processed source files from `raw/<filename>` to `raw/archive/<filename>`.
   - Never delete original source files.

6. **Verify Integrity**:
   - Run `wiki-lint` to ensure no broken links, orphan pages, or category mismatches:
     ```bash
     python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
     ```
