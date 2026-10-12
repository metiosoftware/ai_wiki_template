# AI Wiki — Schema & Agent Operating Manual

This repository is an **LLM-maintained living wiki and project intelligence engine**.
Raw source documents (notes, transcripts, specifications, data exports, research papers, slide decks) go into `raw/`.
The AI agent (Claude Code, Antigravity, Cursor, Codex, Pi) compiles them into structured, interlinked Markdown pages under `wiki/`, and uses that curated knowledge to accelerate engineering, product design, research, or content creation.

This document is the **operating manual and schema definition**. It is read automatically by all agents working in this repository:
- **Claude Code**: reads via `CLAUDE.md` (`@AGENTS.md` import)
- **Cursor**: reads via `AGENTS.md` and `.cursorrules`
- **Antigravity / Gemini**: reads via `GEMINI.md`, `.agents/`, and `AGENTS.md`
- **OpenAI / Codex / Copilot**: reads via `.github/copilot-instructions.md` and `AGENTS.md`
- **Qwen & Open Models (Aider, Windsurf, Cline)**: reads via `AGENTS.md` natively

---

## The Three Layers

| Layer | Path | Owner | Mutability | Purpose |
|---|---|---|---|---|
| **Sources** | `raw/` | User | **Immutable** | Raw incoming notes, transcripts, PDFs, data tables. Agents read, never edit in-place. |
| **Wiki** | `wiki/` | **Agent & Team** | **Mutable** | Reconciled living knowledge base: architecture, ADRs, requirements, playbooks, glossary. |
| **Schema** | `AGENTS.md` | Both | **Living Law** | Directory mappings, frontmatter schemas, authority hierarchy, prose guidelines. |

---

## Directory Structure

```
.
├── AGENTS.md                  ← Core instructions, schema, agent rules (this file)
├── CLAUDE.md                  ← Claude Code entry point (@AGENTS.md import)
├── README.md                  ← Human onboarding & project documentation
├── .agents/skills.json        ← Antigravity config referencing .claude/skills/
├── .claude/skills/            ← Canonical skill definitions & helper scripts
│   ├── wiki-ingest/           ← Compile sources from raw/ into wiki/
│   ├── wiki-query/            ← Role-aware answers with exact citations
│   ├── wiki-lint/             ← Health-check wiki links, categories & frontmatter
│   ├── wiki-get/              ← Fetch web sources into raw/
│   └── doc-reader/            ← Extract CSV / TXT / DOCX / XLSX / PDF → Markdown
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

## Page Conventions & Schema

Every page in `wiki/` must be Markdown formatted with a YAML frontmatter block:

```yaml
---
title: "Document or Feature Title"
category: architecture | decision | requirement | guide | process | concept | analysis | reference | glossary
status: draft | review | approved | deprecated | evergreen
relevance: strategic | tactical | reference | both
tags: [tag1, tag2, tag3]
sources: [raw/source-file.pdf]
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: username
---
```

### Directory → Category Mapping

| Directory | `category` value | Content Description |
|---|---|---|
| `architecture/` | `architecture` | System topologies, subsystem boundaries, data contracts, mental models |
| `decisions/` | `decision` | Architectural Decision Records (ADRs) with context, choice & consequences |
| `requirements/` | `requirement` | PRDs, feature specifications, acceptance criteria, constraints |
| `guides/` | `guide` | Developer workflows, operational playbooks, setup procedures |
| `processes/` | `process` | Team operating procedures, release checklists, governance |
| `concepts/` | `concept` | Foundational domain concepts, algorithmic deep-dives |
| `analysis/` | `analysis` | Benchmarks, retrospectives, performance profiles, trade-off evaluations |
| `reference/` | `reference` | Cheat sheets, external standards, compliance checklists |
| `glossary/` | `glossary` | Ubiquitous language, project dictionary, approved terminology |

The script `.claude/skills/wiki-lint/scripts/wiki-lint.py` strictly validates this mapping.

### Frontmatter Values

- **`status`**:
  - `draft`: Work in progress; exploratory; not yet binding.
  - `review`: Ready for peer or architectural review.
  - `approved`: Binding, canonical specification or active ADR.
  - `deprecated`: Retained for historical context; superseded by a newer page.
  - `evergreen`: Living document that evolves continuously (e.g., glossary, index).
- **`relevance`**:
  - `strategic`: High-level principles, overarching architecture, long-term goals.
  - `tactical`: Implementation details, sprint tasks, temporary experiments.
  - `reference`: Dictionaries, API schemas, benchmark tables.
  - `both`: Spans both high-level design and concrete implementation.

---

## Authority Order & Information Hierarchy

When synthesizing answers, drafting code, or making technical decisions, agents must observe the following authority hierarchy:

1. **Approved ADRs (`wiki/decisions/`) and Specifications (`wiki/requirements/`) are Absolute Law**.
   - If an idea in discussion conflicts with an approved ADR, the ADR wins unless an explicit proposal to amend or supersede the ADR is under review.
2. **Trust Factor & Temporal Freshness**:
   - `status: approved` outranks `status: draft`.
   - Newer timestamps (`updated: YYYY-MM-DD`) take precedence over older notes unless explicitly marked `deprecated`.
   - If two documents contradict each other, surface the discrepancy explicitly with exact file citations.
3. **Never Fabricate Facts or Metrics**:
   - Never invent APIs, throughput benchmarks, client commitments, or test results.
   - If data is missing, request it or mark it as an open question.
4. **Mandatory Interlinking**:
   - Every page must link to related pages and be referenced in `wiki/index.md`. No orphan pages are permitted.

---

## Role-Aware Context Synthesis

When answering questions or generating specifications via `wiki-query`, agents must determine the inquirer's role before or during synthesis. If the role is unstated or ambiguous, briefly prompt the user to confirm their lens (or frame the answer through the primary technical lens while offering others):

- **Architect**: Emphasize systemic invariants, modular decoupling, trade-offs, failure modes, data lifecycle, and ADR justification.
- **Developer / Engineer**: Emphasize concrete interfaces, data types, error handling, reproduction steps, code snippets, and setup commands.
- **Product Manager / Tech Lead**: Emphasize functional scope, acceptance criteria, milestone dependencies, release blockers, and user impact.
- **Researcher / Stakeholder**: Emphasize high-level conclusions, evidence, methodology, and strategic context.

---

## Anti-AI Mannerisms & High-Craft Prose Standards

To ensure documentation remains natural, engaging, and professional for human readers, agents must adhere to the following prose standards:

1. **No Mechanical Bold-Colon Catalogs**:
   - Avoid formatting technical explanations as repetitive bullet lists: `- **Item**: definition...`.
   - Write structured, continuous prose in cohesive paragraphs.
2. **No Nested Sub-Bullet Sprawl**:
   - Ban nesting bullet points 3 levels deep. If explaining complex architecture, break it into named sections with clear subheadings.
3. **High Signal-to-Noise Ratio**:
   - Every sentence must deliver concrete facts, steps, or insights. Prune empty filler phrases (*"It is important to remember that..."*, *"In order to achieve optimal performance..."*).
4. **No Raw Schema Dumping**:
   - Never dump internal schema fields directly into article or user copy (e.g., *"using metadata: status: approved"*). Explain the engineering meaning instead.
5. **Clean Subheadings Without Melodrama**:
   - Avoid sensationalist headings (*"Why Traditional Approaches Die a Silent Death"*).
   - Use grounded, informative headers (*"Why Unmaintained Knowledge Bases Decay Over Time"*).
6. **Moderate Punctuation (Dash Diet)**:
   - Avoid overusing dashes (`–` or `—`). Prefer crisp sentence splits with periods, or natural commas and conjunctions.
7. **Plain ASCII Trees**:
   - Avoid bloating directory trees with bracketed English acronyms or redundant explanations. Keep descriptions pragmatic and clean.
8. **Humble, Balanced Discussions**:
   - When soliciting feedback or writing post-mortems, invite both positive and critical observations.

---

## Core Operations

### 1. Ingest New Sources (`wiki-ingest`)
1. Place incoming source document into `raw/`.
2. If binary (PDF, Word, Excel), extract text first via `doc-reader`:
   ```bash
   python .claude/skills/doc-reader/scripts/convert_doc.py raw/<file.ext> raw/
   ```
3. Extract core concepts, architecture, or requirements into structured pages under `wiki/`.
4. Add YAML frontmatter to every created page.
5. Update catalog in `wiki/index.md` and append entry to `wiki/log.md`.
6. Move raw source to `raw/archive/<filename>`.
7. Run `wiki-lint` to confirm zero broken links or orphan pages.

### 2. Synthesize Answers (`wiki-query`)
1. Ascertain the user's role (Architect, Developer, Product Manager, Stakeholder). Ask or confirm if not evident.
2. Consult `wiki/index.md` and `wiki/overview.md`.
3. Gather relevant pages, weighting by Trust Factor (`status: approved` > `status: draft`).
4. Formulate an answer tailored to the user's role with exact citations (`path/to/page.md#L10-L20`).

### 3. Fetch Web Knowledge (`wiki-get`)
```bash
python .claude/skills/wiki-get/scripts/fetch_url.py <URL> raw/
```
Captures clean markdown snapshots with provenance headers into `raw/` ready for ingestion.

### 4. Health Check (`wiki-lint`)
```bash
python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
```
Validates frontmatter, category alignment, internal links, and index completeness.

---

## Domain Archetypes & Adapting This Template

This repository template is deliberately modular. While initialized with an engineering default (`architecture/`, `decisions/`, `requirements/`, `guides/`), you can adapt the folders to any domain:

### Archetype A: Software & Product Engineering (Default)
`architecture/`, `decisions/`, `requirements/`, `components/`, `services/`, `deployment/`, `glossary/`

### Archetype B: Company & Team Operations
`processes/`, `policies/`, `onboarding/`, `people/`, `projects/`, `glossary/`

### Archetype C: Research & Intelligence
`concepts/`, `papers/`, `experiments/`, `analysis/`, `reference/`, `glossary/`

### Archetype D: Content & Brand Engine
`voice/`, `brand/`, `pillars/`, `posts/`, `drafts/`, `analysis/`, `glossary/`

The built-in linter automatically recognizes categories matching any folder name (and handles plural/singular conversions).

---

## Project-Specific Guardrails & Non-Negotiables

*(Add your team's specific architectural invariants, tech stack constraints, security requirements, and taboos here.)*

- **Guardrail 1**: [Define your non-negotiable tech stack or architectural rule]
- **Guardrail 2**: [Define your data privacy or security constraint]
- **Guardrail 3**: [Define forbidden dependencies, patterns, or antipatterns]
