# Task CRAFT-INVOKE-RECEIPT-002: Execute Invoke Define And Write Receipt

## Objective

Execute the current `Invoke Define` owner stage through the parent/native surface or write an actionable block receipt if execution cannot be completed.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L1 |
| Slice | S-INVOKE-RECEIPT-002 |
| Wave | W1 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/context-builder/context-pack.md`
- `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md`
- `spells/invoke/define.md`

## Dependencies

- CRAFT-INVOKE-RECEIPT-001 must pass.

## Smallest Working Units

### SWU-CRAFT-INVOKE-RECEIPT-002

Goal: produce `receipts/02-invoke-define.json` for the current run.

Source anchors:

- Stage handoff prompt in `stages/02-invoke-define.md`.
- Expected receipt path `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`.
- Resume command in the same handoff.

Related context:

- The stage request is:

```text
define refinement target=development/craft/CRAFT-VALIDATION.md using seed=development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md and context=development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/01-context-builder.md; preset=standard; preserve native output contract
```

- The context-builder receipt already passed and should not be reopened.
- This task may produce a `pass`, `flag`, or `block` receipt according to evidence.

Write scope:

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`
- optional owner artifact under `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/`
- optional task-session evidence under `development/craft/task-sessions/`

Implementation detail:

1. Read the stage handoff and source inputs.
2. Execute the Invoke Define owner-stage work directly in the parent/native surface:
   - produce a compact define-stage artifact for refining `CRAFT-VALIDATION.md`,
   - cite the seed proposal and context-builder evidence,
   - preserve the native output contract,
   - avoid claims about downstream Interrogation, Distill, Invoke Design, or Invoke Plan.
3. If the stage succeeds, write a `pass` receipt with:
   - `stage`: `Invoke Define`,
   - `owner`: `invoke`,
   - `evidence_kind`: `receipt`,
   - `handoff_path`: the current stage file,
   - `artifact_paths`: the actual define-stage artifact path(s),
   - `validation`: artifact existence and source-contract checks,
   - `blockers`: empty array.
4. If the stage cannot execute, write a `block` receipt with:
   - empty or partial artifact paths,
   - validation note explaining failure,
   - blocker with exact recovery action.
5. Validate receipt JSON with `jq empty`.

Done criteria:

- `receipts/02-invoke-define.json` exists.
- Receipt follows the local stage receipt contract.
- Pass receipts cite at least one real artifact path.
- Block receipts name an actionable blocker.

Acceptance evidence:

- `jq empty` passes for the receipt.
- Every artifact path in a pass receipt exists.
- Receipt status and validation match the observed execution.

Validation:

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
jq -r '.artifact_paths[]?' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json | xargs -r -I{} test -e {}
jq '{stage,owner,status,evidence_kind,handoff_path,artifact_paths,validation,blockers}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
```

Execution owner: manual or local-fallback.

## Completion Evidence

| Field | Value |
| --- | --- |
| Context pack | `development/craft/task-sessions/20260602T151215Z-CRAFT-INVOKE-RECEIPT-002-CONTEXT.md` |
| Owner-stage artifact | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/RESULT.md` |
| Receipt | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json` |
| Task-session result | `development/craft/task-sessions/20260602T151215Z-CRAFT-INVOKE-RECEIPT-002-RESULT.md` |
| Status | pass |

Validation performed:

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
jq -r '.artifact_paths[]?' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json | xargs -r -I{} test -e {}
jq '{stage,owner,status,evidence_kind,handoff_path,artifact_paths,validation,blockers}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
rg -n "Mode: define|Target: development/craft/CRAFT-VALIDATION.md|REFINE-SEED-PROPOSAL|01-context-builder|downstream" development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/RESULT.md
```

Observed result:

- `receipts/02-invoke-define.json` parses with `jq`.
- The pass receipt cites an existing owner-stage artifact.
- The owner-stage artifact cites the seed proposal and Context Builder evidence.
- The owner-stage artifact explicitly defers downstream stages.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-INVOKE-RECEIPT-002
result: pass
files_touched:
  - development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
  - development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/RESULT.md
validation:
  - receipt JSON validation
  - artifact existence check
blockers:
  - none
handoff_note: receipt ready for native Refine rerun
```
