# Task CRAFT-NATIVE-RECEIPT-001: Define Stage Receipt Contract

## Objective

Define the minimal stage receipt contract required for native Refine to distinguish completed owner-stage work from prepared runtime-native handoffs.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L0 |
| Slice | S-NATIVE-RECEIPT-001 |
| Wave | W0 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/evidence-index.json`
- `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-IMPLEMENTATION-LAYERING.md`
- `tools/arcanum` function `record_refine_stage`

## Dependencies

None.

## Smallest Working Units

### SWU-CRAFT-NATIVE-RECEIPT-001

Goal: create a reviewable receipt schema/example for owner-stage execution evidence.

Source anchors:

- Latest evidence index `stage_evidence[]`
- `tools/arcanum` stage evidence fields: `stage`, `owner`, `status`, `evidence_kind`, `artifact_path`, `handoff_path`, `receipt_path`, `blocked_reason`

Related context:

- Handoff-only stages must remain non-pass.
- Receipt-backed stages may be `pass`, `flag`, or `block`.

Write scope:

- `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md`
- optional receipt schema/example under `development/craft/work-packs/native-stage-execution-receipts/`

Implementation detail:

1. Define required receipt fields: `receipt_id`, `run_id`, `stage`, `owner`, `status`, `evidence_kind`, `artifact_paths`, `validation`, `blockers`, and `handoff_path`.
2. Define allowed receipt statuses: `pass`, `flag`, `block`, `interrupted`, `timeout`.
3. Define mapping to native Refine stage evidence:
   - `pass` receipt maps to stage `pass` with `evidence_kind=receipt`.
   - `flag` receipt maps to stage `flag` with `evidence_kind=receipt`.
   - `block`, `interrupted`, or `timeout` receipt maps to stage `block` or `flag` with an actionable reason.
4. Include a minimal Context Builder receipt example.
5. Keep the contract local to Craft/native Refine until a separate runtime interface plan promotes it.

Done criteria:

- Receipt contract has required fields and status mapping.
- Contract explains why handoff stubs are not receipts.
- Contract names the validation shape a Task Session or parent-native worker must return.

Acceptance evidence:

- Markdown receipt contract section or schema/example exists.
- Review confirms every receipt can map into `stage_evidence[]`.

Validation:

```text
rg -n "receipt_id|evidence_kind|handoff_path|status|validation|blockers" development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md development/craft/work-packs/native-stage-execution-receipts
```

Execution owner: local-fallback.

## Completion Evidence

| Field | Value |
| --- | --- |
| Receipt contract | `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md` |
| Contract status | pass |
| Validation | `rg -n "receipt_id|evidence_kind|handoff_path|status|validation|blockers" development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md development/craft/work-packs/native-stage-execution-receipts` |

Result:

- Required receipt fields are named.
- Allowed statuses and native Refine stage mappings are defined.
- Handoff stubs are explicitly excluded from receipt evidence.
- Context Builder pass and block examples are included.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-NATIVE-RECEIPT-001
result: pass | flag | block
files_touched:
  - development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md
validation:
  - receipt contract grep or review result
blockers:
  - none or named contract ambiguity
handoff_note: contract ready for receipt ingestion implementation
```
