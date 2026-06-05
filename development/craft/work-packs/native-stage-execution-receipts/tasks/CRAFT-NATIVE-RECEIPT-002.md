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
| Status | completed |

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

## Completion Evidence

| Field | Value |
| --- | --- |
| Receipt path convention | `<run_dir>/receipts/<stage-file-without-md>.json` |
| Synthetic pass fixture | `/tmp/craft-native-receipt-002/receipts/01-context-builder.json` |
| Receipt-backed run | `/tmp/craft-native-receipt-002` |
| Missing-receipt run | `/tmp/craft-native-receipt-002-no-receipt` |
| Status | pass |

Validation performed:

```text
bash -n tools/arcanum
jq empty /tmp/craft-native-receipt-002/receipts/01-context-builder.json
tools/arcanum --exec --adapter local-skill --timeout 120 --output /tmp/craft-native-receipt-002/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no use existing run folder /tmp/craft-native-receipt-002'
jq '.stage_evidence[] | {stage,status,evidence_kind,handoff_path,receipt_path,blocked_reason}' /tmp/craft-native-receipt-002/evidence-index.json
tools/arcanum --exec --adapter local-skill --timeout 120 --output /tmp/craft-native-receipt-002-no-receipt-output.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no use existing run folder /tmp/craft-native-receipt-002-no-receipt'
jq '.stage_evidence[] | select(.stage == "Context Builder evidence baseline") | {stage,status,evidence_kind,handoff_path,receipt_path,blocked_reason}' /tmp/craft-native-receipt-002-no-receipt/evidence-index.json
```

Observed result:

- With a valid synthetic receipt, `Context Builder evidence baseline` records `status=pass`, `evidence_kind=receipt`, and `receipt_path=/tmp/craft-native-receipt-002/receipts/01-context-builder.json`.
- Without a receipt, the same stage remains `status=flag`, `evidence_kind=handoff_prepared`, and `receipt_path=null`.

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
