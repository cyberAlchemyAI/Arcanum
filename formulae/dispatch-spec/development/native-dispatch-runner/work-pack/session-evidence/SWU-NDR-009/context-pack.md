# Context Pack — SWU-NDR-009

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one local Task Session. It is not reusable design authority.

## Task

Prove that when one action in a compiled wave spawns successfully and the next spawn fails, the driver stops before remaining actions, reconciles every known native identifier, records residue, and returns blocked with no dependent actions.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Consume compiled wave actions in deterministic order. | covered |
| O2 | After the first spawn failure, perform no further spawn action. | covered |
| O3 | Preserve every native identifier returned before the failure. | covered |
| O4 | Register and wait/reconcile every known identifier exactly once. | covered |
| O5 | Interrupt each unresolved known identifier at most once and record a terminal event. | covered |
| O6 | Persist a blocked result with explicit partial-wave residue. | covered |
| O7 | Emit no dependent action identifiers or actions. | covered |
| O8 | Preserve causal event order for attempts, return/failure, registration, wait, and interrupt. | covered |
| O9 | Add host-stub tests only when existing spawn/join/failure contracts already compose correctly. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-004.md` | SWU-NDR-009 | O1–O9 |
| `work-pack/session-evidence/SWU-NDR-008/receipt.json` | dependency pass and no-dependent invariant | O2, O6, O7 |
| `EXECUTION-PACK.md` | recovery rule | O2–O8 |
| `DESIGN.md` | partial-spawn risk/control | O2–O8 |
| `runtime/orchestrate/SKILL.md` | spawn failure and join recovery contracts | O1–O8 |
| `runtime/orchestrate/hosts/codex-native.md` | spawn, mailbox wait, inventory, interrupt mappings | O3–O5, O8 |
| `runtime/orchestrate/tests/fixtures/compile/expected-run-plan.json` | three compiled actions | O1, O2, O7 |
| `runtime/orchestrate/tests/native-spawn/test_native_spawn_contract.py` | one-call and host-error semantics | O1–O3, O8 |
| `runtime/orchestrate/tests/native-join/test_native_join_contract.py` | pending-set and bounded interrupt semantics | O3–O5, O8 |

## Decisions

1. Compose the already-proven spawn and join rules in a deterministic host-stub partial-wave harness; do not alter canonical runtime contracts unless the composition fails.
2. Use the three-action compiled fixture: spawn 0001 succeeds, spawn 0002 fails, and spawn 0003 must never be attempted.
3. Model the successful sibling as unresolved during cleanup so the fixture exercises one mailbox wait and one interrupt.
4. Require a terminal event for the known agent and a residue object binding it to its action.
5. Add excluded tests/evidence only so installed generated packages retain zero drift.

## Write Scope

- `runtime/orchestrate/tests/partial-wave/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-009/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

The task allows skill/host changes, but the current contracts already express every required transition.

## Validation Surface

- exact ordered host-call/event trace;
- spawn call count equals two for a three-action wave;
- third action absent from attempts;
- one known native identifier registered and reconciled;
- one interrupt for the unresolved identifier;
- blocked result with explicit residue;
- zero dependent actions;
- all earlier regressions;
- generated selected-support drift remains zero.

No blocker remains. Causal event-stream validation remains SWU-NDR-010.

## Provenance

- Built: `2026-07-22T15:35:44Z`
- Source digests: `context-pack.json`
