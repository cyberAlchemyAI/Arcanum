# Context Pack — SWU-NDR-001

Status: pass

Mode: lean, strict obligation mapping

Session evidence: this pack controls one local Task Session execution. It is not canonical design authority.

## Task

Compile one validator-passing capability-bound dispatch in `prepared` state into the exact dependency-free first-wave action set and initialized run state. Receipt reduction and host-native execution are out of scope.

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Run the canonical Dispatch Spec validator before compilation and emit no actions unless validation is `pass`. | validator `main`/`validate`; contract invariants | covered |
| O2 | Compile only the earliest declared wave whose dependencies are empty at initial state. | execution-wave schema; canary source dispatch | covered |
| O3 | Bind every action to dispatch, run, wave, role, capability, target, mode, step, and write scope with stable ordering. | task done criteria; capability-bound role fields | covered |
| O4 | Initialize deterministic `state.json` and `run-plan.json` data without host calls or time-dependent fields. | contract states/actions; L0 boundary | covered |
| O5 | Preserve authorization and validator/executor boundaries. | contract authority/invariants; architecture decisions | covered |
| O6 | Validate invalid input, dependency filtering, agent cardinality, and stable output. | task validation contract | covered |
| O7 | Write only coordinator, schemas, compile fixtures/tests, and this Task Session evidence. | task write scope; work-pack rules | covered |
| O8 | Return a machine Task Session receipt and name only `SWU-NDR-002` as the next unit. | task handoff; work-pack dependency row | covered |

## Selected Evidence

| Source | Selector | Obligations | Why included |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-NDR-001.md` | SWU-NDR-001 lines 7–18 | O1–O8 | Exact task, scope, criteria, validation, handoff. |
| `native-dispatch-runner.contract.json` | authority, invariants, components, states/actions | O1, O3–O5 | Strongest proposed machine behavior source. |
| `ARCHITECTURE.json` | modules, dependency/failure rules, decisions | O1, O4, O5 | Preserves validator/coordinator boundary. |
| `IMPLEMENTATION-LAYERING.md` | L0 and First Unit | O2, O4–O6 | Restricts this SWU to deterministic coordination. |
| `WORK-PACK.md` | authority, rules, task row, first handoff | O7, O8 | Governs sequencing and evidence. |
| `formulae/dispatch-spec/dispatch.schema.yml` | dispatch required fields, capability-bound roles/waves, steps | O1–O3 | Defines accepted route shape. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | `validate`, capability-bound validation, `main` | O1–O3, O6 | Canonical validation behavior and CLI. |
| `runtime-integration/20260722T063407Z-native-host-canary/failure/source.dispatch.json` | subagent strategy roles and waves | O2, O3, O6 | Existing validator-passing two-wave example; fixture seed only, not integration proof. |

## Architecture Guidance

- The coordinator is deterministic and may invoke the deterministic validator.
- It does not spawn, wait for, join, or close agents.
- The first action set comes from the first declared dependency-free wave only; dependent waves remain absent.
- A `spawn` action represents one agent instance. `agent_count` therefore expands deterministically by role order and zero-based instance ordinal.
- `step_id` is the first declared applied step and the complete binding remains in `applies_to_steps`, so action receipts have a stable primary step without discarding multi-step context.
- Authorization is satisfied only for `approved` or `not_needed`; all other values block with zero actions.
- Stable output excludes wall-clock timestamps and random identifiers; `run_id` is caller-supplied.

## Write Scope

- `runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- `runtime/orchestrate/schemas/`
- `runtime/orchestrate/tests/fixtures/compile/`
- `runtime/orchestrate/tests/test_compile_actions.py`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-001/`

## Non-goals

- receipt reduction;
- gate evaluation after a wave;
- native host operations;
- generated skill installation;
- canary reclassification;
- lifecycle promotion.

## Validation Surface

```text
python3 -m unittest runtime/orchestrate/tests/test_compile_actions.py
python3 runtime/orchestrate/scripts/native_dispatch_coordinator.py compile <fixture> --run-id <id> --output-dir <temporary-dir>
python3 formulae/dispatch-spec/scripts/validate-dispatch.py <fixture> --json
```

## Gaps and Resolutions

- Task prose says one action per eligible role while the schema permits `agent_count > 1` and the machine contract defines one native agent per spawn action. Resolution: compile one action per role instance. This preserves exact cardinality and the stronger machine invariant; the Task Session receipt records the interpretation.
- A role may apply to multiple steps while the receipt contract names a singular `step_id`. Resolution for L0: use the first declared applied step as the stable primary `step_id` and preserve the complete `applies_to_steps` array. Later receipt binding remains outside this SWU.

No blocker remains for local implementation.

## Provenance

- Source revision: `b652e06a1571da602691436766b6beedb073e887`
- Built: `2026-07-22T14:39:02Z`
- Source digests: recorded in `context-pack.json`
