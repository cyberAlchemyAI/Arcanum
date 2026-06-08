---
module: inventory-whole-arcanum
task: TASK-WAI-002
swu: SWU-WAI-003
status: context-built
updatedAt: 2026-05-29
docType: task-session-context
---

# Context Pack: SWU-WAI-003

## Task

Create a slice-aware validation contract and Inventory self-slice cards.

## Selected Context

| Source | Selector | Obligation |
| --- | --- | --- |
| `arcana/inventory/development/whole-arcanum/WORK-PACK.md` | SWU row and W1 validation gate | Execute `SWU-WAI-003`; use option B and keep write scope to `cards/inventory/` plus validator wrapper/contract path. |
| `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-002-inventory-self-slice.md` | SWU-WAI-003 notes | Use `cards.json`, `index.json`, `retrieval.json`; create at least four proof cards. |
| `arcana/inventory/development/whole-arcanum/decisions/W1-VALIDATION-SHAPE-DECISION.md` | selected option B | Add slice-aware validation rather than pilot-compatible filenames. |
| `arcana/inventory/templates/evidence-card.schema.yml` | required/properties/allOf | Cards must satisfy schema fields and full-card trace/handoff requirements. |
| `arcana/inventory/development/VALIDATOR-RUNTIME.md` | selected surface and validator scope | Keep validation shell plus `jq`; human UI remains deferred. |
| `arcana/inventory/templates/index.md` | index and retrieval output | Retrieval should select cards, preserve exclusions, and avoid full dumps. |
| `arcana/inventory/README.md` and `arcana/inventory/SKILL.md` | evidence-card, EvidenceSet, lookup, and authority sections | Cards remain candidate/read-model evidence, not downstream authority. |

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Add or wrap a slice-aware validator for conventional slice files. | covered |
| O2 | Create Inventory self-slice cards in `cards/inventory/cards.json`. | covered |
| O3 | Include at least schema, validator, retrieval/index, and authority-boundary cards. | covered |
| O4 | Validate cards through slice-aware validator and existing pilot fixture validator. | covered |
| O5 | Preserve EvidenceSet promotion and human UI deferrals. | covered |

## Gate Verdict

Strict coverage passes for local execution. No runtime handoff pack is required.
