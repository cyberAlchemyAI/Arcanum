---
module: inventory-whole-arcanum
task: TASK-WAI-002
swu: SWU-WAI-004
status: context-built
updatedAt: 2026-05-29
docType: task-session-context
---

# Context Pack: SWU-WAI-004

## Task

Create the self-slice EvidenceSet and query example for the Inventory proof
slice.

## Selected Context

| Source | Selector | Obligation |
| --- | --- | --- |
| `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-002-inventory-self-slice.md` | SWU-WAI-004 row | Create a self-slice EvidenceSet and query example after `SWU-WAI-003`. |
| `arcana/inventory/development/whole-arcanum/cards/inventory/cards.json` | four self-slice cards | EvidenceSet must reference existing cards only. |
| `arcana/inventory/templates/evidence-set.schema.yml` | required/properties | Candidate set must include card refs, excluded refs, index terms, handoff target, synthesis note, residue, status, owner, and update date. |
| `arcana/inventory/README.md` | EvidenceSet Candidate Layer | EvidenceSet remains candidate-level and does not replace Context Builder packs or downstream authority. |

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Store a candidate EvidenceSet under `whole-arcanum/evidence-sets/`. | covered |
| O2 | Reference only existing self-slice card IDs. | covered |
| O3 | Include query/purpose and index terms for shell plus `jq` lookup. | covered |
| O4 | Preserve candidate status and promotion owner boundary. | covered |

## Gate Verdict

Strict coverage passes for local execution. No runtime handoff pack is required.
