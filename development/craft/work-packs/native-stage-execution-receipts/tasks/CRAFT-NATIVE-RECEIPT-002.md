# Task CRAFT-NATIVE-RECEIPT-002: Implement Receipt Ingestion In Native Refine

## Objective

Teach native Refine to discover, validate, and record an owner-stage receipt before downstream stages depend on that stage.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L1 |
| Slice | S-NATIVE-RECEIPT-002 |
| Wave | W1 |
| Complexity | medium |
| Status | not-started |

## Source Contracts

- `tools/arcanum`
- `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md`
- `development/craft/work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-001.md`

## Dependencies

- CRAFT-NATIVE-RECEIPT-001 must pass.

## Smallest Working Units

### SWU-CRAFT-NATIVE-RECEIPT-002

Goal: native Refine can ingest a valid receipt file for a stage and propagate it into `RUN-MANIFEST.md` and `evidence-index.json`.

Source anchors:

- `tools/arcanum` functions `run_refine_command_stage`, `record_refine_stage`, and `write_native_refine_outputs`
- latest generated `stage_evidence[]` shape

Related context:

- Handoff output remains `handoff_prepared`.
- Receipt ingestion is allowed only when the receipt validates against the local contract.

Write scope:

- `tools/arcanum`
- optional generated fixture under `/tmp` or task-session evidence

Implementation detail:

1. Add a receipt path convention, for example `<run_dir>/receipts/<stage-slug>.json`.
2. Add a helper that checks whether a receipt exists and validates required fields with `jq`.
3. In `run_refine_command_stage`, after a handoff stub is detected, check for a valid receipt before returning `flag`.
4. Map valid receipt statuses into stage evidence:
   - receipt `pass`: status `pass`, `evidence_kind=receipt`, `receipt_path=<receipt>`.
   - receipt `flag`: status `flag`, `evidence_kind=receipt`, `receipt_path=<receipt>`.
   - receipt `block`/`interrupted`/`timeout`: status `block` or `flag` with `blocked_reason`.
5. Preserve the current behavior when no receipt exists.

Done criteria:

- A valid synthetic receipt can change a stage from handoff-only `flag` to receipt-backed status.
- Missing or invalid receipts do not produce `pass`.
- Evidence index and manifest expose `receipt_path`.

Acceptance evidence:

- `bash -n tools/arcanum` passes.
- `jq` inspection shows receipt-backed stage evidence for a synthetic receipt case.

Validation:

```text
bash -n tools/arcanum
jq empty <synthetic-receipt>.json
jq '.stage_evidence[] | {stage,status,evidence_kind,handoff_path,receipt_path,blocked_reason}' <generated-run>/evidence-index.json
```

Execution owner: local-fallback.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-NATIVE-RECEIPT-002
result: pass | flag | block
files_touched:
  - tools/arcanum
validation:
  - bash syntax check
  - synthetic receipt evidence inspection
blockers:
  - none or receipt validation ambiguity
handoff_note: ingestion ready for parent-native handoff/resume flow
```
