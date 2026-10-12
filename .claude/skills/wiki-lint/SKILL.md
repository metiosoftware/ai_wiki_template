---
name: wiki-lint
description: Validate and audit the integrity of the AI wiki, checking YAML frontmatter, directory category matching, internal link validity, and index completeness.
---

# Wiki Lint Skill

Use this skill to audit wiki integrity, detect broken links, identify orphan pages, and verify frontmatter conformance.

## Automated Execution
Run the linter script directly from the repository root:

```powershell
# Windows (PowerShell)
$env:PYTHONIOENCODING="utf-8"; python .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
```

```bash
# Linux / macOS / WSL
python3 .claude/skills/wiki-lint/scripts/wiki-lint.py wiki/
```

## Validation Rules
1. **Frontmatter Schema**:
   - `title`: String describing the document.
   - `category`: Must match the directory type (e.g. `architecture`, `decision`, `requirement`, `guide`, `process`, `glossary`, etc.).
   - Recommended fields: `status`, `relevance`, `tags`, `sources`, `created`, `updated`, `author`.
2. **Directory Category Alignment**:
   - Subfolder pages must declare a matching `category` in their frontmatter.
3. **No Dead Links**:
   - Every internal link `[text](target)` must resolve to an existing file in `wiki/` or the repository.
4. **No Orphan Pages**:
   - Every page in `wiki/` (except `index.md` and `log.md`) must be cataloged and linked in `wiki/index.md`.
