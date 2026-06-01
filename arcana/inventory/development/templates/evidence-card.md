# Evidence-Card Authoring Template

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
  note: ""
open_questions: []
updated_at: YYYY-MM-DD
```

## Authoring Notes

- Use `profile: minimal` only for honest triage or source-selection scaffolding.
- Minimal cards still need source refs, authority level, selection reason, captured metadata, promotion fields, and update date.
- Do not use `promoted` unless a downstream owner and real governed reference exist.
