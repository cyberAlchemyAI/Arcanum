# Arcanum Runtime Adapter: runtime-handoff

<!-- arcanum:capability-id runtime-handoff -->
<!-- arcanum:capability-kind runtime-adapter -->
<!-- arcanum:capability-tier runtime -->
<!-- arcanum:command runtime-handoff -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-runtime-handoff-<UTC timestamp>`.
- `capability.id`: `runtime-handoff`
- `capability.kind`: `runtime-adapter`
- `capability.tier`: `runtime`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the selected task/SWU, handoff pack, and runtime adapter request.
- expected outputs: list intended handoff, receipt, or blocked-runtime artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.

## Objective

Expose the repository-local runtime handoff contract used by Task Session and Refine.

## Canonical Sources

- Adapter contract: `arcana/task-session/runtime-adapters/runtime-handoff.md`
- Refine template: `arcana/refine/templates/runtime-handoff.md`
- Runtime template: `framework/runtime/templates/RUNTIME-HANDOFF.md`
- Runtime command surface: `tools/arcanum`

## Process

1. Read `arcana/task-session/runtime-adapters/runtime-handoff.md` before executing.
2. Treat the user request as a selected task/SWU runtime handoff, runtime-contract review, or blocked-field diagnosis.
3. Confirm the required handoff fields exist:
   - selected work-pack task or SWU,
   - bounded write scope,
   - done criteria,
   - validation evidence,
   - Context Builder handoff pack and JSON/index when delegating,
   - strict coverage status,
   - selected runtime adapter.
4. If strict runtime delegation is requested and any required field is missing, return `BLOCK` with the smallest unblock action.
5. If the request is only a contract review, report whether the handoff is runnable, flagged, or blocked.

## Guardrails

- This route exposes and validates runtime handoff contracts; it does not implement every runtime adapter.
- Native adapters produce handoff/receipt contracts and must not spawn nested model-backed CLIs.
- Legacy model CLI adapters require explicit operator selection.
- Do not mark delegated execution complete until returned runtime evidence is reviewed by Task Session.
- Do not mutate Task Session, Refine, or adapter internals from this command route unless an explicit work-pack task authorizes that scope.
