# Context Pack — SWU-NDR-004

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one Task Session and one bounded native proof agent. It is not reusable design authority.

## Task

Consume one persisted coordinator-shaped `spawn` action, record its attempt before the host call, invoke the mapped Codex native spawn operation exactly once with bounded role context, and bind the returned agent identifier to that action.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Consume one persisted action that validates against the canonical action schema. | covered |
| O2 | Reject unknown or non-persisted action identifiers before any host call. | covered |
| O3 | Append `action_attempted` before calling the host-native spawn operation. | covered |
| O4 | Call the mapped host operation exactly once for the selected action. | covered |
| O5 | Bound child context by role, capability, target, mode, mutation policy, scopes, inputs, and outputs. | covered |
| O6 | Append the returned native agent identifier and bind it to the action identifier. | covered |
| O7 | Block duplicate/replay attempts and record a blocking host-error event when spawn fails. | covered |
| O8 | Join the proof helper only for Task Session lifecycle hygiene; product wave joining remains SWU-NDR-005. | covered |
| O9 | Restrict product writes to the SWU write scope and session evidence. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-002.md` | SWU-NDR-004 | O1–O9 |
| `work-pack/session-evidence/SWU-NDR-003/receipt.json` | pass dependency and handoff | O1, O9 |
| `work-pack/session-evidence/SWU-NDR-003/active-host-capability-check.json` | active native operation availability | O3, O4, O6, O8 |
| `native-dispatch-runner.contract.json` | actions, evidence invariants, non-goals | O1–O8 |
| `DESIGN.md` | native driver, causal event, and risk controls | O1–O8 |
| `work-pack/shared/traceability.md` | NDR-R4 and NDR-R7 | O3, O4, O6 |
| `runtime/orchestrate/SKILL.md` | current execution boundary | O1–O4, O7 |
| `runtime/orchestrate/hosts/codex-native.md` | Codex operation mapping | O3–O8 |
| `runtime/orchestrate/schemas/action.schema.json` | canonical action shape | O1, O2, O5 |

## Decisions

1. Use a dedicated read-only action fixture so the native proof cannot mutate repository files.
2. Treat the persisted action file plus its identifier as the admission registry; an absent or already-attempted identifier blocks before spawn.
3. Persist append-only JSONL events around the live host call: `action_attempted` first, then `host_spawn_returned` or `host_spawn_failed`.
4. The proof helper receives the exact bounded action context and may only return an acknowledgement.
5. Wait for the helper only to satisfy Task Session subagent closeout. Do not claim that as the product wave-join implementation.

## Active Host Evidence

The current runtime exposes `collaboration.spawn_agent`, `collaboration.wait_agent`, `collaboration.interrupt_agent`, and `collaboration.list_agents`. SWU-NDR-003 proved availability without spawning; this SWU must supply the first causal host-call proof.

## Write Scope

- `runtime/orchestrate/SKILL.md`
- `runtime/orchestrate/hosts/codex-native.md`
- `runtime/orchestrate/tests/native-spawn/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-004/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

## Validation Surface

- one admitted action produces one host request;
- duplicate/replay rejection before host call;
- unknown action rejection before host call;
- host error produces a blocking event/receipt;
- live event order proves attempt-before-spawn-return;
- one returned native agent identifier is bound to the action;
- the proof helper completes with no file mutation and no open subagent residue;
- public-boundary and JSON/YAML parsing checks.

No blocker remains. Wave waiting, receipt normalization, and reducer feedback belong only to SWU-NDR-005.

## Provenance

- Built: `2026-07-22T15:09:31Z`
- Source digests: `context-pack.json`
