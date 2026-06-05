# Invoke Define Receipt Contract

## Purpose

Define the exact receipt evidence required for the current `Invoke Define` stage in the Craft Refine validation run.

This contract is local to `development/craft/`. It reuses the native stage receipt contract and narrows it to the current `Invoke Define` owner stage.

## Stage Identity

| Field | Value |
| --- | --- |
| Run id | `20260601T080122Z-context-builder-receipt-proof` |
| Stage | `Invoke Define` |
| Owner | `invoke` |
| Handoff path | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md` |
| Expected receipt path | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json` |

## Stage Request

```text
define refinement target=development/craft/CRAFT-VALIDATION.md using seed=development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md and context=development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/01-context-builder.md; preset=standard; preserve native output contract
```

## Pass Artifact Contract

A `pass` receipt for this stage must cite at least one owner-stage artifact path. The preferred artifact is a compact Invoke Define result under:

```text
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/
```

The owner-stage artifact must show:

1. Mode: `define`.
2. Spell/capability: `invoke`.
3. Target: `development/craft/CRAFT-VALIDATION.md`.
4. Source inputs:
   - `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md`
   - `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/01-context-builder.md`
5. Output interpretation for the refinement target.
6. Decisions or assumptions used by the parent-native worker.
7. Unresolved gaps or residue, if any.
8. Native output contract preservation.
9. Explicit statement that downstream Interrogation, Distill, Invoke Design, Invoke Plan, and final synthesis stages were not executed by this artifact.

## Pass Receipt Contract

A `pass` receipt must include:

```json
{
  "receipt_id": "receipt-20260601T080122Z-context-builder-receipt-proof-invoke-define",
  "run_id": "20260601T080122Z-context-builder-receipt-proof",
  "stage": "Invoke Define",
  "owner": "invoke",
  "status": "pass",
  "evidence_kind": "receipt",
  "handoff_path": "development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md",
  "artifact_paths": [
    "<invoke-define-owner-artifact>"
  ],
  "validation": [
    {
      "check": "owner-artifact-exists",
      "result": "pass",
      "notes": "artifact path exists and is cited by the receipt"
    },
    {
      "check": "source-contracts-cited",
      "result": "pass",
      "notes": "artifact cites the seed proposal and Context Builder stage"
    },
    {
      "check": "native-output-boundary",
      "result": "pass",
      "notes": "artifact does not claim downstream stages completed"
    }
  ],
  "blockers": []
}
```

## Block Receipt Contract

A `block` receipt is valid when parent-native execution cannot produce the owner-stage artifact. It must include:

1. `status`: `block`.
2. `evidence_kind`: `receipt`.
3. `artifact_paths`: empty array or partial evidence paths.
4. `validation`: at least one failing or blocking check.
5. `blockers`: at least one blocker with `id`, `reason`, and `next_action`.

Use this blocker id when the execution surface itself is missing:

```text
BLK-INVOKE-DEFINE-PARENT-NATIVE-EXECUTION
```

## Validation Checks

For a pass receipt:

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
jq -r '.artifact_paths[]?' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json | xargs -r -I{} test -e {}
rg -n "Mode:.*define|Target:.*CRAFT-VALIDATION|REFINE-SEED-PROPOSAL|01-context-builder|downstream" <invoke-define-owner-artifact>
```

For a block receipt:

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
jq -e '.status == "block" and .evidence_kind == "receipt" and (.blockers | length > 0)' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
```

## Boundary

This contract does not execute Invoke Define, write the receipt, run Refine validation, solve downstream owner-stage receipts, mutate canonical surfaces, or promote Craft.
