# Stage 2: Invoke Define

## Verdict

`pass`

## Definition

Arcanum needs a **Durable Runtime Interface**: a generic execution substrate that can receive bounded work from orchestrators, preserve intent and state in files, run adapters, and return auditable artifacts.

## Core Problem

The current system conflates four things:

1. command resolution,
2. stage orchestration,
3. runtime handoff,
4. Codex execution.

This works for simple command prompts, but breaks when refine or task-session need durable multi-stage execution, nested execution, resumability, or clean blocked status.

## Defined Architecture

```text
orchestrator
  -> async task handoff
  -> runtime translator
  -> runtime executor
  -> adapter
```

## Definitions

- **Orchestrator**: decides the workflow shape and owns final synthesis.
- **Async task handoff**: durable, immutable request package.
- **Runtime translator**: converts generic handoff to adapter-specific input.
- **Runtime executor**: owns run lifecycle, status, events, result capture, and adapter invocation.
- **Adapter**: concrete execution mechanism, such as `codex-exec` or `dry-run`.

## Design Goal

Make runtime execution generic enough that refine loops, task-session tasks, and future Arcanum workflows all use the same substrate.
