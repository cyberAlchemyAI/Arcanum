# Context Pack — SWU-NDR-003

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one local Task Session. It is not reusable design authority.

## Task

Add the exact `orchestrate execute <dispatch.json>` grammar and a host-native preflight that validates the dispatch, resolves execution authorization, verifies required Codex native operations, and reaches `wave_ready` without spawning.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Recognize exactly one execute verb and dispatch path. | covered |
| O2 | Require canonical Dispatch Spec result `pass` before compilation. | covered |
| O3 | Treat only `approved` and `not_needed` as satisfied execution authorization. | covered |
| O4 | Verify required native host operations from the active host tool catalog. | covered |
| O5 | Invalid route, pending/blocked authorization, or missing host operation returns block with zero spawn attempts. | covered |
| O6 | Valid authorized input with all host operations compiles to `wave_ready`. | covered |
| O7 | Never replace absent native tools with shell or nested model-backed CLI execution. | covered |
| O8 | Restrict mutation to canonical Orchestrate skill/host contract, preflight tests, and Task Session evidence. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-002.md` | SWU-NDR-003 | O1–O8 |
| `work-pack/session-evidence/SWU-NDR-002/receipt.json` | pass status and next route | O8 |
| `native-dispatch-runner.contract.json` | authority and invariants | O2–O7 |
| `ARCHITECTURE.json` | entry points, modules, failure rule | O1–O7 |
| `DEFINE.md` | NDR-R1/R2/R4 | O2–O6 |
| `DESIGN.md` | native driver boundary and runtime sequence | O4–O7 |
| `formulae/dispatch-spec/SKILL.md` | validator and non-execution boundary | O2, O3, O7 |
| `development/craft/ARCANUM-SKILL-RUNTIME-HANDOFF.md` | parent runtime and adapter constraints | O4, O7 |
| `.arcanum/runtime/adapters/native-skill.json` | parent-orchestrated, non-shell limitation | O4, O7 |

## Decisions

1. `runtime/orchestrate/SKILL.md` carries a machine-readable YAML execute/preflight contract because it is the host-native executable skill source.
2. `hosts/codex-native.md` maps abstract operations to current Codex native tool identities; the active host catalog, not a shell probe, decides availability.
3. Preflight has a hard zero-spawn invariant. It may call the deterministic validator/coordinator but never a host operation.
4. Required Codex operations are `collaboration.spawn_agent`, `collaboration.wait_agent`, `collaboration.interrupt_agent`, and `collaboration.list_agents`; message delivery is optional for the first spawn/join path.

## Active Host Evidence

The current runtime exposes all four required Codex operations through its native collaboration tool surface. This is availability evidence only; no native action is called in SWU-NDR-003.

## Write Scope

- `runtime/orchestrate/SKILL.md`
- `runtime/orchestrate/hosts/codex-native.md`
- `runtime/orchestrate/tests/preflight/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-003/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

## Validation Surface

- contract parsing and exact grammar test;
- invalid dispatch fixture;
- authorization-pending fixture;
- missing-host-operation fixture;
- ready fixture using the deterministic coordinator;
- zero-spawn assertion for every preflight result;
- public-boundary and JSON/YAML parsing checks.

No blocker remains. Actual native spawning belongs only to SWU-NDR-004.

## Provenance

- Built: `2026-07-22T15:01:57Z`
- Source digests: `context-pack.json`
