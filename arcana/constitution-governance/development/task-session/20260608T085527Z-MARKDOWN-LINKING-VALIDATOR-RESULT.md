---
artifact_id: constitution-governance.task-session.markdown-linking-validator.result
artifact_type: validation-report
intent: Record task-session result for Markdown linking validator hardening.
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

# Task Session Result: Markdown Linking Validator Hardening

## Task

Harden validator coverage for the candidate Markdown Linking Constitution.

## Result

PASS for the bounded task.

The repository-wide artifact validator remains FLAG because unrelated dirty or
existing generated/schema state fails outside this task scope.

## Decisions

| Decision | Classification | Selection |
| --- | --- | --- |
| Whether to promote the constitution | blocker for promotion, not for this task | Deferred; no promotion attempted. |
| Whether to scan all Markdown files | blocker for migration, not for this task | Deferred; adapter validates the constitution and fixtures only. |
| Whether to add typed-edge semantic validation | deferrable | Deferred to a future Markdown linking profile or capability-specific adapter. |

## Context Pack

[20260608T085527Z-MARKDOWN-LINKING-VALIDATOR-CONTEXT.md](20260608T085527Z-MARKDOWN-LINKING-VALIDATOR-CONTEXT.md)

Strict coverage: pass.

## Changes

| File | Change |
| --- | --- |
| [Artifact Validator](../../../../tools/validate-artifact-constitution.sh) | Added Markdown Linking Constitution and link-checker existence checks. |
| [Artifact Validator](../../../../tools/validate-artifact-constitution.sh) | Added targeted validation that the Markdown Linking Constitution's own local links and anchors resolve. |
| [Artifact Validator](../../../../tools/validate-artifact-constitution.sh) | Added passing and failing Markdown link fixtures to `--self-test`. |

## Validation

| Command | Result |
| --- | --- |
| `bash -n tools/validate-artifact-constitution.sh` | pass |
| `bash -n tools/check_markdown_links.sh` | pass |
| `tools/validate-artifact-constitution.sh --self-test` | pass |
| `bash tools/check_markdown_links.sh framework/MARKDOWN-LINKING-CONSTITUTION.md --check-anchors` | pass |
| `bash tools/check_markdown_links.sh framework/ARTIFACT-CONSTITUTION.md --check-anchors` | pass |
| `tools/validate-artifact-constitution.sh` | flag: unrelated `.claude/skills/dispatch-spec/dispatch.schema.json` violates `.schema.yml` rule; generated artifact warnings also remain. |

## Synchronized Evidence

- [Context pack](20260608T085527Z-MARKDOWN-LINKING-VALIDATOR-CONTEXT.md)
- [This result](20260608T085527Z-MARKDOWN-LINKING-VALIDATOR-RESULT.md)

## Follow-Up

1. Decide whether the Markdown Linking Constitution should remain candidate or
   enter a promotion/backfill task.
2. Design a future edge-table adapter if relation-like claims need deterministic
   enforcement beyond local link resolution.
3. Handle unrelated schema-format blocker separately:
   `.claude/skills/dispatch-spec/dispatch.schema.json`.
