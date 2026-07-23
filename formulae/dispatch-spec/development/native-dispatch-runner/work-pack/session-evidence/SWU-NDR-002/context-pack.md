# Context Pack — SWU-NDR-002

Status: pass

Mode: lean, strict obligation mapping

Session evidence: this pack controls one local Task Session execution. It is not canonical design authority.

## Task

Reduce one completed wave's action-bound receipts into exactly one deterministic `gate_pass` or `gate_block`. A passing gate compiles the next eligible wave; a blocking gate emits no dependent actions. Host joining remains out of scope.

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Consume the exact SWU-NDR-001 state/run plan and preserve dispatch/run identity. | SWU-NDR-001 receipt; coordinator and expected run plan | covered |
| O2 | Require one structurally valid receipt for every current action. | machine receipt requirements; NDR-R5 trace | covered |
| O3 | Match action, dispatch, run, wave, step, role, and capability identity. | contract receipt requirements; current action fields | covered |
| O4 | Pass only when every required receipt has `status=pass`, `validation=pass`, and no blockers. | architecture gate expression/failure rule | covered |
| O5 | On pass, compile only the earliest now-eligible dependent wave. | source dispatch waves; coordinator ordering | covered |
| O6 | On any missing, malformed, duplicate, unexpected, mismatched, or non-pass receipt, emit `gate_block` and zero next actions. | architecture failure rule; task done criteria | covered |
| O7 | Produce byte-stable state, gate decision, and next-action set for identical input. | task replay criterion; deterministic L0 boundary | covered |
| O8 | Keep writes to reducer code/schemas/fixtures/tests plus Task Session evidence and manifest synchronization. | task write scope and Task Session contract | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-001.md` | SWU-NDR-002 lines 20–31 | O1–O8 |
| `native-dispatch-runner.contract.json` | states, actions, receipt requirements | O2–O4, O6 |
| `ARCHITECTURE.json` | gate expression and failure rule | O4–O6 |
| `work-pack/shared/traceability.md` | NDR-R5/R6 | O2, O3, O6 |
| `work-pack/session-evidence/SWU-NDR-001/receipt.json` | pass status and handoff | O1, O8 |
| `runtime/orchestrate/scripts/native_dispatch_coordinator.py` | compiled action/state/run-plan shape | O1, O3, O5, O7 |
| `runtime/orchestrate/tests/fixtures/compile/valid-two-wave.json` | roles, waves, dependencies, gate | O3–O6 |
| `runtime/orchestrate/tests/fixtures/compile/expected-run-plan.json` | exact first-wave action bindings | O1–O3, O7 |

## Decisions

- Receipt admission uses one receipt per `action_id`; action identity is the primary join key.
- The internal reducer receipt uses scalar `validation: pass|fail|block`, matching the architecture gate expression. Prior narrative validation arrays are historical evidence, not this runtime contract.
- A blocking gate is a successful reducer outcome, not a process crash.
- Next action identifiers continue the current run sequence, so a three-action first wave yields `spawn-0004` for the dependent role.
- The reducer emits no timestamps; receipt timestamps remain inputs and identical inputs produce identical output bytes.

## Write Scope

- `runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- `runtime/orchestrate/schemas/`
- `runtime/orchestrate/tests/fixtures/reduce/`
- `runtime/orchestrate/tests/test_reduce_receipts.py`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-002/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` synchronization only

## Validation Surface

```text
python3 -m unittest runtime/orchestrate/tests/test_compile_actions.py runtime/orchestrate/tests/test_reduce_receipts.py
python3 runtime/orchestrate/scripts/native_dispatch_coordinator.py reduce <dispatch> --state <state> --run-plan <plan> --receipts-dir <dir> --output-dir <dir>
python3 -m json.tool <schemas, fixtures, and evidence>
```

## Non-goals

- spawning, waiting for, joining, or closing native agents;
- live event recording;
- authorization preflight changes;
- generated skill installation.

No blocker remains for deterministic implementation.

## Provenance

- Built: `2026-07-22T14:54:18Z`
- Source digests: `context-pack.json`
