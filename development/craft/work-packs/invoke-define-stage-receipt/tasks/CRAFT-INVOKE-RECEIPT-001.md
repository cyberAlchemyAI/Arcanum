# Task CRAFT-INVOKE-RECEIPT-001: Define Invoke Define Receipt Contract

## Objective

Define the exact artifact and receipt evidence needed for the current `Invoke Define` stage to count as parent-native owner-stage execution.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L0 |
| Slice | S-INVOKE-RECEIPT-001 |
| Wave | W0 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`
- `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/context-builder/context-pack.md`
- `spells/invoke/README.md`
- `spells/invoke/define.md`

## Dependencies

None.

## Smallest Working Units

### SWU-CRAFT-INVOKE-RECEIPT-001

Goal: make the `Invoke Define` receipt contract unambiguous enough for task-session or a parent-native worker to execute without reopening Craft architecture discovery.

Source anchors:

- Stage request in `stages/02-invoke-define.md`.
- Expected receipt path `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`.
- Receipt contract required fields.
- Invoke define-mode owner contract.

Related context:

- The stage output file currently contains only a runtime-native handoff.
- A pass receipt must cite at least one real owner-stage artifact path.
- A block receipt is acceptable if it names the exact missing parent/native execution capability or missing Invoke define input.

Write scope:

- `development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md`
- optional shared note under `development/craft/work-packs/invoke-define-stage-receipt/shared/`

Implementation detail:

1. Read `stages/02-invoke-define.md` and extract:
   - run id,
   - stage title,
   - owner,
   - stage request,
   - handoff path,
   - expected receipt path,
   - resume command.
2. Define the minimum pass artifact for this stage:
   - either replace or supplement `stages/02-invoke-define.md` with an actual Invoke Define result,
   - or write a separate artifact under the current run folder and cite it from the receipt.
3. Define the minimum pass validation:
   - artifact path exists,
   - artifact states target `development/craft/CRAFT-VALIDATION.md`,
   - artifact uses the seed proposal and Context Builder output as source inputs,
   - artifact preserves the native output contract and does not claim downstream stages completed.
4. Define the minimum block validation:
   - receipt status is `block`,
   - blocker explains what prevented owner-stage execution,
   - blocker includes an actionable next action.
5. Preserve the receipt contract fields:
   - `receipt_id`,
   - `run_id`,
   - `stage`,
   - `owner`,
   - `status`,
   - `evidence_kind`,
   - `handoff_path`,
   - `artifact_paths`,
   - `validation`,
   - `blockers`,
   - `created_at`,
   - `worker`.

Done criteria:

- The next worker knows exactly what artifact to produce or inspect.
- The next worker knows how to write a pass or block receipt.
- No downstream stage is included in this task.

Acceptance evidence:

- Review confirms the task contract names all required receipt fields.
- Review confirms pass/block criteria are explicit.

Validation:

```text
rg -n "Invoke Define|expected receipt|artifact_paths|validation|blockers|receipt_id|handoff_path" development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md
```

Execution owner: local-fallback.

## Completion Evidence

| Field | Value |
| --- | --- |
| Context pack | `development/craft/task-sessions/20260602T145930Z-CRAFT-INVOKE-RECEIPT-001-CONTEXT.md` |
| Shared contract | `development/craft/work-packs/invoke-define-stage-receipt/shared/invoke-define-receipt-contract.md` |
| Task-session result | `development/craft/task-sessions/20260602T145930Z-CRAFT-INVOKE-RECEIPT-001-RESULT.md` |
| Status | pass |

Validation performed:

```text
rg -n "Invoke Define|expected receipt|artifact_paths|validation|blockers|receipt_id|handoff_path" development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md development/craft/work-packs/invoke-define-stage-receipt/shared/invoke-define-receipt-contract.md
```

Observed result:

- The shared contract names the exact stage identity, expected receipt path, pass artifact contract, pass receipt contract, block receipt contract, and validation checks.
- No runtime, registry, command, sigil, spell, promotion, downstream receipt, or validation-rerun work was executed.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-INVOKE-RECEIPT-001
result: pass
files_touched:
  - development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md
  - development/craft/work-packs/invoke-define-stage-receipt/shared/invoke-define-receipt-contract.md
validation:
  - contract grep passed
blockers:
  - none
handoff_note: contract ready for Invoke Define owner-stage execution
```
