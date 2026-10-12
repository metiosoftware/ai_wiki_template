---
title: "Project Glossary & Ubiquitous Language"
category: glossary
status: approved
relevance: reference
tags: [glossary, terminology, ubiquitous-language]
sources: [initial-scaffold]
created: 2026-10-12
updated: 2026-10-12
author: team
---

# Project Glossary & Ubiquitous Language

Canonical dictionary defining shared terms, system concepts, and acronyms across the project.

---

## Core Definitions

### ADR (Architectural Decision Record)
A lightweight document capturing an important architectural decision, including its context, alternatives considered, and consequences. See [ADR-001](../decisions/ADR-001-record-architecture-decisions.md).

### AI Wiki
A 3-layer Git-based knowledge repository (`raw/`, `wiki/`, `schema/`) maintained collaboratively by human engineers and autonomous AI agents.

### Invariant
A non-negotiable rule, constraint, or condition in the system that must remain true across all operations and state transitions.

### PRD (Product Requirements Document)
A formal specification outlining the purpose, features, functionality, and behavior of a product or major capability. See [PRD Template](../requirements/PRD-template.md).

### Trust Factor
The weighting mechanism used by agents to prioritize information: approved decisions (`status: approved`) always take precedence over working drafts (`status: draft`), and fresh documentation takes precedence over legacy notes.
