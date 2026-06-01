# Execution Pack: Refine Runtime Stage Receipts

## Purpose

Sequence the implementation waves for repairing native Refine stage receipt semantics.

## Waves

| Wave | Layer | Goal | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-packs/refine-runtime-stage-receipts/waves/W0.md) | L0 | Fix handoff-stub classification. | CRAFT-RECEIPT-001 | Work-pack exists. | Handoff stub is not marked pass. |
| [W1](work-packs/refine-runtime-stage-receipts/waves/W1.md) | L1 | Materialize dispatch before stages. | CRAFT-RECEIPT-002 | W0 passed. | `REFINE-DISPATCH.json` exists and validates. |
| [W2](work-packs/refine-runtime-stage-receipts/waves/W2.md) | L2 | Harden evidence index/manifest semantics. | CRAFT-RECEIPT-003 | W1 passed. | Evidence index distinguishes handoff/receipt/artifact states. |
| [W3](work-packs/refine-runtime-stage-receipts/waves/W3.md) | L3 | Rerun Craft validation and sync state. | CRAFT-RECEIPT-004 | W2 passed. | Craft README/session ledger point to honest next route. |

## Parallelization

No parallel execution recommended. Each wave changes the validity criteria for the next wave.

## Stop Conditions

- Stop if `tools/arcanum --resolve dispatch-spec` or `tools/arcanum --resolve runtime-handoff` regresses.
- Stop if a proposed change would reintroduce nested model-backed CLI execution as the default native path.
- Stop if generated evidence cannot be inspected with local shell and `jq`.
