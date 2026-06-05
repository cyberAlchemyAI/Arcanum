# Experiment Harness: loop

<!-- arcanum:capability-id experiment-harness -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command experiment-loop -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-experiment-loop-<UTC timestamp>`.
- `capability.id`: `experiment-harness`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run Experiment Harness in `loop` mode.

## Command Shape

```text
/experiment-loop <artifact-path> <regime-id>
```

## Process

1. Resolve the target artifact path.
2. Use the installed `experiment-harness` command contract as the authoritative behavior source.
3. Run or explain the equivalent script operation for `loop` mode.
4. Preserve profile metadata, validation fields, observability rules, and live-loop budget gates.
5. Return artifact used, mode, command or script path, validation result, observation result, and next action.

## Guardrails

- Keep this adapter focused on Experiment Harness `loop` mode.
- Do not bypass `development/EXPERIMENT-PROFILE.md` validation.
- Do not run live Codex loops unless the user explicitly approved the live-loop budget.
