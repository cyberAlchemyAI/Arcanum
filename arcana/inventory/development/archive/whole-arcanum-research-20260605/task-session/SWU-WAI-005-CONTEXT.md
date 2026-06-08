---
module: inventory-whole-arcanum
task: TASK-WAI-003
swu: SWU-WAI-005
status: context-built
updatedAt: 2026-06-01
docType: task-session-context
---

# Context Pack: SWU-WAI-005

## Task

Create governance evidence cards for Artifact Constitution and Schema
Constitution.

## Selected Context

| Source | Selector | Obligation |
| --- | --- | --- |
| `WORK-PACK.md` | SWU-WAI-005 row | Write governance cards under `cards/governance/`. |
| `TASK-WAI-003-governance-lifecycle-slices.md` | Execution assumptions | Create at least Artifact Constitution and Schema Constitution cards. |
| `framework/ARTIFACT-CONSTITUTION.md` | Classes, rules, validation contract | Capture artifact class and generated/local runtime boundaries. |
| `framework/SCHEMA-CONSTITUTION.md` | Purpose, scope, rules, promotion boundary | Capture `.schema.yml` rule and schema validation boundary. |

## Gate Verdict

Strict coverage passes for local execution.
