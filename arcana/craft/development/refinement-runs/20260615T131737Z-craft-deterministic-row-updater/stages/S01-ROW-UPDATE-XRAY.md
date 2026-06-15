# S01 X-Ray: Row Update Pipeline

## Hidden Structure

The proposed updater is not a ledger editor. It is a deterministic patch-plan
planner with a narrow contract.

```text
ledger.yml
  -> parse row families
  -> build row selectors and reference graph
  -> accept proposed delta
  -> validate source hash, row id, family, field, references, enums, and read-only state
  -> emit patch plan
  -> later owner applies or rejects patch plan
```

## Components

| Component | Responsibility | Authority |
| --- | --- | --- |
| Source ledger loader | Parse `.craft/ledger.yml` and compute `ledger_sha256`. | Read-only source authority. |
| Row selector resolver | Locate exactly one row by family and stable ID. | Derived lookup. |
| Delta normalizer | Convert CSV/form/CLI field changes into typed candidate deltas. | Derived staging. |
| Row update planner | Produce add/update/remove path operations for allowed scalar/list-link fields. | Dry-run plan only. |
| Safety validator | Block stale source, ID churn, missing references, enum drift, unsupported family, and read-only nested fields. | Validation gate. |
| Patch plan report | Human-readable and JSON artifact describing what would change and why. | Evidence artifact, not mutation. |

## First Editable Surface

Start with scalar and simple list-link fields only. The first proof should avoid
arbitrary nested edits and whole-row replacement.

Recommended first families:

- `contexts`: `stage`, `gate`, `next_move`, `links`.
- `artifacts`: `status`, `notes`, `links`.
- `decisions`: `selected`, `rationale`, `status`, `blocking`, `links`.

Recommended read-only first:

- row IDs;
- parent/source/target references unless explicitly covered by a reference-check fixture;
- nested evidence objects;
- generated indexes;
- projection metadata.

## Failure Map

| Failure | Required Behavior |
| --- | --- |
| Projection hash stale | block patch plan. |
| Row ID changed or missing | block patch plan. |
| Unknown family | block with supported-family list. |
| Unsupported field | flag or block with read-only reason. |
| Reference target missing | block patch plan. |
| Enum value invalid | block patch plan. |
| No semantic diff | pass with no-op patch plan. |

## X-Ray Verdict

Pass. The narrow unit is coherent and can recompose into CSV import later.
