---
module: inventory-whole-arcanum
task: TASK-WAI-001
status: completed
layer: L0
---

# TASK-WAI-001: Source Manifest And Exclusion Policy

## Objective

Create the boundary artifact that decides what the whole-Arcanum inventory may
read, summarize, index, and ignore.

## Implementation Detail

Build a manifest from repository file discovery, then classify paths into:

- source artifacts,
- candidate durable evidence,
- generated artifacts,
- local runtime artifacts,
- excluded third-party or temporary surfaces.

The manifest should prefer source-family selectors over individual-file microlists
where the family is governed by the same artifact constitution rule.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-WAI-001 | Draft source manifest and family classification. | `source-manifest.*` | source families and initial selectors exist | `rg -n "arcana|spells|transmutations|formulae|framework|registry|tools" source-manifest.*` |
| SWU-WAI-002 | Add exclusion and durable-evidence policy. | `SOURCE-POLICY.md` | generated/runtime exclusions and durable promotion rule exist | `rg -n "generated|local runtime|durable evidence|exclude" SOURCE-POLICY.md` |

## Completion Evidence

| SWU | Result | Evidence |
| --- | --- | --- |
| SWU-WAI-001 | pass | `source-manifest.json` exists, parses with `jq`, and includes required source families. |
| SWU-WAI-002 | pass | `SOURCE-POLICY.md` exists and defines generated/local runtime exclusions plus durable evidence promotion rules. |

## Source Anchors

- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/SCHEMA-CONSTITUTION.md`
- `arcana/inventory/development/WORK-PACK.md`

## Expected Result Shape

```yaml
swu_id: SWU-WAI-001
result: pass | flag | block
files_touched:
  - arcana/inventory/development/whole-arcanum/source-manifest.*
validation:
  - command and result
blockers:
  - blocker or none
handoff_note: next SWU or policy issue
```

## Result

See `arcana/inventory/development/whole-arcanum/task-session/TASK-WAI-001-RESULT.md`.
