---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: implementation-layering
---

# Implementation Layering: Inventory Interface, Linking, And Indexing

## Purpose

Define the minimum implementation layers for turning Inventory into a usable
chat-first interface backed by JSON indexes and Markdown records.

## Target And Scope

- Target: `arcana/inventory/`
- Scope: Inventory skill contract, templates, validators, and first pilot slice
- Current state: design package refreshed; production mutation starts at
  `SWU-INT-001`

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Can `$inventory` infer a target and ask for confirmation before mutation? | SKILL/README auto interface contract plus target proposal template. | `auto`, `inventorize`, `status`, `continue`, `explain`; confirmation proposal. | Actual pilot slice execution. | Contract grep and template review pass. | Continue to index substrate. |
| L1 | Can Inventory represent lookup structure with JSON indexes and Markdown records? | Selector/link/backlink/traceability/gap/query/projection templates. | JSON index templates and examples. | Validator enforcement, projections. | `jq empty` examples and controlled vocabulary review. | Continue to validation. |
| L2 | Can index/link discipline be validated and exercised on one bounded slice? | Validator extension and first pilot slice. | edge vocabulary checks, source/card refs, non-authority notices, pilot `cards/index/retrieval/COVERAGE`. | Whole-repo ingest, database, vector index. | Validator and pilot slice pass. | Continue to readiness sync. |
| L3 | Is the interface MVP ready for repeated use? | Readiness/docs sync and next-route handoff. | README, readiness, work-pack, refresh report. | Full UI and broad inventorization. | Readiness states what works and what remains blocked. | Continue to broader inventorization only after interface proof. |

## Non-Regression Guardrails

- Do not remove existing evidence-card behavior.
- Do not continue archived whole-Arcanum or whole-repo tracks as active work.
- Do not write inside nested submodules for the interface MVP.
- Do not promote tags into canonical definitions.
- Do not promote Inventory links into ontology relations.
- Do not build a database/vector/full UI before JSON + Markdown behavior works.

## Recommended Next Layer

- Next layer: L0.
- First unit: `SWU-INT-001`.
- Key decision unlocked: whether `$inventory` has a clear default interface
  contract.
