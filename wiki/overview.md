---
title: "Project Overview & System Charter"
category: architecture
status: approved
relevance: strategic
tags: [overview, architecture, knowledge-base]
sources: [initial-scaffold]
created: 2026-10-12
updated: 2026-10-12
author: team
---

# Project Overview & System Charter

Welcome to the **Project Knowledge Engine**. This repository is an AI-assisted living knowledge base designed for collaborative engineering, product architecture, and operational decisions.

---

## The 3-Layer Knowledge Architecture

This repository organizes information into three distinct layers, separating immutable raw inputs from synthesized knowledge and agent operating rules:

```
[Incoming Sources: Briefs, Notes, Transcripts, Specs]
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

---

## Directory Index & Navigation

- **[System Architecture](./architecture/system-overview.md)**: Foundational topology, component boundaries, and technology decisions.
- **[Decisions (ADRs)](./decisions/ADR-001-record-architecture-decisions.md)**: Architectural Decision Records documenting why choices were made.
- **[Requirements](./requirements/PRD-template.md)**: Functional requirements, acceptance criteria, and technical constraints.
- **[Guides & Operations](./guides/workflow-template.md)**: Developer onboarding, operational workflows, and local environments.
- **[Glossary](./glossary/terms.md)**: Domain lexicon, ubiquitous language, and acronym directory.

---

## Core Operational Guidelines

1. **Immutable Ingest**: Place all incoming notes, meeting transcripts, briefs, or PDFs into `raw/`. Never overwrite original inputs.
2. **Canonical Source of Truth**: The `wiki/` directory is the single source of truth for humans and AI agents.
3. **No Hallucinations**: Never fabricate performance metrics, API endpoints, or client commitments. Ground statements in active pages.
4. **Automated Health Checks**: Keep links fresh and pages indexed. Run `wiki-lint` before committing changes:
   ```bash
   python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
   ```
