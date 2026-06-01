---
module: inventory-evidence-card
version: current
status: draft
updatedAt: 2026-05-26
docType: observability
---

# Observability: Inventory Evidence-Card

## Signal Inventory

| Signal Family | Purpose | Source Contract |
| --- | --- | --- |
| Template integrity | Detect missing or drifted template fields. | `TEMPLATE-MANIFEST.md`, `CONCEPT-MODEL.md` |
| Fixture validity | Track pilot parse and schema review status. | `IMPLEMENTATION-PLAN.md` |
| Authority boundary | Detect false promotion or downstream ownership confusion. | `FLOWS-POLICIES.md`, `INTERFACES.md` |
| Execution readiness | Track task/SWU completion and blocker age. | `WORK-PACK.md`, `EXECUTION-PACK.md` |

## Signals

| Signal | Instrument Type | Attributes | Alert Rule |
| --- | --- | --- | --- |
| inventory.template.missing_field | Counter | template, field | Any increment blocks readiness. |
| inventory.fixture.parse_failure | Counter | fixture, error | Any increment blocks fixture promotion. |
| inventory.authority_boundary.violation | Counter | artifact, rule | Any increment requires review. |
| inventory.workpack.blocker_age | Gauge | blocker_id | Review when blocker persists across sessions. |

## Traceability Rules

1. Every readiness claim must cite an artifact path.
2. Every fixture failure must link to the fixture and rule.
3. Every authority-boundary finding must name the downstream owner.
