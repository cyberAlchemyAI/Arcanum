---
module: inventory-whole-arcanum
task: TASK-WAI-001
swus:
  - SWU-WAI-001
  - SWU-WAI-002
status: context-built
updatedAt: 2026-05-29
docType: task-session-context
---

# Context Pack: TASK-WAI-001

## Task

Create the source manifest and exclusion policy for the whole-Arcanum inventory.

## Selected Context

| Source | Selector | Obligation |
| --- | --- | --- |
| `arcana/inventory/development/whole-arcanum/WORK-PACK.md` | Control fields, SWU Manifest, Blockers And Gates | Select next ready unit, respect write scopes, keep EvidenceSets candidate-only. |
| `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-001-source-manifest.md` | Objective, Implementation Detail, Smallest Working Units | Create `source-manifest.*` first, then `SOURCE-POLICY.md`; classify source, durable evidence, generated, local runtime, and temporary surfaces. |
| `arcana/inventory/development/whole-arcanum/EXECUTION-PACK.md` | First Task-Session Handoff, Validation Spine | Stop if classification cannot distinguish source from generated state; run constitution and inventory validation. |
| `framework/ARTIFACT-CONSTITUTION.md` | Classes, Rules, Validation Contract | Source artifacts are versioned by default; generated/local runtime artifacts are excluded unless promoted as durable evidence. |
| `framework/SCHEMA-CONSTITUTION.md` | Rules and Validation | New machine-readable schemas must be `.schema.yml`; this task must not create a schema artifact. |

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Source families and initial selectors must exist. | covered |
| O2 | Generated/local runtime paths must not become source inventory scope. | covered |
| O3 | Durable evidence inclusion must require an explicit promotion reason. | covered |
| O4 | Validation must include manifest grep checks and artifact constitution checks. | covered |
| O5 | Completion evidence must synchronize the work-pack and task-session result. | covered |

## Execution Constraints

- Use tracked-file discovery as the primary source baseline.
- Prefer family selectors over individual-file microlists.
- Do not generate evidence cards in this task.
- Do not promote EvidenceSet status.
- Keep shell plus `jq` as the agent-runtime assumption.

## Gate Verdict

Strict coverage passes for local execution. No runtime handoff pack is needed.
