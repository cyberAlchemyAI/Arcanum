# Inventory Index

This index is the content-oriented catalog of generated inventory pages.

Machine view: keep `index.json` in sync with this file. `index.md` is for
human navigation; `index.json` is the primary machine-readable lookup surface.
CSV files, when used, belong under `projections/` and are derived from
`index.json`.

## Pages

| Page | Type | Summary | Tags | Sources | Updated |
| ---- | ---- | ------- | ---- | ------- | ------- |
| _No pages yet_ |  |  |  |  |  |

## By Type

| Type | Pages | Notes |
| ---- | ----- | ----- |
| source | 0 | Raw source summaries. |
| concept | 0 | Reusable concepts and terms. |
| architecture-layer | 0 | Repository architecture layers. |
| implementation-pattern | 0 | Reusable implementation patterns. |
| decision | 0 | Durable decisions and rationale. |
| synthesis | 0 | Filed answers and cross-source analysis. |

## Evidence-Card Index Families

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

## EvidenceSet Index Families

| Index | Key | Purpose |
| --- | --- | --- |
| evidence-sets-by-id | `set_id` | Stable grouped-evidence lookup. |
| evidence-sets-by-card | `card_refs[].id`, `excluded_card_refs[].id` | Find groups affected by a card change. |
| evidence-sets-by-term | `index_terms[]` | Fast topic lookup through shell plus `jq`. |
| evidence-sets-by-handoff-target | `handoff_target` | Route grouped evidence to downstream packet assembly. |
| evidence-sets-by-status | `status`, `promotion_owner` | Keep candidate promotion state visible. |

## Evidence-Card Retrieval Output

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

Return compact task-shaped selections with `selected_cards`, `excluded_matches`, and `trace_notes`. Do not return a full inventory dump unless explicitly requested.

## EvidenceSet Output

```yaml
schema_version: inventory.evidence-set.v0.1
set_id: evidence-set.id
purpose: string
card_refs:
  - id: inventory.card.id
    inclusion_reason: string
excluded_card_refs:
  - id: inventory.card.id
    reason: string
index_terms: [string]
handoff_target: context-builder | ontology-vault | definitions-governance | invoke | repository-harness | other
synthesis_note: string
residue: string
status: candidate | promote-pending | rejected | superseded
promotion_owner: inventory | ontology-vault | definitions-governance | context-builder | invoke | repository-harness | other
updated_at: YYYY-MM-DD
```

EvidenceSets are candidate grouped-evidence artifacts. They reference evidence-card IDs only and must not duplicate card source excerpts or summaries.

## Open Gaps

- No gaps recorded yet.
