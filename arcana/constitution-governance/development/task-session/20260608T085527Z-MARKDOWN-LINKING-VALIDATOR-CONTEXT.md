---
artifact_id: constitution-governance.task-session.markdown-linking-validator.context
artifact_type: context-pack
intent: Lean context pack for hardening Markdown linking constitution validation.
owner: constitution-governance
lifecycle_status: candidate
constitution_selectors:
  - framework.artifact
  - framework.artifact-metadata
  - framework.markdown-linking
validation_profile:
  - markdown-linking
  - artifact-constitution
---

# Context Pack: Markdown Linking Validator Hardening

## Task

Harden the validator coverage for the candidate Markdown Linking Constitution
without promoting the constitution or forcing a legacy Markdown migration.

## Mode

lean

## Obligations

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O1 | Keep the task bounded to Markdown linking validation. | covered | [Markdown Linking Constitution](../../../../framework/MARKDOWN-LINKING-CONSTITUTION.md) |
| O2 | Preserve candidate status and avoid canonical promotion decisions. | covered | [Markdown Linking Constitution](../../../../framework/MARKDOWN-LINKING-CONSTITUTION.md#promotion-boundary) |
| O3 | Provide deterministic validation for local Markdown links. | covered | [Markdown Link Checker](../../../../tools/check_markdown_links.sh) |
| O4 | Wire the deterministic check into artifact constitution validation without scanning the whole dirty Markdown worktree. | covered | [Artifact Validator](../../../../tools/validate-artifact-constitution.sh) |
| O5 | Validate with passing and failing fixtures. | covered | [Artifact Validator Self-Test](../../../../tools/validate-artifact-constitution.sh) |

## Selected Context

| Source | Selectors | Why Included |
| --- | --- | --- |
| [Markdown Linking Constitution](../../../../framework/MARKDOWN-LINKING-CONSTITUTION.md) | Rules, Validation, Promotion Boundary | Defines candidate rules and explicitly blocks canonical promotion until validator coverage and adoption evidence exist. |
| [Markdown Link Checker](../../../../tools/check_markdown_links.sh) | whole helper | Existing deterministic helper for local file and optional anchor validation. |
| [Artifact Validator](../../../../tools/validate-artifact-constitution.sh) | constitution path checks, self-test, validation loop | Existing validation surface that already owns framework constitution existence checks and self-test fixtures. |
| [Inventory Linking Discipline](../../../inventory/development/LINKING-DISCIPLINE.md) | Link Validation Rules | Evidence for narrower future Inventory edge/index validation, not framework authority. |

## Gate Checks

| Gate | Verdict | Note |
| --- | --- | --- |
| Dependencies | pass | Constitution and helper exist in `HEAD`. |
| Write scope | pass | Limit edits to `tools/validate-artifact-constitution.sh` and task-session evidence. |
| Promotion decision | n/a | No promotion attempted. |
| Legacy migration | n/a | No repository-wide Markdown scan added. |
| Validation path | pass | Syntax, targeted link checks, self-test, and full validator attempted. |

## Constraints

- Do not turn candidate edge vocabulary into canonical ontology authority.
- Do not fail all existing Markdown files until a migration/backfill decision is made.
- Keep full worktree validator failures attributable when unrelated dirty state exists.

## Validation Surface

```bash
bash -n tools/validate-artifact-constitution.sh
bash -n tools/check_markdown_links.sh
tools/validate-artifact-constitution.sh --self-test
bash tools/check_markdown_links.sh framework/MARKDOWN-LINKING-CONSTITUTION.md --check-anchors
bash tools/check_markdown_links.sh framework/ARTIFACT-CONSTITUTION.md --check-anchors
tools/validate-artifact-constitution.sh
```

## Strict Coverage

pass

## Blockers

None for the bounded validator-hardening task.
