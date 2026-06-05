# Branch-Aware Ontology Schema Validation Plan

Status: published candidate bundle
Date: 2026-06-01
Owner: Ontology Vault development

## Purpose

Provide the current published candidate bundle for the branch-aware ontology schema validation surface.

This package now contains the validated development schema, fixtures, validators, JSON Schema candidate, promotion-boundary decisions, and candidate-bundle index. It remains non-canonical as a full schema/template package: publication here means future ontology sessions may cite the bundle as candidate evidence, not that canonical templates or external systems must adopt it.

The exception is the PromotionRecord record-kind boundary. `record_kind: promotion_record` is now canonical as the Ontology Vault governance decision shape for owner-routed promotion decisions. Companion templates, separate schemas, and external-system adoption remain gated.

## Source Design References

- `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`
- `../invoke-runs/20260527T011500Z-schema-axis-design.md`
- `../general-ontology-lifecycle/refinement-runs/20260527T010000Z-role-lifecycle-redundancy/RESULT.md`
- `../cyberalchemy-ontology-lifecycle/ONTOLOGY-VAULT-BRIEF.md`
- `../cyberalchemy-ontology-lifecycle/WORK-PACK.md`

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `GOVERNED-CANDIDATE-BUNDLE.md` | Stable published-candidate index and boundary contract. |
| `IMPLEMENTATION-LAYERING.md` | L0-L3 validation layers and promotion evidence. |
| `WORK-PACK.md` | Executable test-first planning contract with tasks and SWUs. |
| `PLAN-TRANSPORT.md` | Invoke plan provenance and next-route summary. |
| `VALIDATION-REPORT.md` | Passing validation report for fixtures and JSON Schema candidate. |
| `decision-gates/OVS-GATE-001-promotion-boundary.md` | Passed promotion-boundary decision selecting the governed candidate bundle. |
| `decision-gates/OVS-GATE-002-promotion-record-companion-boundary.md` | Passed PromotionRecord boundary decision selecting canonical record-kind semantics while deferring templates and separate schemas. |
| `schema/branch-aware-ontology-candidate.schema.yml` | Development JSON Schema candidate. |
| `fixtures/` | Valid and invalid fixture corpus. |
| `tests/` | Development validators for fixture and JSON Schema behavior. |

## Boundary

This bundle must not mutate:

- Inventory,
- structured-action-schema,
- canonical Ontology Vault templates,
- canonical branch conventions.

Canonical template promotion, DomainSpec adoption, CyberAlchemy source mutation, and future-system obligations require later owner-scoped gates.
