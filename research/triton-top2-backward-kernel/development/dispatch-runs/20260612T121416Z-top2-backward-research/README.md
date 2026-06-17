# Dispatch Run - Triton Top2 Backward Research

Run id: `20260612T121416Z-top2-backward-research`

Dispatch: `research/triton-top2-backward-kernel/top2-backward-research.dispatch.json`

Dispatch id: `triton-top2-backward-kernel-research-20260612`

Status: `flag`

## Summary

This run executes the validated research dispatch as an artifact-backed closeout.
The research tower exists and covers the requested context. The run is `flag`
instead of `pass` because the research discovered real unresolved specification
choices that block honest implementation:

- exact continuous relaxation is not selected;
- top-2 combine semantics are not selected;
- capacity constraint semantics are not selected;
- `FFN(X)` scope is not selected;
- target GPU/Triton version is not captured.

The correct next execution is not writing Triton yet. It is selecting a named
relaxation and building a PyTorch reference/TDD harness.

## Receipts

| Step | Status | Receipt |
| --- | --- | --- |
| recover-context | pass | `receipts/01-recover-context.md` |
| govern-definitions | pass | `receipts/02-govern-definitions.md` |
| claim-ledger | pass | `receipts/03-claim-ledger.md` |
| derive-backward | pass | `receipts/04-derive-backward.md` |
| implementation-research | pass | `receipts/05-implementation-research.md` |
| synthesize-learning-pack | flag | `receipts/06-synthesize-learning-pack.md` |
| route-validation | pass | `receipts/07-route-validation.md` |
| closeout | flag | `CLOSEOUT.md` |
