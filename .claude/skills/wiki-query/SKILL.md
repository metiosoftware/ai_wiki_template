---
name: wiki-query
description: Query and synthesize project knowledge, architecture, decisions, and requirements from the wiki with role-aware synthesis and exact citations.
---

# Wiki Query Skill

Use this skill when answering technical, architectural, operational, or strategic questions using the project knowledge base.

## Query Strategy

1. **Ascertain Inquirer Role ("Wiki ví, komu odpovídá")**:
   - Before synthesizing, identify the user's role and perspective.
   - **If role is specified or evident** (e.g., *"As an architect...", "I'm coding the persistence layer..."*): Adopt that role's lens directly.
   - **If role is unstated or ambiguous**: Briefly ask the user:
     > *"To provide the exact level of detail you need, which lens should I answer from?*
     > *- **Architect** (system invariants, modular boundaries, trade-offs, ADR rationale)*
     > *- **Developer / Engineer** (interfaces, error handling, types, code implementation)*
     > *- **Product Manager / Tech Lead** (functional scope, acceptance criteria, milestones, blockers)*
     > *- **Stakeholder / Researcher** (high-level synthesis, evidence, business impact)*"
     *(If in a single-turn or non-interactive flow where stopping to ask would cause unnecessary friction, structure the answer primarily for Developer/Architect while providing a concise PM/Stakeholder summary at the top).*

2. **Locate Canonical Sources**:
   - Consult `wiki/index.md` and `wiki/overview.md` to identify relevant directories and pages.
   - For architecture & system design: check `wiki/architecture/` and component specs.
   - For technical decisions: check `wiki/decisions/` (ADRs).
   - For functional scope & user requirements: check `wiki/requirements/`.
   - For developer workflows & operational procedures: check `wiki/guides/`.
   - For definitions & domain terminology: check `wiki/glossary/`.

3. **Evaluate Trust Factor & Authority**:
   - **Authority Hierarchy**: Approved decisions (`status: approved`) take precedence over drafts or exploratory notes.
   - **Freshness**: Pay attention to the `updated` frontmatter date. If two documents conflict, flag the discrepancy and favor the more recent approved document.
   - **Ground Truth**: Ground all statements in active documentation or source files in `raw/`. Never invent facts, API signatures, or metrics.

4. **Role-Tailored Synthesis**:
   Adapt depth, terminology, and focus strictly according to the identified role:
   - **Architect**: Focus on system invariants, data flows, boundaries, tradeoffs, and ADR rationale.
   - **Developer / Engineer**: Focus on concrete interfaces, schema definitions, implementation steps, error scenarios, and code snippets.
   - **Product Manager / Tech Lead**: Focus on feature scope, requirements coverage, milestones, dependencies, and business constraints.
   - **Researcher / Stakeholder**: Focus on high-level takeaways, evidence, background context, and outcomes.

4. **Exact Citations**:
   - Always cite specific file paths and line numbers (e.g. `wiki/architecture/system-overview.md#L42-L60`).
   - If citing original source evidence, reference `raw/archive/<filename>`.
