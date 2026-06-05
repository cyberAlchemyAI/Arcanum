# Execution Pack: Craft Invoke Define Stage Receipt

## Purpose

Sequence the waves for turning the current `Invoke Define` handoff into receipt-backed owner-stage evidence through local skill-surface execution.

## Waves

| Wave | Layer | Goal | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-packs/invoke-define-stage-receipt/waves/W0.md) | L0 | Define the `Invoke Define` receipt artifact contract. | CRAFT-INVOKE-RECEIPT-001 | Current run shows `Invoke Define` as `handoff_prepared`. | Task contract names the exact pass/block receipt evidence. |
| [W1](work-packs/invoke-define-stage-receipt/waves/W1.md) | L1 | Execute or block the `Invoke Define` owner stage and write the receipt. | CRAFT-INVOKE-RECEIPT-002 | W0 contract passed. | `receipts/02-invoke-define.json` exists and validates. |
| [W2](work-packs/invoke-define-stage-receipt/waves/W2.md) | L2 | Review Craft validation through the local Refine skill and sync state. | CRAFT-INVOKE-RECEIPT-003 | W1 receipt exists. | Evidence index and package state agree on the updated status and next route. |

## Parallelization

No parallel execution is recommended. The contract must exist before receipt execution, and receipt execution must complete before validation rerun.

## Stop Conditions

- Stop if the only available evidence is another handoff stub.
- Stop if owner-stage execution requires canonical runtime mutation not approved by this work-pack.
- Stop if the receipt cannot name artifact paths or actionable blockers.
- Stop if local Refine skill review cannot be inspected with `jq`, `rg`, and Markdown review.
