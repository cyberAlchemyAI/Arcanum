# Task CRAFT-INVOKE-RECEIPT-003: Local Skill Validation Sync

## Objective

Re-evaluate Craft validation through the local Refine skill after the `Invoke Define` receipt exists, then synchronize package state with the latest honest evidence.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L2 |
| Slice | S-INVOKE-RECEIPT-003 |
| Wave | W2 |
| Complexity | low |
| Status | completed |

## Source Contracts

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`
- `development/craft/CRAFT-VALIDATION.md`
- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- `development/craft/CRAFT-PROMOTION-READINESS.md`
- `arcana/refine/SKILL.md`

## Dependencies

- CRAFT-INVOKE-RECEIPT-002 must produce a receipt, even if that receipt is `block`.

## Smallest Working Units

### SWU-CRAFT-INVOKE-RECEIPT-003

Goal: make Craft package state reflect the latest receipt-backed validation state using the local skill surface.

Source anchors:

- Latest `evidence-index.json` stage evidence.
- `RESULT.md` verdict table.
- README current verdict and next move.
- SESSION-LEDGER open gaps and task board.
- `arcana/refine/SKILL.md` local skill contract.

Related context:

- Promotion remains deferred.
- If `Invoke Define` passes, the next validation blocker may move to Interrogation, Distill, Invoke Design, or a later stage.
- If `Invoke Define` blocks, preserve the block receipt and route to its recovery action.

Write scope:

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RESULT.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RUN-MANIFEST.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json`
- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md`
- optional task-session evidence under `development/craft/task-sessions/`

Implementation detail:

1. Validate `receipts/02-invoke-define.json`.
2. Read and follow `arcana/refine/SKILL.md` as the local Refine execution contract.
3. Re-evaluate the current run folder directly from local artifacts:
   - `REFINE-DISPATCH.json`,
   - `REFINE-SEED-PROPOSAL.md`,
   - `stages/native-stage-evidence.jsonl`,
   - `receipts/01-context-builder.json`,
   - `receipts/02-invoke-define.json`,
   - stage artifacts under `stages/`.
4. Update `evidence-index.json`, `RUN-MANIFEST.md`, and `RESULT.md` from local skill evidence only. Do not call `tools/arcanum --exec`, `.codex/commands`, or command resolution.
5. Inspect `evidence-index.json`:
   - `Invoke Define` should now have `evidence_kind=receipt`,
   - status should match the receipt,
   - `receipt_path` should point to `receipts/02-invoke-define.json`.
6. Identify the first remaining non-pass stage, if any.
7. Sync README and SESSION-LEDGER:
   - current verdict,
   - latest run,
   - receipt-backed state,
   - recommended next route.
8. Update this work-pack's task board with completion evidence.
9. Preserve Craft promotion deferral.

Done criteria:

- Local Refine skill re-evaluation completed and evidence is inspectable.
- README and SESSION-LEDGER agree on the latest state.
- Next route names the next exact blocker or validation completion path.
- Promotion remains deferred.

Acceptance evidence:

- `jq` confirms `Invoke Define` receipt-backed evidence.
- `rg` confirms README/session ledger mention the updated state and next route.

Validation:

```text
jq '.stage_evidence[] | select(.stage == "Invoke Define") | {status,evidence_kind,handoff_path,receipt_path,blocked_reason}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json
rg -n "Invoke Define|receipt|promotion.*defer|Current Next Move|Recommended" development/craft/README.md development/craft/SESSION-LEDGER.md
```

Execution owner: manual.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-INVOKE-RECEIPT-003
result: pass | flag | block
files_touched:
  - development/craft/README.md
  - development/craft/SESSION-LEDGER.md
  - development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md
validation:
  - local Refine skill re-evaluation
  - evidence-index inspection
  - package sync grep
blockers:
  - none or next exact receipt-backed blocker
handoff_note: Craft state synchronized after Invoke Define receipt
```

## Completion Evidence

| Field | Value |
| --- | --- |
| Context pack | `development/craft/task-sessions/20260602T202908Z-CRAFT-INVOKE-RECEIPT-003-CONTEXT.md` |
| Task-session result | `development/craft/task-sessions/20260602T202908Z-CRAFT-INVOKE-RECEIPT-003-RESULT.md` |
| Evidence index | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json` |
| Run manifest | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RUN-MANIFEST.md` |
| Refine result | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RESULT.md` |
| Status | pass |

Validation performed:

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json
jq '.stage_evidence[] | select(.stage == "Invoke Define") | {status,evidence_kind,handoff_path,receipt_path,blocked_reason}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json
rg -n "Interrogation refine-review|Invoke Define|receipt|promotion.*defer|Current Next Move|Recommended" development/craft/README.md development/craft/SESSION-LEDGER.md
```

Observed result:

- `Invoke Define` is now receipt-backed pass evidence in the run index.
- `RUN-MANIFEST.md` and `RESULT.md` agree with the evidence index.
- README and SESSION-LEDGER name `Interrogation refine-review` as the next exact blocker.
- Promotion remains deferred.
