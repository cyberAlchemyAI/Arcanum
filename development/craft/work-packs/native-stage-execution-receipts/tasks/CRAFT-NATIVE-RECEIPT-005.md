# Task CRAFT-NATIVE-RECEIPT-005: Rerun Craft Validation And Sync Receipt-Backed State

## Objective

Rerun Craft Refine validation after the Context Builder receipt path exists, then synchronize Craft package state with the latest honest result.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L3 |
| Slice | S-NATIVE-RECEIPT-005 |
| Wave | W3 |
| Complexity | low |
| Status | completed |

## Source Contracts

- `development/craft/CRAFT-VALIDATION.md`
- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- latest receipt-backed Refine run evidence

## Dependencies

- CRAFT-NATIVE-RECEIPT-004 must pass or produce an actionable receipt-backed block.

## Smallest Working Units

### SWU-CRAFT-NATIVE-RECEIPT-005

Goal: record the latest Craft validation status and next route after receipt-backed native stage evidence exists.

Source anchors:

- Latest receipt-backed `RUN-MANIFEST.md`
- Latest receipt-backed `evidence-index.json`
- `CRAFT-PROMOTION-READINESS.md`

Related context:

- Promotion remains deferred unless separately approved.
- A block is acceptable if it is receipt-backed and names the next exact owner-stage blocker.

Write scope:

- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- current work-pack/task evidence

Implementation detail:

1. Rerun Craft validation with native Refine.
2. Inspect dispatch validation, stage receipts, manifest status, and result.
3. Update README/session ledger to name the receipt-backed state.
4. Preserve promotion deferral.
5. Mark the work-pack state according to evidence.

Done criteria:

- README and session ledger agree on latest receipt-backed validation status.
- The next route names either the next owner-stage receipt gap or the next Craft validation action.
- Promotion remains deferred.

Acceptance evidence:

- Refine run exists with receipt-aware stage evidence.
- Package sync grep shows matching status and next route.

Validation:

```text
tools/arcanum --exec --adapter local-skill --timeout 240 --output <tmp>/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'
rg -n "receipt|refine|promotion.*defer|next" development/craft/README.md development/craft/SESSION-LEDGER.md
```

Execution owner: manual.

## Completion Evidence

| Field | Value |
| --- | --- |
| Latest receipt-backed run | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof` |
| Dispatch validation | pass |
| Run status | block |
| First remaining blocker | `Invoke Define` has `evidence_kind=handoff_prepared` and no receipt. |
| Package sync | pass |
| Promotion status | deferred |

Validation performed:

```text
python3 formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-DISPATCH.json
jq '.stage_evidence[] | {stage,status,evidence_kind,handoff_path,receipt_path,blocked_reason}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json
rg -n "receipt|refine|promotion.*defer|next|Invoke Define" development/craft/README.md development/craft/SESSION-LEDGER.md
```

Result:

- Craft now has durable receipt-backed validation evidence for the Context Builder stage.
- The current validation blocker has moved to the next owner stage: `Invoke Define` needs its own parent-native receipt.
- Promotion remains deferred.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-NATIVE-RECEIPT-005
result: pass | flag | block
files_touched:
  - development/craft/README.md
  - development/craft/SESSION-LEDGER.md
validation:
  - refine rerun
  - package sync grep
blockers:
  - none or next receipt-backed owner-stage blocker
handoff_note: Craft state synchronized with latest receipt-backed validation
```
