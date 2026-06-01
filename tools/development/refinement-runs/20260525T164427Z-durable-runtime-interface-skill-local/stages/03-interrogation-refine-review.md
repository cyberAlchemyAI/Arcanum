# Stage 3: Interrogation Refine Review

## Verdict

`flag`

## Review

The defined architecture is right, but it needs stronger answers on three points:

1. Is the handoff immutable?
2. Can the runtime support local skill execution as well as external adapters?
3. How does refine validate multiple loops without becoming the runtime database?

## Findings

The handoff must be immutable after creation. Mutable status belongs in runtime state.

Local skill execution should be represented as an adapter too, but not the first shell runner adapter. For v1, `dry-run` can stand in for non-executing validation, while `codex-exec` handles actual model execution. This current run is a design artifact created by the active Codex session, not a durable executor adapter.

Refine should not become a database. Its target-local `RUN-MANIFEST.md` and `evidence-index.json` should index stage topology and artifacts. Runtime execution state belongs under `.arcanum/runtime/runs/`.

## Required Strengthening

The design needs two linked but separate folder contracts:

- runtime-owned durable execution folders,
- orchestrator-owned target-local refinement folders.

It also needs explicit loop topology fields for candidate, nested, repair, and continuation loops.
