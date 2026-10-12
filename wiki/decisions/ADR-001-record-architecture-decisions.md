---
title: "ADR-001: Record Architecture Decisions"
category: decision
status: approved
relevance: strategic
tags: [adr, architecture, governance]
sources: [initial-scaffold]
created: 2026-10-12
updated: 2026-10-12
author: team
---

# ADR-001: Record Architecture Decisions

## Status
**Approved** (2026-10-12)

## Context
As the project grows in complexity and team members (both engineers and autonomous AI agents) make decisions, we need a standard mechanism to record significant architectural choices along with their context, alternatives evaluated, and consequences.

Without explicit decision records, architectural rationale is lost in chat history or code reviews, leading to repeated debates and regressions.

## Decision
We will record all architecturally significant decisions in `wiki/decisions/` using lightweight Architectural Decision Records (ADRs).

Each ADR must contain:
1. **Title & Frontmatter**: Category set to `decision`, status (`draft`, `review`, `approved`, `superseded`), and relevant tags.
2. **Status**: Current lifecycle phase and decision date.
3. **Context**: The forces, constraints, and problem statement driving the decision.
4. **Decision**: The chosen course of action and technical path.
5. **Consequences**: Both positive advantages and negative tradeoffs or operational costs incurred.

## Consequences

### Positive
- **Institutional Memory**: Rationale is preserved directly within the Git repository.
- **Agent Authority**: AI agents can inspect `wiki/decisions/` to understand non-negotiable architectural constraints and avoid proposing deprecated patterns.
- **Clarity for New Contributors**: Onboarding developers can review past decisions chronologically.

### Tradeoffs
- Slight operational overhead to author and review an ADR before major refactorings or library changes.
