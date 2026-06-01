# Evidence-Card Schema Template

Schema Artifact Role: non-canonical

Canonical machine-readable schema: `arcana/inventory/templates/evidence-card.schema.yml`

## Purpose

Development reference for the Inventory evidence-card contract. This file is retained as package refresh evidence and must not be treated as the canonical machine-readable schema.

## YAML Shape

```yaml
id: inventory.card.<stable-slug>
schema_version: inventory.evidence-card.v0.2
profile: full | minimal
card_type: source-summary | concept | method | claim | question | context | relation-candidate | contradiction-candidate | operational-lesson
title: string
summary: string
source_refs:
  - path: string
    selector: string
    selector_type: file | heading | line-span | anchor | query | fragment
    start_line: number?
    end_line: number?
    fragment_kind: section | heading | line | symbol | commit | clause | region | other?
authority_level: raw-source | session-evidence | discovery-baseline | inventory-knowledge | ontology-candidate | downstream-governed-ref
tags: [string]
selection_reason: string
captured:
  by: human | agent | tool
  at: YYYY-MM-DD
  tool_or_command: string?
  source_stage: context-builder | invoke-define | distill | invoke-design | pilot | manual | other
promotion_status: captured | candidate | proposed | promoted | rejected | superseded | blocked
promotion_owner: none | inventory | ontology-vault | definitions-governance | context-builder | invoke | repository-harness | other
governed_ref: string?
handoff_targets: [ontology-vault | definitions-governance | context-builder | invoke | repository-harness]
related_cards: [inventory.card.id]
claim_shape:
  subject_ref: string?
  predicate_label: string?
  predicate_status: captured | unresolved | proposed | cataloged?
  object_ref: string?
  target_resolution: resolved | unresolved | proposed?
  evidence_refs: [string]?
  non_authority_notice: string?
trace:
  - field: string
    rule: string
    source_ref: string
    confidence: number
    decision: assigned | inferred | copied | rejected | deferred
residue:
  type: schema | instance | both | none
  status: open | proposed | deferred | scoped-out | declared | resolved
  surfaced_by: string?
  note: string?
open_questions: [inventory.card.id]
updated_at: YYYY-MM-DD
```

## Field Tiers

Required for every card: `id`, `schema_version`, `profile`, `card_type`, `title`, `summary`, `source_refs`, `authority_level`, `tags`, `selection_reason`, `captured`, `promotion_status`, `promotion_owner`, `updated_at`.

Required for `profile: full`: `handoff_targets`, `trace`.

Optional: `governed_ref`, `related_cards`, `claim_shape`, `residue`, `open_questions`.

## Authority Rules

- Inventory may record candidates; it does not promote ontology relations or canonical definitions.
- Trace confidence is extraction/rule confidence only.
- `promotion_status` values `promoted`, `rejected`, `superseded`, and `blocked` require `promotion_owner` other than `none`.
- Relation candidates require `claim_shape.non_authority_notice`.
