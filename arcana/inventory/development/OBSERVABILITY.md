---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: observability
---

# Observability: Inventory Interface, Linking, And Indexing

## Purpose

Track whether the new Inventory interface and index/link substrate help agents
inventorize safely and reuse context faster.

## Recommended Signals

| Signal | Meaning |
| --- | --- |
| `inventory.auto.started` | `$inventory` default interface started. |
| `inventory.target.inferred` | target/action inferred from prompt. |
| `inventory.confirmation.shown` | mutation proposal shown to user. |
| `inventory.confirmation.approved` | user approved bounded mutation. |
| `inventory.confirmation.rejected` | user rejected or changed target. |
| `inventory.slice.created` | bounded slice created. |
| `inventory.index.updated` | JSON index updated. |
| `inventory.link.validation.failed` | link/index validation failed. |
| `inventory.lookup.used` | lookup/status/explain used Inventory indexes. |
| `inventory.gap.opened` | gap/risk queue row opened. |

## Metrics

| Metric | Use |
| --- | --- |
| target inference confidence | identify vague prompts that need better questions |
| confirmation rejection rate | detect bad inference or unsafe proposals |
| source anchors per slice | prevent broad ingestion |
| selected vs excluded cards | measure retrieval precision |
| validation failures by class | harden templates and validator |
| gaps opened/closed | track operational residue |

## MVP Requirement

The first pilot slice should record:

- target proposal,
- approval state,
- source anchor count,
- cards created,
- indexes updated,
- validation result,
- gaps opened,
- next route.
