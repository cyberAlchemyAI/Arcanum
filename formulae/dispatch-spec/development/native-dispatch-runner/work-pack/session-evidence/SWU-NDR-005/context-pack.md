# Context Pack — SWU-NDR-005

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one local Task Session. It is not reusable design authority.

## Task

Join every known native agent in one compiled wave, normalize each bounded result into the canonical action receipt, close completed or unresolved agents under policy, and pass the complete receipt set to the deterministic reducer without changing the reducer's gate decision.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Accept only the complete action-to-agent bindings for one persisted wave. | covered |
| O2 | Wait for each known native identifier exactly once. | covered |
| O3 | Bind each result to its declared action, role, step, wave, capability, run, and native agent identity. | covered |
| O4 | Treat terminal completion as closed; interrupt an unresolved known agent at most once under incomplete policy. | covered |
| O5 | Give the reducer one receipt per expected action, including an explicit timed-out receipt for a missing result. | covered |
| O6 | Return exactly the state, gate decision, and next action set emitted by the deterministic reducer. | covered |
| O7 | A non-pass result, missing result, or identity mismatch must produce a blocking gate. | covered |
| O8 | Append wait and terminal/interrupt events at the host-action boundary. | covered |
| O9 | Exclude multi-wave progression, generation, and full native canaries from this SWU. | covered |
| O10 | Restrict mutation to canonical join contracts, join tests, and Task Session evidence. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-002.md` | SWU-NDR-005 | O1–O10 |
| `work-pack/session-evidence/SWU-NDR-004/receipt.json` | pass dependency and native identifier binding | O1, O2, O10 |
| `native-dispatch-runner.contract.json` | actions, receipt requirements, invariants | O1–O9 |
| `ARCHITECTURE.json` | reducer boundary and failure rule | O3–O7 |
| `DESIGN.md` | join sequence, evidence view, partial-spawn control | O2–O9 |
| `work-pack/shared/context.md` | shared execution constraints | O1–O10 |
| `runtime/orchestrate/SKILL.md` | current native execution contract | O1–O4, O8, O9 |
| `runtime/orchestrate/hosts/codex-native.md` | wait, interrupt, and inventory mappings | O2, O4, O8 |
| `runtime/orchestrate/schemas/receipt.schema.json` | canonical normalized receipt | O3, O5, O7 |
| `runtime/orchestrate/scripts/native_dispatch_coordinator.py` and `tests/test_reduce_receipts.py` | reducer interface and exact gate behavior | O5–O7 |

## Decisions

1. Use deterministic host stubs for join edge cases; live end-to-end host behavior remains the two later canaries.
2. A completed host result closes that known identifier logically; a missing result emits `wait_timed_out`, invokes interrupt once, and produces a canonical `timed_out` receipt.
3. Normalize results against the persisted action and known agent binding. Any identity mismatch becomes a blocking receipt for the expected action rather than being trusted.
4. Give the complete normalized receipt set to the existing coordinator reducer and compare returned gate artifacts byte-for-structure with reducer output.

## Write Scope

- `runtime/orchestrate/SKILL.md`
- `runtime/orchestrate/hosts/codex-native.md`
- `runtime/orchestrate/tests/native-join/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-005/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

## Validation Surface

- all-pass join;
- one-agent failure;
- missing result with one interrupt and explicit timed-out receipt;
- result identity mismatch;
- exactly-once wait/close accounting;
- canonical receipt-schema validation;
- reducer input completeness and exact gate return;
- all earlier compiler, reducer, preflight, and spawn tests;
- public-boundary and JSON/YAML checks.

No blocker remains. Cross-wave execution and live failure/success canaries stay outside this SWU.

## Provenance

- Built: `2026-07-22T15:16:20Z`
- Source digests: `context-pack.json`
