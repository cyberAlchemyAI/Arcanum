# Evidence-Card Authoring Template

Use this template to author source-backed Inventory evidence-cards.

The default shape is `profile: full` because POC cards are expected to support retrieval, validation, residue tracking, and downstream handoff review. Use `profile: minimal` only for honest triage cards that are not yet intended for retrieval or handoff assembly.

## Full Card

```yaml
id: inventory.card.<stable-slug>
schema_version: inventory.evidence-card.v0.2
profile: full
card_type: concept
title: ""
summary: ""
source_refs:
  - path: ""
    selector: ""
    selector_type: heading
    start_line:
    end_line:
    fragment_kind: section
authority_level: inventory-knowledge
tags: []
selection_reason: ""
captured:
  by: agent
  at: YYYY-MM-DD
  tool_or_command: ""
  source_stage: manual
promotion_status: captured
promotion_owner: none
governed_ref:
handoff_targets: []
related_cards: []
claim_shape:
  subject_ref: ""
  predicate_label: ""
  predicate_status: captured
  object_ref: ""
  target_resolution: unresolved
  evidence_refs: []
  non_authority_notice: ""
trace:
  - field: summary
    rule: source-backed-summary
    source_ref: ""
    confidence: 0.8
    decision: assigned
residue:
  type: none
  status: resolved
  surfaced_by: ""
  note: ""
open_questions: []
updated_at: YYYY-MM-DD
```

## Minimal Card

```yaml
id: inventory.card.<stable-slug>
schema_version: inventory.evidence-card.v0.2
profile: minimal
card_type: source-summary
title: ""
summary: ""
source_refs:
  - path: ""
    selector: ""
    selector_type: heading
authority_level: raw-source
tags: []
selection_reason: ""
captured:
  by: agent
  at: YYYY-MM-DD
  tool_or_command: ""
  source_stage: manual
promotion_status: captured
promotion_owner: none
updated_at: YYYY-MM-DD
```

## Authoring Notes

- Keep each card centered on one reusable source-backed claim, concept, question, method, or lesson.
- Use `profile: minimal` only for honest triage or source-selection scaffolding.
- Minimal cards still need source refs, authority level, selection reason, captured metadata, promotion fields, and update date.
- Do not use `promoted` unless a downstream owner and real governed reference exist.
- Use `card_type: relation-candidate` only with `claim_shape.evidence_refs`, `claim_shape.target_resolution`, and `claim_shape.non_authority_notice`.
- Use `residue` when the source exposes ambiguity, schema pressure, contradiction, or unresolved scope.
- For POC cards, prefer line-span selectors so reviewers can inspect material claims quickly.
