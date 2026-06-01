---
module: inventory-whole-arcanum
task: TASK-WAI-002
status: completed
layer: L1
---

# TASK-WAI-002: Inventory Self-Slice

## Objective

Use Inventory itself as the first proof slice so the package proves its own
query, lint, schema, and handoff contracts before broad rollout.

## Implementation Detail

Create cards for the Inventory package that answer agent implementation
questions:

- what evidence-card fields are required,
- how candidate EvidenceSets are shaped,
- how fixture validation works,
- where downstream authority boundaries sit,
- what remains deferred.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-WAI-003 | Create slice-aware validation contract and Inventory self-slice cards. | `cards/inventory/`, validator wrapper/contract path under whole-Arcanum pack or Inventory scripts | slice validator accepts conventional files and cards cover schema, validator, retrieval, boundaries | slice-aware validator plus fixture validator |
| SWU-WAI-004 | Create self-slice EvidenceSet and query example. | `evidence-sets/` | selected/excluded cards explain a real query | candidate set reference checks |

## Completion Evidence

| SWU | Result | Evidence |
| --- | --- | --- |
| SWU-WAI-003 | pass | `arcana/inventory/scripts/validate-evidence-card-slice.sh` validates conventional slice files; Inventory self-slice cards, index, and retrieval fixture exist. |
| SWU-WAI-004 | pass | `evidence-sets/evidence-sets.json` contains a candidate EvidenceSet that references only self-slice card IDs. |

## Source Anchors

- `arcana/inventory/README.md`
- `arcana/inventory/SKILL.md`
- `arcana/inventory/templates/evidence-card.schema.yml`
- `arcana/inventory/templates/evidence-set.schema.yml`
- `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`

## Decision Inputs

- `decisions/W1-VALIDATION-SHAPE-DECISION.md`: selected option B,
  slice-aware validator contract.

## SWU-WAI-003 Execution Notes

- Use conventional slice filenames: `cards.json`, `index.json`,
  `retrieval.json`, and optional `evidence-sets.json`.
- The validation wrapper may adapt these files to the existing validator or add
  equivalent `jq` checks directly.
- Minimum Inventory self-slice cards:
  - evidence-card schema contract,
  - validator runtime,
  - retrieval/index behavior,
  - downstream authority boundary.

## Result

See `arcana/inventory/development/whole-arcanum/task-session/TASK-WAI-002-RESULT.md`.
