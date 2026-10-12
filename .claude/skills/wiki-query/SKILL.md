---
name: wiki-query
description: Query and synthesize project knowledge, architecture, decisions, and requirements from the wiki with role-aware synthesis and exact citations.
---

# Wiki Query Skill

Use this skill when answering technical, architectural, operational, or strategic questions using the project knowledge base.

## Query Strategy

1. **Locate Canonical Sources**:
   - Consult `wiki/index.md` and `wiki/overview.md` to identify relevant directories and pages.
   - For architecture & system design: check `wiki/architecture/` and component specs.
   - For technical decisions: check `wiki/decisions/` (ADRs).
   - For functional scope & user requirements: check `wiki/requirements/`.
   - For developer workflows & operational procedures: check `wiki/guides/`.
   - For definitions & domain terminology: check `wiki/glossary/`.

2. **Evaluate Trust Factor & Authority**:
   - **Authority Hierarchy**: Approved decisions (`status: approved`) take precedence over drafts or exploratory notes.
   - **Freshness**: Pay attention to the `updated` frontmatter date. If two documents conflict, flag the discrepancy and favor the more recent approved document.
   - **Ground Truth**: Ground all statements in active documentation or source files in `raw/`. Never invent facts, API signatures, or metrics.

3. **Role-Aware Synthesis**:
   Adapt the depth, terminology, and focus to the user's role:
   - **Architect**: Focus on system invariants, data flows, boundaries, tradeoffs, and ADR rationale.
   - **Developer / Engineer**: Focus on concrete interfaces, schema definitions, implementation steps, error scenarios, and code snippets.
   - **Product Manager / Tech Lead**: Focus on feature scope, requirements coverage, milestones, dependencies, and business constraints.
   - **Researcher / Stakeholder**: Focus on high-level takeaways, evidence, background context, and outcomes.

4. **Exact Citations**:
   - Always cite specific file paths and line numbers (e.g. `wiki/architecture/system-overview.md#L42-L60`).
   - If citing original source evidence, reference `raw/archive/<filename>`.
