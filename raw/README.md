# Raw Sources Layer (`raw/`)

This directory is the **immutable input drop-zone** for external source materials before they are synthesized into the living `wiki/`.

---

## Operating Rules for Humans & AI Agents

1. **Immutable Ingestion Rule**:
   - The LLM and automation tools **only read** source files from `raw/`.
   - Never overwrite or silently modify original incoming files in `raw/`.

2. **Directory Layout**:
   - `raw/`: Drop incoming files here (`.md`, `.txt`, `.csv`, `.docx`, `.xlsx`, `.pdf`).
   - `raw/assets/`: Place diagrams, charts, UI screenshots, vector drawings, and presentation slides referenced by the wiki.
   - `raw/archive/`: Once a source file is processed and compiled into `wiki/` via `wiki-ingest`, it is moved here to maintain auditability.

3. **Workflow**:
   - Drop a document (e.g., `client-brief.pdf`, `meeting-notes.txt`, `benchmarks.csv`) into `raw/`.
   - Run `/doc-reader` if binary conversion is needed.
   - Run `/wiki-ingest` to extract, synthesize, and categorize into `wiki/`.
   - The processed file is moved to `raw/archive/`.
