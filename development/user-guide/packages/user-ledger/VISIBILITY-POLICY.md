# User Ledger Visibility Policy

## Purpose

Define the first candidate visibility and promotion boundary for User ledger records.

## Default Policy

All User ledger rows are `local_private` by default.

Rows may become `session_visible`, `exportable`, or `promotion_candidate` only through explicit user action or a future policy rule approved in a later lifecycle stage.

## Visibility Rules

| Rule ID | Scope | Rule | Enforcement |
| --- | --- | --- | --- |
| VP-001 | all rows | Store local learning memory as protected context. | Default `visibility = local_private`. |
| VP-002 | receipts | Store bounded summaries and evidence, not full transcripts by default. | Receipt schemas should require summary fields, not transcript fields. |
| VP-003 | vocabulary preferences | Preferences are practical explanation hints, not identity traits. | Block hidden trait inference. |
| VP-004 | glossary entries | User-local glossary is not canonical Arcanum knowledge. | Block Inventory/Ontology promotion without owner review. |
| VP-005 | residue | Residue guides future explanations; it is not a deficiency label. | Use neutral friction language. |
| VP-006 | export/reset | Runtime export/reset behavior is deferred. | Record as L3 runtime gap. |

## Promotion Boundary

```text
user glossary entry
  -> user-local consultation
  -> optional promotion candidate after explicit user request
  -> Inventory/Ontology owner review
  -> canonical promotion or rejection
```

No User ledger row can directly mutate:

- `registry/`,
- `arcana/ontology-vault/`,
- `arcana/inventory/`,
- canonical glossaries,
- command surfaces,
- runtime memory stores.

## Runtime Gap

This policy is not yet a runtime privacy implementation. It is a development package guardrail for fixture and schema work.
