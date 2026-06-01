# Task CRAFT-RECEIPT-003: Harden Manifest And Evidence Index Semantics

## Objective

Update native Refine run evidence so manifests and indexes distinguish handoff, receipt, owner artifact, flag, and block states.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L2 |
| Slice | S-RECEIPT-003 |
| Wave | W2 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `tools/arcanum`
- `arcana/refine/templates/evidence-index.json`
- `arcana/refine/templates/run-manifest.md`
- `arcana/refine/templates/usage-telemetry.md`

## Dependencies

- CRAFT-RECEIPT-002 must pass.

## Smallest Working Units

### SWU-CRAFT-RECEIPT-003

Goal: generated evidence records the difference between handoff preparation and completed stage execution.

Write scope:

- `tools/arcanum`
- optional task-session evidence artifact

Implementation detail:

1. Extend `record_refine_stage` payload or the generated evidence index with evidence fields such as `evidence_kind`, `handoff_path`, `artifact_path`, `receipt_path`, and `blocked_reason`.
2. Update `write_native_refine_outputs` so final status is computed from real stage statuses, not file existence alone.
3. Ensure `pass` stage entries have owner artifact evidence or a validated special-case such as Context Builder persisted context pack.
4. Ensure `flag` and `block` statuses carry actionable reasons.

Done criteria:

- Evidence index can answer whether each stage was executed, handed off, flagged, or blocked.
- Manifest status matches evidence index status.

Validation:

```text
jq '.stage_evidence[] | {stage,status,evidence_kind,artifact,handoff_path,blocked_reason}' <generated-run>/evidence-index.json
```

Execution owner: local-fallback.

## Completion Evidence

| Field | Value |
| --- | --- |
| Completed run | `development/craft/development/refinement-runs/20260601T014741Z-craft-validation-md` |
| Dispatch validation | `pass` |
| Run status | `block` |
| Evidence contract result | `pass` |

Validation performed:

```text
bash -n tools/arcanum
tools/arcanum --exec --adapter local-skill --timeout 120 --output /tmp/craft-receipt-003/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'
python3 formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/development/refinement-runs/20260601T014741Z-craft-validation-md/REFINE-DISPATCH.json
jq '.stage_evidence[] | {stage,status,evidence_kind,artifact,artifact_path,handoff_path,receipt_path,blocked_reason}' development/craft/development/refinement-runs/20260601T014741Z-craft-validation-md/evidence-index.json
```

Evidence interpretation:

- `Task Zero Observer Envelope` is `pass` with `evidence_kind=observer_envelope`.
- `Context Builder evidence baseline` is `flag` with `evidence_kind=handoff_prepared` and a populated `handoff_path`.
- Downstream dependent stages are `block` with `evidence_kind=blocked` and actionable dependency reasons.
- `RUN-MANIFEST.md` and `evidence-index.json` agree on run status `block`.
