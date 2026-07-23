# TASK-NDR-005 — Causal Integration Canaries

Owner: Task Session

Objective: prove failure withholding and successful progression from the installed execution entry point, then correct the historical proof classification.

## SWU-NDR-011 — Run the failure-withholding canary

- Behavior: invoke only `orchestrate execute <dispatch.json>` on a two-wave fixture whose first wave returns non-pass, and prove the dependent role is never spawned.
- Split analysis: failure behavior is independently acceptable and must precede any success canary.
- Dependencies: `SWU-NDR-007`, `SWU-NDR-008`, `SWU-NDR-010`, and `SWU-NDR-010R` pass receipts.
- Source anchors: `native-dispatch-runner.contract.json` scenario `failure-withholding`; `EXECUTION-PACK.md` G4.
- Related context: `DESIGN.md` failure sequence.
- Attempt state: the root `failure/` evidence is blocked attempt 1 and remains byte-preserved.
- Retry write scope: `formulae/dispatch-spec/development/runtime-integration/native-dispatch-runner-canary/failure/retry-001/` only.
- Retry rule: regenerate the isolated installed runtime from repaired canonical source; link attempt 1 instead of replacing it.
- Done criteria: command entry is recorded; first-wave native agent identifier exists; non-pass receipt exists; gate blocks; dependent native spawn count is zero; the full terminal lifecycle stream validates; retry evidence links the blocked attempt.
- Acceptance evidence: retry source dispatch, live lifecycle events, native receipt, gate decision, result, closeout validation, and immutable attempt-1 hashes.
- Validation: canonical Dispatch Spec validator plus native run-evidence validator.
- Handoff: only a passing retry unlocks `SWU-NDR-012`; fail/block forbids the success run.

## SWU-NDR-012 — Run the success-progression canary

- Behavior: invoke only `orchestrate execute <dispatch.json>` on the matching passing fixture and prove the dependent role spawns exactly once after the gate opens.
- Split analysis: success progression is separate because it relies on, but must not mask, failure withholding.
- Dependencies: passing `SWU-NDR-011` retry receipt; a blocked or absent retry receipt forbids execution.
- Source anchors: `native-dispatch-runner.contract.json` scenario `success-progression`; `EXECUTION-PACK.md` G5.
- Related context: `DESIGN.md` success sequence.
- Write scope: `formulae/dispatch-spec/development/runtime-integration/native-dispatch-runner-canary/success/` only.
- Done criteria: first-wave pass receipt precedes `gate_pass`; dependent action is compiled afterward; dependent role has one native agent identifier and one terminal receipt; closeout validates.
- Acceptance evidence: source dispatch, live events, both native receipts, gate decision, exact spawn counts, result, closeout validation.
- Validation: canonical Dispatch Spec validator plus native run-evidence validator.
- Handoff: pass unlocks `SWU-NDR-013` and closure verification.

## SWU-NDR-013 — Adjudicate historical canary proof

- Behavior: add an immutable correction that classifies the earlier manually driven canary as host-tool evidence rather than automatic dispatch integration proof, and link the new causal canary.
- Split analysis: truth-status correction is one documentation/evidence behavior after replacement proof exists; original files remain unchanged.
- Dependencies: `SWU-NDR-012` pass receipt.
- Source anchors: `formulae/dispatch-spec/development/runtime-integration/20260722T063407Z-native-host-canary/result.json`; new failure and success canary results; `CAPABILITY-BOUND-DELEGATION.md` proof status.
- Related context: `DEFINE.md` acceptance boundary.
- Write scope: `formulae/dispatch-spec/development/runtime-integration/20260722T063407Z-native-host-canary/adjudication.json`, `formulae/dispatch-spec/CAPABILITY-BOUND-DELEGATION.md`, new canary summary.
- Done criteria: historical records are byte-preserved; adjudication states the original proof limit; capability status cites the new causal evidence without claiming cross-host parity.
- Acceptance evidence: before hashes for historical files, adjudication, updated bounded status, links to new validator receipts.
- Validation: JSON parse, concrete-path existence, historical hash comparison, public-boundary scan.
- Handoff: pass unlocks `TASK-NDR-VERIFY` closure-only recomposition.
