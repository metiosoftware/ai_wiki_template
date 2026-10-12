---
title: "Developer Onboarding & Engineering Workflow"
category: guide
status: approved
relevance: tactical
tags: [workflow, guide, onboarding, development]
sources: [initial-scaffold]
created: 2026-10-12
updated: 2026-10-12
author: team
---

# Developer Onboarding & Engineering Workflow

This guide walks new contributors and AI agents through the development workflow, local environment setup, and verification routines.

---

## 1. Quickstart & Local Setup

1. **Clone & Configure**:
   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```

2. **Verify Dependencies**:
   Ensure Python 3.11+ is installed on your machine:
   ```bash
   python --version
   ```

3. **Validate Knowledge Base Health**:
   Run the wiki integrity linter to ensure all links and categories resolve cleanly:
   ```bash
   python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
   ```

---

## 2. Day-to-Day Development Workflow

1. **Check Requirements & ADRs**:
   Before modifying existing features or architecture, review related specifications in [wiki/requirements/PRD-template.md](../requirements/PRD-template.md) and approved decisions in [wiki/decisions/ADR-001-record-architecture-decisions.md](../decisions/ADR-001-record-architecture-decisions.md).

2. **Drafting or Updating Documentation**:
   - Place any incoming raw material into `raw/`.
   - Update or create pages under the corresponding `wiki/` subdirectory.
   - Always include standard YAML frontmatter (`title`, `category`, `status`, etc.).
   - Add new entries to [wiki/index.md](../index.md) and log changes in [wiki/log.md](../log.md).

3. **Pre-Commit Verification**:
   Always run the linter before pushing:
   ```bash
   python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
   ```
