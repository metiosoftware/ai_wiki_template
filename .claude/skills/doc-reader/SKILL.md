---
name: doc-reader
description: Convert documents and spreadsheets (CSV, TXT, DOCX, XLSX, PDF) in raw/ into clean plain-text or Markdown representations ready for wiki ingestion.
---

# Document Reader Skill

Use this skill when processing binary documents, spreadsheets, data tables, or PDFs placed in `raw/`.

## Workflow

1. **Detect Document Type**:
   - `.csv` / `.tsv`: tabular data, benchmarks, metric exports.
   - `.docx`: meeting notes, customer briefs, technical specs.
   - `.xlsx`: multi-sheet spreadsheets, estimation models, roadmap grids.
   - `.pdf`: whitepapers, compliance standards, architectural diagrams.

2. **Run Converter Script**:
   ```bash
   python .claude/skills/doc-reader/scripts/convert_doc.py raw/<filename.ext> raw/
   ```

3. **Hand-off to Wiki Ingestion**:
   - Trigger `wiki-ingest` on the resulting Markdown file to index and file content under the appropriate `wiki/` categories.
