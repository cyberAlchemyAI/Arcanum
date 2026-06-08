---
module: inventory-whole-arcanum
task: TASK-WAI-003
swu: SWU-WAI-007
status: context-built
updatedAt: 2026-06-01
docType: task-session-context
---

# Context Pack: SWU-WAI-007

## Task

Create the cross-pilot EvidenceSet that answers whether a planned Inventory SWU
can execute directly or needs a decision gate first.

## Selected Context

| Source | Selector | Obligation |
| --- | --- | --- |
| `TASK-WAI-003-governance-lifecycle-slices.md` | SWU-WAI-007 row | Create candidate set after governance and lifecycle cards exist. |
| `cards/governance/cards.json` | governance cards | Include Artifact Constitution and Schema Constitution cards. |
| `cards/lifecycle/cards.json` | lifecycle cards | Include Invoke, Refine, and Task Session cards. |
| `cards/inventory/cards.json` | self-slice cards | Exclude retrieval/index card as non-decisive for gate routing. |
| `arcana/inventory/templates/evidence-set.schema.yml` | required/properties | Candidate EvidenceSet must reference card IDs and preserve candidate status. |

## Gate Verdict

Strict coverage passes for local execution.
