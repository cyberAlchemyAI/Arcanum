# Runtime Handoff

## Runtime Boundary

- Runtime: `arcanum-runtime`
- Adapter: `codex-exec`
- Owner: `refine`
- Status: block
- Runtime run folder: blocked for current run

## Runtime Objective

Run the canonical Refine loop for `arcana/x-ray` and produce `RESULT.md`.

## Stage Dispatch Contract

```bash
tools/arcanum --exec --output STAGE_OUTPUT COMMAND STAGE_REQUEST
```

Before each command-backed stage:

```bash
tools/arcanum --resolve COMMAND
```

## Handoff Status

- Context Builder handoff pack: blocked for current run
- Handoff index: blocked for current run
- Strict coverage: block for current run
- Runtime adapter profile: blocked for current run
- Runtime status: block
- Blocked reason: the runtime-backed command loop did not produce current-run stage artifacts, so Refine did not dispatch the command-backed loop stages.
