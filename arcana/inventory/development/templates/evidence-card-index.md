# Evidence-Card Index And Retrieval Contract

## Index Families

| Index | Key | Purpose |
| --- | --- | --- |
| cards-by-id | `id` | Stable lookup. |
| cards-by-source | `source_refs.path`, selector fields | Traceability and re-ingest impact checks. |
| cards-by-tag | `tags[]` | Topic and task lookup. |
| cards-by-type | `card_type`, `profile` | Validation and retrieval filtering. |
| cards-by-authority | `authority_level` | Authority boundary checks. |
| cards-by-promotion | `promotion_status`, `promotion_owner` | Downstream state and drift review. |
| cards-by-handoff-target | `handoff_targets[]` | Packet assembly. |
| cards-by-cohort | cohort tag or future field | Pilot/source selection. |
| cards-by-related-card | `related_cards[]` | Navigation and tension lookup. |
| cards-by-residue | `residue.type`, `residue.status` | Open gap lookup. |
| cards-by-trace-rule | `trace.rule`, `trace.decision` | Audit extraction choices. |

## Retrieval Output Shape

```yaml
query:
  purpose: string
  filters: object
selected_cards:
  - id: inventory.card.id
    schema_version: string
    profile: full | minimal
    card_type: string
    title: string
    summary: string
    source_refs: []
    authority_level: string
    selection_reason: string
    promotion_status: string
    promotion_owner: string
    residue: object?
unresolved_questions: []
handoff_candidates: []
excluded_matches:
  - id: inventory.card.id
    reason: string
trace_notes: []
```

## Retrieval Rule

Return compact task-shaped selections with excluded matches and trace notes. Do not return a full inventory dump unless explicitly requested.
