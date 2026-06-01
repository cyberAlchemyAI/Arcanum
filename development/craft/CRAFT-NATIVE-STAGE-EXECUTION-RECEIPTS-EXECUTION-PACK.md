# Execution Pack: Craft Native Stage Execution Receipts

## Purpose

Sequence the waves for creating a receipt-backed native Refine stage path after a stage handoff is prepared.

## Waves

| Wave | Layer | Goal | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-packs/native-stage-execution-receipts/waves/W0.md) | L0 | Define the stage receipt contract. | CRAFT-NATIVE-RECEIPT-001 | Receipt blocker evidence exists. | Receipt schema/example is reviewable. |
| [W1](work-packs/native-stage-execution-receipts/waves/W1.md) | L1 | Teach native Refine to ingest stage receipts. | CRAFT-NATIVE-RECEIPT-002 | W0 passed. | Synthetic receipt affects stage evidence classification. |
| [W2](work-packs/native-stage-execution-receipts/waves/W2.md) | L2 | Add parent-native handoff and resume flow. | CRAFT-NATIVE-RECEIPT-003, CRAFT-NATIVE-RECEIPT-004 | W1 passed. | Context Builder stage can return a receipt through parent/native execution. |
| [W3](work-packs/native-stage-execution-receipts/waves/W3.md) | L3 | Rerun Craft validation and sync state. | CRAFT-NATIVE-RECEIPT-005 | W2 passed. | README/session ledger point to receipt-backed validation status. |

## Parallelization

No parallel execution is recommended before W2. Receipt contract, ingestion, and parent handoff/resume semantics build on each other.

W2 tasks may be split only after W1 proves the receipt ingestion contract:

- CRAFT-NATIVE-RECEIPT-003 owns handoff/resume plumbing.
- CRAFT-NATIVE-RECEIPT-004 owns the first Context Builder receipt proof.

## Stop Conditions

- Stop if receipt ingestion would require counting a handoff as pass.
- Stop if the implementation requires broad cross-runtime adapter redesign.
- Stop if Task Session cannot produce or preserve the receipt artifact expected by native Refine.
- Stop if generated Refine evidence cannot be inspected with local shell, `jq`, and Markdown review.
