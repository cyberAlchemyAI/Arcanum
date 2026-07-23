# TASK-NDR-002 — Native Orchestrate Driver

Owner: Task Session

Objective: make `orchestrate execute` perform coordinator-emitted actions through one host's native subagent operations.

## SWU-NDR-003 — Add execute grammar and preflight

- Behavior: recognize `orchestrate execute <dispatch.json>`, validate the route, resolve execution authorization, and verify native host operations before asking for actions.
- Split analysis: preflight is independently acceptable because it must block safely without spawning; actual native calls are excluded.
- Dependencies: `SWU-NDR-002` pass receipt.
- Source anchors: `runtime/orchestrate/` proposed architecture; `formulae/dispatch-spec/SKILL.md`; `development/craft/ARCANUM-SKILL-RUNTIME-HANDOFF.md` native adapter limitation.
- Related context: `DEFINE.md` NDR-R1/R2; `DESIGN.md` authority contracts.
- Write scope: `runtime/orchestrate/SKILL.md`, `runtime/orchestrate/hosts/codex-native.md`, `runtime/orchestrate/tests/preflight/`.
- Done criteria: invalid dispatch, missing authorization, or unavailable host capability produces a blocked receipt and zero spawn actions; valid authorized input reaches `wave_ready`.
- Acceptance evidence: preflight receipts and zero-spawn assertions for every blocked fixture.
- Validation: invoke grammar, validation failure, authorization pending, missing-host-tool, and ready fixtures.
- Handoff: pass unlocks `SWU-NDR-004`.

## SWU-NDR-004 — Execute one native spawn action

- Behavior: map one coordinator-emitted `spawn` action to exactly one native host spawn operation and record the action attempt plus returned agent identifier.
- Split analysis: one spawn mapping is the smallest causal host slice; waiting, joining, and gate reduction are excluded.
- Dependencies: `SWU-NDR-003` pass receipt.
- Source anchors: `native-dispatch-runner.contract.json` actions/invariants; `DESIGN.md` runtime sequence and evidence view.
- Related context: `work-pack/shared/traceability.md` NDR-R4/R7.
- Write scope: `runtime/orchestrate/SKILL.md`, `runtime/orchestrate/hosts/codex-native.md`, `runtime/orchestrate/tests/native-spawn/`.
- Done criteria: a spawn event is persisted at attempt time; the host is called exactly once with bounded role context; the returned agent identifier is bound to the action; no uncompiled action can run.
- Acceptance evidence: ordered action/event files, host-call count, returned agent identifier, native spawn receipt.
- Validation: one-action pass, duplicate/replay rejection, unknown-action rejection, and host-error block cases.
- Handoff: pass unlocks `SWU-NDR-005`.

## SWU-NDR-005 — Join one wave and return receipts to the reducer

- Behavior: wait for all known agents in a wave, normalize their bounded results, close them under join policy, and feed the receipt set to the deterministic reducer.
- Split analysis: joining is one behavior boundary after spawn; multi-wave progression is proven later by canaries.
- Dependencies: `SWU-NDR-004` pass receipt.
- Source anchors: `native-dispatch-runner.contract.json` receipt requirements; `ARCHITECTURE.json` failure rule; `DESIGN.md` native execution boundary.
- Related context: `work-pack/shared/context.md`.
- Write scope: `runtime/orchestrate/SKILL.md`, `runtime/orchestrate/hosts/codex-native.md`, `runtime/orchestrate/tests/native-join/`.
- Done criteria: every known agent is waited/closed exactly once; results are bound to declared identities; the reducer receives a complete receipt set or an explicit missing receipt; returned gate matches reducer output.
- Acceptance evidence: wait/close event sequence, normalized receipts, reducer input, gate decision.
- Validation: all-pass join, one-agent failure, missing result, and identity mismatch cases.
- Handoff: pass establishes the L1 runtime dependency for `TASK-NDR-003` and `TASK-NDR-004`.
