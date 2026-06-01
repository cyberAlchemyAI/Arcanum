---
module: inventory-evidence-card
version: current
status: draft
updatedAt: 2026-05-26
docType: implementation-layering
---

# Implementation Layering: Inventory Evidence-Card

## Purpose

Define a decision-first layer model for moving the development package into production Inventory artifacts.

## Target And Scope

- Target: `arcana/inventory/`
- Scope: sigil capability development
- Current state: design package refreshed; production mutation pending

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the evidence-card contract is coherent as static markdown templates. | Schema, authoring, and lint templates. | Target template files and schema references. | Runtime validator, pilot fixtures. | Template review passes. | Continue to fixtures. |
| L1 | After this layer, we know whether cards can be indexed and retrieved in task-shaped form. | Index/retrieval contract and pilot card fixture. | Index template, pilot cards, retrieval fixture. | Production ingest. | Pilot JSON and manual checks pass. | Continue to handoff examples. |
| L2 | After this layer, we know whether downstream handoff boundaries remain clean. | Ontology/Definitions packet examples and docs updates. | Handoff fixtures, README/SKILL updates. | Downstream promotion. | Non-authority checks pass. | Continue to readiness. |
| L3 | After this layer, we know whether runtime hardening should start. | Readiness review and gap ledger. | Glossary candidates, validation report. | CLI integration until approved. | Acceptance criteria checked. | Start validator or defer. |

## Non Regression Guardrails

- Do not remove existing page-based Inventory behavior.
- Do not mutate CyberAlchemy sources.
- Do not promote candidate glossary or ontology material.
- Do not implement runtime validator before static lint contract and fixtures exist.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the static evidence-card contract is ready to become production templates.
- Major deferred scope: executable validator and command integration.
