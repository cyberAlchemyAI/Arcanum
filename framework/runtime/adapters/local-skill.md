# Runtime Adapter: local-skill

## Identity

| Field | Value |
| --- | --- |
| `adapter_id` | `local-skill` |
| `runtime_kind` | `native-agent-skill-surface` |
| `execution_mode` | parent-orchestrated handoff |
| `state_model` | current session and native subagents |
| `isolation_model` | no nested model CLI |

## Purpose

`local-skill` is the default non-nested Arcanum runtime adapter. It represents execution by the active agent host through native skills, instructions, and subagents rather than by spawning a second model-backed CLI process.

This adapter is intentionally a handoff/receipt contract. A shell command cannot start a native Codex, Claude, or Copilot subagent by itself. The parent agent surface owns stage execution and returns the receipt.

## Output Contract

The parent runner must return:

- run id or dispatch id,
- step id or command name,
- capability reference,
- execution surface,
- status,
- artifact paths,
- validation result,
- observability status or returned telemetry receipt,
- blockers,
- handoff note.

## Validation

Useful checks:

```bash
tools/arcanum --resolve-adapter local-skill
tools/arcanum --exec --adapter local-skill --output /tmp/arcanum-local-skill-output.md invoke "define runtime smoke"
```

## Boundary

`local-skill` must not spawn nested model-backed CLI processes. Use `codex-exec` only as an explicit legacy adapter compatibility test.
