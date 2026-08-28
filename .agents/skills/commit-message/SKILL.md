---
name: commit-message
description: Checklist for splitting changes into commit groups and writing commit messages — use at commit time
---

# Commit Message Skill

## Grouping (before writing any message)

When the pending changes span more than one logical concern, split them
into **commit groups** — one commit per group. A single commit is fine
when the changeset is genuinely one concern.

1. **Choose one grouping rule** for the whole changeset. The agent
   decides which rule fits; common rules (not exhaustive):
   - *By concern* — each independent fix/feature/refactor is a group
   - *By layer* — e.g. domain logic vs. interface vs. infrastructure
   - *By feature/folder* — when changes touch unrelated features
   - *Mechanical vs. behavioral* — renames/formatting apart from logic changes
2. **Explain to the user, before committing:**
   - The groups (which files/changes land in each)
   - Which rule was chosen to form them
   - Why that rule fits this changeset better than the alternatives
3. **Then write one standard commit message per group**, following the
   rest of this checklist (prefix, subject, body, files, tests, ref).

A group must be self-contained: it should build and make sense on its
own, without depending on changes left in a later group.

## Prefix (required)

Pick exactly one: `fix:` | `feat:` | `refactor:`

## Subject (required)

- Imperative mood ("add", "remove", "strip" — not "added", "removes")
- Max 72 characters (prefix included)
- No trailing period
- Right abstraction level — not too vague, not too granular

## Body (required for non-trivial commits)

Blank line after subject. Answer:
- **What** changed — concrete description
- **Why** — motivation or problem solved
- **Impact** — quantify when possible ("~80% smaller payload", "eliminates N+1")

Wrap at 72 characters.

## Files (include when 2+ code files changed)

List production code only. No tests, docs, or config.
Mark each `(created)` or `(modified)`. Relative paths from repo root.

```
Files:
- domains/aquisicao/interfaces/views.py (modified)
- frontend/src/pages/contratos-tabs/BulkImportTab.jsx (modified)
```

## Tests (include when test suite changed)

Summarize what was validated, added, or removed. Focus on *what*, not file paths.

```
Tests:
- Added negative assertions confirming stripped fields are absent
- Deleted test_document_includes_ocr_text_field
```

## Ref (only when the commit directly implements a planned item)

Include only when the work was explicitly described in a spec, discovery, or backlog item **and** you can point to the specific section. Do not add a Ref for standalone fixes, ad-hoc improvements, or work that wasn't pre-planned.

Relative path, optional `§Section` anchor.

```
Ref: specs/refactor/docs/frontend-page-load/page-load-discovery.md §Fix 1
```
