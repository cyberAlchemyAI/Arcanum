# EvidenceSet Schema

Schema Artifact Role: schema-template

Canonical machine-readable schema: `evidence-set.schema.yml`

## Purpose

Define the candidate Inventory `EvidenceSet` contract.

An EvidenceSet is a stable, task-scoped grouping of evidence-card IDs with inclusion reasons, exclusion reasons, index terms, handoff intent, synthesis note, residue, status, and promotion owner.

EvidenceSets make repeated agent retrieval and downstream handoff assembly faster and more explainable. They do not own source evidence, duplicate evidence-card content, promote ontology relations, define canonical terms, replace Context Builder packs, or provide a human UI workflow.

## YAML Shape

```yaml
schema_version: inventory.evidence-set.v0.1
set_id: evidence-set.<stable-slug>
purpose: string
card_refs:
  - id: inventory.card.<stable-slug>
    inclusion_reason: string
excluded_card_refs:
  - id: inventory.card.<stable-slug>
    reason: string
index_terms: [string]
handoff_target: context-builder | ontology-vault | definitions-governance | invoke | repository-harness | other
synthesis_note: string
residue: string
status: candidate | promote-pending | rejected | superseded
promotion_owner: inventory | ontology-vault | definitions-governance | context-builder | invoke | repository-harness | other
updated_at: YYYY-MM-DD
```

## Required Fields

Every EvidenceSet requires:

- `schema_version`
- `set_id`
- `purpose`
- `card_refs`
- `excluded_card_refs`
- `index_terms`
- `handoff_target`
- `synthesis_note`
- `residue`
- `status`
- `promotion_owner`
- `updated_at`

## Controlled Vocabularies

`schema_version`: `inventory.evidence-set.v0.1`.

`status`: `candidate`, `promote-pending`, `rejected`, `superseded`.

`promotion_owner`: `inventory`, `ontology-vault`, `definitions-governance`, `context-builder`, `invoke`, `repository-harness`, `other`.

`handoff_target`: `context-builder`, `ontology-vault`, `definitions-governance`, `invoke`, `repository-harness`, `other`.

## Validation Rules

- `set_id` must be unique within the EvidenceSet fixture or index.
- `card_refs` must be non-empty.
- Every `card_refs[].id` must resolve to an existing evidence-card ID.
- Every `excluded_card_refs[].id` must resolve to an existing evidence-card ID.
- Every included card must include a non-empty `inclusion_reason`.
- Every excluded card must include a non-empty `reason`.
- `index_terms` must be non-empty.
- `synthesis_note` and `residue` must be short strings, not long-form synthesis.
- EvidenceSets must not duplicate evidence-card source excerpts, summaries, trace arrays, or captured metadata.

## Candidate Boundary

This schema is candidate-level. It proves a useful artifact shape for agent/runtime validation; it does not promote EvidenceSet to canonical Inventory behavior by itself.

Canonical promotion requires a later explicit decision after the candidate fixture and validator remain useful across more than the current POC slices.

## Non-Goals

- No source excerpt duplication.
- No ontology or definitions authority.
- No replacement for Context Builder handoff packs.
- No ledger, dependency graph, or lifecycle manager.
- No human UI fields.
- No ranking or scoring model.
- No nested multi-artifact package.
