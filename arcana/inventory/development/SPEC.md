---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: spec
---

# SPEC: Inventory Interface, Linking, And Indexing

## Objective

Inventory must provide a clear user-facing interface for inventorization:

```text
$inventory
  -> infer what the user wants inventorized
  -> ask for confirmation
  -> inventorize a bounded target
  -> update JSON indexes and Markdown records
  -> make the result reusable through lookup/status/explain views
```

## Scope

This spec covers the active development track for:

- default/no-mode `$inventory` behavior,
- target inference,
- confirmation proposals,
- JSON index templates,
- Markdown coverage/explanation records,
- DomainSpec-style linking discipline,
- link/index validation,
- one interface-driven pilot slice.

This spec does not cover:

- whole-repository ingest,
- whole-Arcanum continuation,
- database or vector search implementation,
- human web UI,
- ontology relation promotion,
- canonical definition promotion.

## Core Concepts

| Concept | Meaning |
| --- | --- |
| Inventory interface | Chat-first layer that translates user intent into safe Inventory actions. |
| Target inference | Classification of the requested source/scope/action before mutation. |
| Confirmation proposal | Human-readable proposal that names target, sources, outputs, exclusions, and non-goals. |
| Bounded slice | Small inventorization unit with source anchors and retrieval question. |
| JSON index | Machine-readable lookup structure owned by Inventory. |
| Markdown record | Human-readable explanation, coverage report, or handoff. |
| Selector index | Source-selector-to-card lookup. |
| Link index | Typed read-model links among sources, cards, records, and owners. |
| Backlink index | Generated reverse lookup derived from link index. |
| Gap/risk queue | Operational residue and next-owner list. |

## Required Behavior

1. `$inventory` defaults to `auto`.
2. `auto` infers action and target from prompt/session context.
3. Any mutation requires a confirmation proposal.
4. Technical modes remain available as internal routes.
5. JSON indexes and Markdown records are both updated by successful slice runs.
6. Links and tags remain Inventory read models, not downstream authority.
7. Lookup/status/explain views expose selected evidence, exclusions, gaps, and
   next owners.

## Acceptance Criteria

| ID | Criterion | Evidence |
| --- | --- | --- |
| AC-001 | Default interface contract documented. | `arcana/inventory/SKILL.md`, `README.md` |
| AC-002 | Confirmation proposal template exists. | `arcana/inventory/templates/target-confirmation.md` |
| AC-003 | Target inference template exists. | `arcana/inventory/templates/target-inference.json` |
| AC-004 | Index templates exist and parse. | `arcana/inventory/templates/*index*.json` |
| AC-005 | Link validation rejects unsafe relations. | validator output |
| AC-006 | First pilot slice proves the interface. | `development/pilot/interface-link-index/` |

## Active Plan

Use:

- `ARCHITECTURE.md`
- `IMPLEMENTATION-LAYERING.md`
- `IMPLEMENTATION-PLAN.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `READINESS.md`
