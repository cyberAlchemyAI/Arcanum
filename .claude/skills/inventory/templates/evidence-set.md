# EvidenceSet Authoring Template

Use this template to author candidate Inventory EvidenceSets.

EvidenceSets should stay small, flat, and agent-readable. Use them when a task repeatedly needs the same group of evidence-card IDs plus boundary exclusions.

```yaml
schema_version: inventory.evidence-set.v0.1
set_id: evidence-set.<stable-slug>
purpose: ""
card_refs:
  - id: inventory.card.<stable-slug>
    inclusion_reason: ""
excluded_card_refs:
  - id: inventory.card.<stable-slug>
    reason: ""
index_terms: []
handoff_target: context-builder
synthesis_note: ""
residue: ""
status: candidate
promotion_owner: inventory
updated_at: YYYY-MM-DD
```

## Authoring Notes

- Reference evidence-card IDs only; do not copy card summaries or source excerpts into the set.
- Include exclusions when nearby cards look relevant but are outside the set boundary.
- Keep `synthesis_note` to one short explanation of what the group preserves.
- Keep `residue` focused on unresolved scope or promotion limits.
- Use `status: candidate` until an explicit promotion decision exists.
- Keep human review/UI details outside the schema.
