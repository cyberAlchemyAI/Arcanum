# TASK-NDR-001 — Deterministic Coordinator

Owner: Task Session

Objective: compile permitted actions and reduce bound receipts without host-native side effects.

## SWU-NDR-001 — Compile the first eligible action set

- Behavior: given one validator-passing dispatch in `prepared` state, emit the exact dependency-free first-wave action set and initialized run state.
- Split analysis: action compilation is independently testable; receipt reduction and host execution are excluded.
- Dependencies: none.
- Source anchors: `native-dispatch-runner.contract.json` components/invariants; `ARCHITECTURE.json` modules; `formulae/dispatch-spec/dispatch.schema.yml`; `formulae/dispatch-spec/scripts/validate-dispatch.py`.
- Related context: `work-pack/shared/context.md`; `IMPLEMENTATION-LAYERING.md` L0.
- Write scope: `runtime/orchestrate/scripts/native_dispatch_coordinator.py`, `runtime/orchestrate/schemas/`, `runtime/orchestrate/tests/fixtures/compile/`, `runtime/orchestrate/tests/test_compile_actions.py`.
- Done criteria: invalid input emits no actions; valid input emits one action per eligible role with exact dispatch/run/wave/step/role/capability/target/mode/write-scope fields; output order is stable.
- Acceptance evidence: validator receipt, initialized `state.json`, expected/actual `run-plan.json`, compile fixture results.
- Validation: deterministic tests covering invalid dispatch, dependency filtering, exact role cardinality, and stable output.
- Handoff: pass receipt unlocks `SWU-NDR-002`; fail/block returns to this SWU only.

## SWU-NDR-002 — Reduce wave receipts into one gate decision

- Behavior: given compiled actions and bound receipts for one completed wave, emit exactly one `gate_pass` with next eligible actions or `gate_block` with no dependent actions.
- Split analysis: gate reduction is separate from action compilation because its acceptance input is a closed receipt set; host joining is excluded.
- Dependencies: `SWU-NDR-001` pass receipt.
- Source anchors: `native-dispatch-runner.contract.json` states/actions/receipt requirements; `ARCHITECTURE.json` gate expression and failure rule.
- Related context: `work-pack/shared/traceability.md` NDR-R5/R6.
- Write scope: `runtime/orchestrate/scripts/native_dispatch_coordinator.py`, `runtime/orchestrate/schemas/`, `runtime/orchestrate/tests/fixtures/reduce/`, `runtime/orchestrate/tests/test_reduce_receipts.py`.
- Done criteria: all required passing receipts open the declared next wave; any missing, mismatched, malformed, or non-pass required receipt blocks; reducer is idempotent for the same state and receipts.
- Acceptance evidence: expected/actual gate decisions, next-action set or empty set, reducer fixture results.
- Validation: deterministic pass, non-pass, missing, identity-mismatch, and replay fixtures.
- Handoff: a passing L0 gate unlocks `TASK-NDR-002`.
