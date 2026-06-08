# Evidence-Card Schema

Schema Artifact Role: schema-template

Canonical machine-readable schema: `evidence-card.schema.yml`

## Purpose

Define the canonical Inventory evidence-card contract.

Evidence-cards capture source-backed knowledge for retrieval and downstream handoff. They may record candidates, questions, relations, contradictions, and operational lessons, but they do not promote ontology relations or canonical definitions by themselves.

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

## Controlled Vocabularies

`profile`: `full`, `minimal`.

`card_type`: `source-summary`, `concept`, `method`, `claim`, `question`, `context`, `relation-candidate`, `contradiction-candidate`, `operational-lesson`.

`selector_type`: `file`, `heading`, `line-span`, `anchor`, `query`, `fragment`.

`fragment_kind`: `section`, `heading`, `line`, `symbol`, `commit`, `clause`, `region`, `other`.

`authority_level`: `raw-source`, `session-evidence`, `discovery-baseline`, `inventory-knowledge`, `ontology-candidate`, `downstream-governed-ref`.

`captured.by`: `human`, `agent`, `tool`.

`captured.source_stage`: `context-builder`, `invoke-define`, `distill`, `invoke-design`, `pilot`, `manual`, `other`.

`promotion_status`: `captured`, `candidate`, `proposed`, `promoted`, `rejected`, `superseded`, `blocked`.

`promotion_owner`: `none`, `inventory`, `ontology-vault`, `definitions-governance`, `context-builder`, `invoke`, `repository-harness`, `other`.

`handoff_targets`: `ontology-vault`, `definitions-governance`, `context-builder`, `invoke`, `repository-harness`.

`claim_shape.predicate_status`: `captured`, `unresolved`, `proposed`, `cataloged`.

`claim_shape.target_resolution`: `resolved`, `unresolved`, `proposed`.

`trace.decision`: `assigned`, `inferred`, `copied`, `rejected`, `deferred`.

`residue.type`: `schema`, `instance`, `both`, `none`.

`residue.status`: `open`, `proposed`, `deferred`, `scoped-out`, `declared`, `resolved`.

## Profile Rules

- `profile: minimal` is allowed for lightweight cards where the source reference and summary are enough for review.
- `profile: full` is required when a card may be reused for retrieval, handoff, schema decisions, relation candidates, contradiction candidates, or downstream governance.
- Full cards must include `trace` so reviewers can distinguish copied source facts from inferred field assignments.
- Full cards must include `handoff_targets` when the card is intended to seed a downstream packet.

## Selector Rules

- Every material claim in `summary` must be inspectable through at least one `source_refs` entry.
- Prefer `selector_type: line-span` or `heading` for repository Markdown sources.
- Use `selector_type: query` only when a stable selector is unavailable, and record the query text in `selector`.
- `start_line` and `end_line` are required when `selector_type: line-span`.

## Authority Rules

- Inventory may record candidates; it does not promote ontology relations or canonical definitions.
- `authority_level` describes the evidence state, not downstream approval.
- Trace confidence is extraction or rule confidence only.
- `promotion_status` values `promoted`, `rejected`, `superseded`, and `blocked` require `promotion_owner` other than `none`.
- Relation candidates require `claim_shape.non_authority_notice`.
- Cards with `authority_level: ontology-candidate` must not imply that Ontology Vault has accepted the relation.
- Cards with `authority_level: downstream-governed-ref` must include `governed_ref`.

## Residue Rules

- Use `residue` when the card exposes ambiguity, unresolved scope, schema pressure, contradiction, or an implementation gap.
- Use `residue.type: schema` for questions about the card contract itself.
- Use `residue.type: instance` for ambiguity in the captured source.
- Use `residue.type: both` when the source ambiguity also pressures the schema.
- Use `residue.status: scoped-out` only when the current POC intentionally leaves the question unresolved.
