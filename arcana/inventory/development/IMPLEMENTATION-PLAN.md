---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: implementation-plan
---

# Implementation Plan: Inventory Interface, Linking, And Indexing

## Invoke Result

- Mode: refresh
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `../../../spells/invoke/refresh.md`
- Outputs: `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`
- Mutation mode: apply-approved
- Next route: task-session

## Objective

Implement the Inventory interface and index/link substrate before any further
whole-repository or whole-Arcanum inventorization.

The implementation target is:

```text
$inventory -> infer target -> confirm -> inventorize bounded slice -> update JSON + Markdown package
```

## Active Inputs

| Input | Role |
| --- | --- |
| `INTERFACE-ARCHITECTURE.md` | interface contract and mode model |
| `INDEX-TECHNIQUE-RESEARCH.md` | index technique backlog |
| `LINKING-DISCIPLINE.md` | link rules, edge vocabulary, source refs |
| `INTERFACE-REFINE-SYNTHESIS.md` | refined next work units |
| `arcana/inventory/SKILL.md` | production skill contract to update |
| `arcana/inventory/templates/` | production template target |
| `arcana/inventory/scripts/` | validator target |

Archived research inputs:

- `archive/domainspec-core-research-20260605/`
- `archive/whole-arcanum-research-20260605/`

Use archived research only as evidence. Do not continue those package roots as
active development tracks.

## Delivery Slices

| Slice | Goal | Dependencies | Exit Condition |
| --- | --- | --- | --- |
| S1 | Add default Inventory interface contract. | architecture refs | `SKILL.md` documents auto/confirmation/status behavior. |
| S2 | Add JSON index schema/template pack. | S1 | selector/link/backlink/traceability/gap/query/projection templates exist. |
| S3 | Add validation for index/link discipline. | S2 | validator checks controlled edges, source refs, missing card refs, and non-authority notices. |
| S4 | Exercise first interface slice. | S1-S3 | one pilot slice proves target proposal, cards, indexes, retrieval, and coverage. |
| S5 | Refresh docs/readiness. | S1-S4 | README/READINESS/WORK-PACK reflect interface MVP state. |

## Task Decomposition

| Task ID | Description | Layer | Complexity | Depends On |
| --- | --- | --- | --- | --- |
| TASK-INT-001 | Update Inventory skill/README with default auto interface and confirmation flow. | L0 | medium | none |
| TASK-INT-002 | Add target proposal and interface view templates. | L0 | medium | TASK-INT-001 |
| TASK-INT-003 | Add selector/link/backlink/traceability/gap/query/projection index templates. | L1 | medium | TASK-INT-001 |
| TASK-INT-004 | Extend validator for link/index discipline. | L2 | medium | TASK-INT-003 |
| TASK-INT-005 | Create first interface-driven pilot slice. | L2 | medium | TASK-INT-001..004 |
| TASK-INT-006 | Sync readiness, docs, and next-route handoff. | L3 | low | TASK-INT-005 |

## Validation Strategy

| Validation Type | Target | Method |
| --- | --- | --- |
| Skill contract | `arcana/inventory/SKILL.md` | `rg "auto|confirmation|target inference|status|explain"` |
| Template presence | `arcana/inventory/templates/` | required template files exist |
| JSON parse | index examples and pilot slice JSON | `jq empty` |
| Source refs | selector/link/card refs | validator checks path/card existence |
| Edge vocabulary | `link-index.json` | validator rejects unknown edges |
| Non-authority language | relation-like links and handoffs | validator/manual review |
| Interface proof | first pilot slice | target proposal + slice outputs + coverage |

## Layering

| Layer | Purpose | Completion Evidence |
| --- | --- | --- |
| L0 interface contract | user-facing behavior is explicit | SKILL/README/template updates |
| L1 index substrate | JSON shapes exist | templates and examples parse |
| L2 validation and pilot | links/indexes are enforceable | validator and pilot slice pass |
| L3 package readiness | pack tells the next user what is active | readiness/work-pack/refresh report synced |

## Non-Goals

- no whole-repository ingest,
- no whole-Arcanum continuation,
- no database requirement,
- no vector search,
- no full browser UI,
- no ontology or definition promotion.

## Handoff

Use `WORK-PACK.md` as the current execution manifest. Execute one task at a
time through `task-session`.
