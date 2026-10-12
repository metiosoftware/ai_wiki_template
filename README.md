# AI Wiki Template — Living Knowledge Engine for Human + AI Collaboration

[![Wiki Integrity Lint](https://github.com/metiosoftware/ai-wiki-template/actions/workflows/wiki-lint.yml/badge.svg)](https://github.com/metiosoftware/ai-wiki-template/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A production-ready, 3-layer Git knowledge repository designed for pairing human teams with autonomous AI coding agents (**Claude Code**, **Antigravity**, **Cursor**, **Codex**, **Pi**).

It provides an authoritative source of truth that prevents context decay, stops hallucinated architecture decisions, and maintains documentation health with automated CI/CD linting.

---

## Why an AI Wiki?

Most AI-assisted development efforts run into a predictable breakdown:

1. **The Context Trap**: Teams feed large, uncurated documents or Notion exports into conversation windows. The model mixes 2-year-old brainstorming notes with yesterday's production architecture.
2. **The RAG Dilemma**: Naive semantic search retrieves text based on keyword similarity without understanding **temporal freshness** or **decision authority**. A rejected 2023 design proposal gets equal weight to an approved 2026 Architectural Decision Record (ADR).
3. **The Silent Decay**: Documentation without enforcement quickly becomes obsolete. Broken links multiply, orphans accumulate, and teams lose trust in the AI's answers.

### The Solution: The "LLM OS" File System Model
Popularized by AI researcher Andrej Karpathy, the model treats:
- The **LLM** as the CPU,
- The **Context Window** as working RAM,
- A structured, versioned **Git Markdown Wiki** as the deterministic hard drive.

This template turns that concept into an operational engine with **Trust Factors**, **Role-Aware queries**, **Automated Ingestion**, and **CI/CD Linting**.

---

## Architecture: The Three Layers

```
[Incoming Sources: Briefs, Notes, Transcripts, Specs, PDFs]
                          │
                          ▼ (wiki-ingest, doc-reader, wiki-get)
┌────────────────────────────────────────────────────────┐
│                      RAW LAYER                         │
│  raw/          Immutable input drop-zone               │
│  raw/assets/   Visual assets, diagrams, charts        │
│  raw/archive/  Processed sources archived here         │
└─────────────────────────┬──────────────────────────────┘
                          │
                          ▼ (Structured compilation)
┌────────────────────────────────────────────────────────┐
│                      WIKI LAYER                        │
│  wiki/index.md          Complete catalog of pages      │
│  wiki/log.md            Append-only audit trail        │
│  wiki/architecture/     System topology & tech stack   │
│  wiki/decisions/        Architecture Decision Records  │
│  wiki/requirements/     Specs, PRDs, user stories      │
│  wiki/guides/           Playbooks & workflows          │
│  wiki/glossary/         Canonical terminology          │
└─────────────────────────┬──────────────────────────────┘
                          │
                          ▼ (wiki-query, wiki-lint, wiki-export)
┌────────────────────────────────────────────────────────┐
│                    EXECUTION LAYER                     │
│  AGENTS.md      Operating manual & authority rules     │
│  .claude/skills Workflow skills for Claude & AGY       │
│  Continuous CI  Automated linter in GitHub Actions     │
└────────────────────────────────────────────────────────┘
```

| Layer | Path | Owner | Mutability | Purpose |
|---|---|---|---|---|
| **Sources** | `raw/` | User | **Immutable** | Drop-zone for raw inputs. LLMs read, never overwrite. Processed files are archived. |
| **Wiki** | `wiki/` | **LLM & Team** | **Mutable** | Reconciled living knowledge base. Structured Markdown with YAML frontmatter. |
| **Schema** | `AGENTS.md` | Both | **Living Law** | System rules, frontmatter schema, authority hierarchy, anti-AI prose standards. |

---

## Directory Layout

```
.
├── AGENTS.md                  ← Universal agent manual, authority rules & schema
├── CLAUDE.md                  ← Claude Code entry point (@AGENTS.md import)
├── README.md                  ← Human onboarding & project documentation
├── .agents/skills.json        ← Antigravity config referencing .claude/skills/
├── .claude/skills/            ← Canonical skill definitions & helper scripts
│   ├── wiki-ingest/           ← Compile sources from raw/ into wiki/
│   ├── wiki-query/            ← Role-aware answers with exact citations
│   ├── wiki-lint/             ← Health-check wiki links, categories & frontmatter
│   ├── wiki-get/              ← Fetch web sources into raw/
│   ├── doc-reader/            ← Extract CSV / TXT / DOCX / XLSX / PDF → Markdown
│   └── wiki-export/           ← Convert drafts to rich text (1-click copy)
├── .github/workflows/         ← CI/CD automation
│   └── wiki-lint.yml          ← Automated linting on push & PR
├── raw/                       ← Immutable source documents
│   ├── assets/                ← Visual assets, diagrams, charts, screenshots
│   └── archive/               ← Ingested sources moved here after compilation
└── wiki/                      ← The living knowledge base
    ├── index.md               ← Complete catalog of all pages
    ├── log.md                 ← Append-only activity log
    ├── overview.md            ← System topology & architectural charter
    ├── architecture/          ← High-level designs, data flows & stack choices
    ├── decisions/             ← Architectural Decision Records (ADRs)
    ├── requirements/          ← Specifications, PRDs, user stories & scope
    ├── guides/                ← Developer onboarding, workflows & playbooks
    └── glossary/              ← Ubiquitous language, acronyms & definitions
```

---

## Built-In Agent Skills & Toolchain

The template includes turnkey agent skills located in `.claude/skills/` and mapped for Antigravity via `.agents/skills.json`:

| Skill | Command / Script | Purpose |
|---|---|---|
| **`wiki-lint`** | `python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/` | Validates frontmatter, category mapping, broken links, and index completeness. |
| **`wiki-ingest`** | Prompt `/wiki-ingest` | Reads incoming files in `raw/`, categorizes into `wiki/`, updates `index.md`, logs to `log.md`, and archives sources. |
| **`wiki-query`** | Prompt `/wiki-query` | Synthesizes role-aware answers citing exact file paths and line ranges. Respects ADR authority. |
| **`wiki-get`** | `python .claude/skills/wiki-get/scripts/fetch_url.py <URL> raw/` | Downloads web articles or docs into clean Markdown snapshots in `raw/`. |
| **`doc-reader`** | `python .claude/skills/doc-reader/scripts/convert_doc.py <file>` | Converts CSV tables, text logs, or DOCX/XLSX/PDFs into Markdown for ingestion. |
| **`wiki-export`** | `python .claude/skills/wiki-export/scripts/export_doc.py <file> --open` | Generates an interactive HTML preview with **1-click rich-text copying** for Google Docs, Notion, Confluence, or LinkedIn. |

---

## Quickstart

### 1. Clone & Use as Template
Click **"Use this template"** on GitHub or clone locally:
```bash
git clone https://github.com/metiosoftware/ai-wiki-template.git my-project-wiki
cd my-project-wiki
```

### 2. Verify Wiki Health
Run the integrity linter to verify zero broken links or orphan pages:
```bash
# Windows
python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/

# Linux / macOS
python3 .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
```

### 3. Ingest Your First Document
1. Drop a meeting transcript, project brief, or architecture note into `raw/` (e.g. `raw/project-brief.txt`).
2. Ask your AI coding assistant:
   > *"Ingest raw/project-brief.txt into the wiki following our schema."*
3. The agent compiles structured pages into `wiki/`, updates `wiki/index.md`, appends to `wiki/log.md`, and archives the file into `raw/archive/`.

### 4. Query the Knowledge Base
Ask your agent:
   > *"Based on our wiki, what persistence layer did we choose and what are its invariants?"*
The agent uses `wiki-query` to return exact citations from [wiki/decisions/ADR-001-record-architecture-decisions.md](file:///wiki/decisions/ADR-001-record-architecture-decisions.md) and [wiki/architecture/system-overview.md](file:///wiki/architecture/system-overview.md).

### 5. Export to Google Docs / Notion / Confluence
When you need to share a decision or spec externally:
```bash
python .claude/skills/wiki-export/scripts/export_doc.py wiki/architecture/system-overview.md --open
```
Click **"📋 Copy Rich Text"** in the browser toolbar and press `Ctrl+V` into your target editor. Headings, lists, code styling, and tables are preserved natively.

---

## Adapting to Other Project Domains

While the default directory structure is optimized for **Software & Digital Product Engineering**, the template is completely modular and adapts to any domain:

### Archetype A: Software & Product Engineering (Default)
```
wiki/
├── architecture/   ← System topologies, components & service contracts
├── decisions/      ← Architecture Decision Records (ADRs)
├── requirements/   ← PRDs, feature specs & acceptance criteria
├── guides/         ← Developer workflows & local environment setups
└── glossary/       ← Ubiquitous language & acronyms
```

### Archetype B: Company & Team Operations
```
wiki/
├── processes/      ← Team operating procedures & release checklists
├── policies/       ← Security policies, PTO guidelines & compliance rules
├── onboarding/     ← Role-specific onboarding playbooks
├── projects/       ← Active initiative overviews & status dashboards
└── glossary/       ← Company terminology & organization index
```

### Archetype C: Research & Domain Intelligence
```
wiki/
├── concepts/       ← Foundational domain models & hypotheses
├── papers/         ← Summaries of external research & literature
├── experiments/    ← Methodology logs, datasets & benchmark runs
├── analysis/       ← Comparative analyses & findings
└── glossary/       ← Technical terms, variables & mathematical definitions
```

### Archetype D: Content & Brand Engine
```
wiki/
├── voice/          ← Tone of voice guidelines & hook frameworks
├── brand/          ← Company profile, value propositions & target personas
├── pillars/        ← Core editorial themes & content pillars
├── drafts/         ← Article drafts & queue in progress
└── glossary/       ← Brand lexicon & approved hashtags
```

*Note: The built-in `wiki-lint` script automatically detects any new folder name and its plural/singular variations without requiring custom configuration.*

---

## License

MIT © 2026 Metio Software & Contributors. Feel free to use, modify, and distribute this template for personal, commercial, or open-source projects.
