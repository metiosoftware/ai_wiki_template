#!/usr/bin/env python3
"""
AI Wiki Integrity Linter.

Audits and validates the health of the living wiki:
1. YAML frontmatter presence and required fields (title, category).
2. Category matches directory convention.
3. Internal markdown links resolve to existing target files.
4. All content pages are cataloged in wiki/index.md (no orphan pages).

Usage:
    python .claude/skills/wiki-lint/scripts/wiki-lint.py [wiki_dir]
"""

import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Built-in category mappings (directory name -> expected category frontmatter)
DEFAULT_CATEGORY_MAP = {
    # Engineering & Architecture
    "architecture": "architecture",
    "decisions": "decision",
    "requirements": "requirement",
    "components": "component",
    "services": "service",
    "deployment": "deployment",
    "protocols": "protocol",
    # Guides, Processes & Operations
    "guides": "guide",
    "processes": "process",
    "workflows": "workflow",
    "operations": "operation",
    # Concepts, Research & Analysis
    "concepts": "concept",
    "analysis": "analysis",
    "reference": "reference",
    "research": "research",
    # Editorial, Strategy & Content
    "brand": "brand",
    "voice": "voice",
    "pillars": "pillar",
    "posts": "post",
    "drafts": "draft",
    # Universal
    "glossary": "glossary",
}

REQUIRED_FRONTMATTER = ["title", "category"]
SPECIAL_ROOT_FILES = {"index.md", "log.md"}


def parse_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter block if present."""
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    fm_raw = parts[1]
    data = {}
    for line in fm_raw.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            data[key] = val
    return data


def find_markdown_links(content: str) -> list[str]:
    """Find all internal markdown file links."""
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    links = []
    for match in re.finditer(pattern, content):
        url = match.group(2).strip()
        # Skip external links
        if url.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        # Clean file:/// prefix
        if url.startswith("file:///"):
            url = url[8:]
        # Separate internal anchors
        if ".md#" in url:
            url = url.split("#")[0]
        elif url.startswith("#"):
            url = ""
        elif "#" in url and not url.endswith(".md"):
            url = url.split("#")[0]

        if url:
            links.append(url)
    return links


def matches_category(parent_dir: str, actual_category: str | None) -> bool:
    """Verify if category matches directory naming or standard conventions."""
    if not actual_category:
        return False
    
    # Exact map match
    if parent_dir in DEFAULT_CATEGORY_MAP:
        if actual_category == DEFAULT_CATEGORY_MAP[parent_dir]:
            return True

    # Exact directory name match
    if actual_category == parent_dir:
        return True

    # Plural-to-singular deduction (e.g. 'guides' -> 'guide', 'policies' -> 'policy')
    if parent_dir.endswith("ies") and actual_category == parent_dir[:-3] + "y":
        return True
    if parent_dir.endswith("s") and actual_category == parent_dir[:-1]:
        return True

    return False


def lint_wiki(wiki_root: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    all_files = sorted(list(wiki_root.rglob("*.md")))
    file_rel_paths = {p.relative_to(wiki_root).as_posix(): p for p in all_files}

    index_path = wiki_root / "index.md"
    index_content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    for file_path in all_files:
        rel_posix = file_path.relative_to(wiki_root).as_posix()
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"[{rel_posix}] Unable to read file: {e}")
            continue

        filename = file_path.name

        # Validate frontmatter on non-exempt files
        if filename not in SPECIAL_ROOT_FILES:
            fm = parse_frontmatter(content)
            if fm is None:
                errors.append(f"[{rel_posix}] Missing YAML frontmatter block (---).")
            else:
                for req in REQUIRED_FRONTMATTER:
                    if req not in fm:
                        errors.append(f"[{rel_posix}] Missing required frontmatter field: '{req}'.")

                # Validate category alignment if inside a subfolder
                parent_dir = file_path.parent.name
                if file_path.parent != wiki_root:
                    actual_cat = fm.get("category")
                    if not matches_category(parent_dir, actual_cat):
                        expected = DEFAULT_CATEGORY_MAP.get(parent_dir, parent_dir.rstrip("s"))
                        errors.append(
                            f"[{rel_posix}] Category mismatch: expected '{expected}', found '{actual_cat}'."
                        )

        # Validate internal links
        links = find_markdown_links(content)
        for link in links:
            # Try 1: Relative to current file's directory
            target = (file_path.parent / link).resolve()
            if target.exists():
                continue

            # Try 2: Relative to wiki_root
            target_alt = (wiki_root / link.lstrip("/")).resolve()
            if target_alt.exists():
                continue

            # Try 3: Relative to workspace root (e.g. link to raw/ or docs)
            target_repo = (wiki_root.parent / link.lstrip("/")).resolve()
            if target_repo.exists():
                continue

            errors.append(f"[{rel_posix}] Broken link target: '{link}'.")

        # Validate orphan status (must be referenced in index.md)
        if filename not in SPECIAL_ROOT_FILES:
            if rel_posix not in index_content and filename not in index_content:
                warnings.append(f"[{rel_posix}] Orphan page: not referenced in wiki/index.md.")

    print(f"=== AI Wiki Lint Report ({len(all_files)} markdown pages scanned) ===")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for err in errors:
            print(f"  ✖ {err}")
        return 1

    print("\n✓ Wiki integrity check passed without errors.")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "wiki"
    wiki_path = Path(target).resolve()
    if not wiki_path.is_dir():
        print(f"Error: Target path '{wiki_path}' is not a directory.")
        sys.exit(1)
    sys.exit(lint_wiki(wiki_path))
