# Observed Runs

Observed runs make sigil and spell execution recoverable in long sessions.

The stable source of truth is an Arcanum run bundle, not private runtime session storage. Runtimes may enrich a bundle when they expose structured data, but the bundle must remain useful without platform internals.

## Run Bundle Layout

```text
.arcanum/observability/runs/<session-id>/<run-id>/
  envelope.json
  events.jsonl
  checkpoints/
    <timestamp>.json
  final-output.md
  observer-output.json
```

## Lifecycle States

- `opened`
- `checkpointed`
- `closing`
- `closed`
- `interrupted`
- `stale`

## Checkpoint Event

Long-running work should checkpoint after meaningful phases, tool-heavy work, validation, interruption, or context transitions.

Each checkpoint captures:

- phase summary,
- tools used summary,
- files touched,
- decisions made,
- validation state,
- blockers,
- next intended step.

## Observation Fallback

If a close boundary exists, observe the closed bundle.

If close data is missing, observe the latest checkpoint and emit capability telemetry with status `partial` or `interrupted`. The recommendation should be `resume-or-reflect`.

Use `scripts/observe-run-with-codex.sh` only as an explicit legacy Codex observer when Codex CLI is available and a bounded AI observer is desired. Native agent/subagent routes should return the observer fields in their receipt. The script reads only the run bundle and writes `observer-output.json`.

## Runtime Policy

Installed `arcanum-sigil-*` and `arcanum-spell-*` commands should eventually use this wrapper flow:

```text
start observed run
execute command inline or via runtime
checkpoint at meaningful phase boundaries
finish observed run
dispatch observer hook
append telemetry
```

Subagents are optional. The boundary is the run bundle.
