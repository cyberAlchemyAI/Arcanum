# Refine Seed Proposal

- Run ID: `arcanum-refine-20260526T222905Z`
- Capability: `refine`
- Mode: command
- Target: `framework/runtime`
- Request summary: smoke check that Arcanum `codex-exec` can start and return a minimal non-mutating response.
- Preset: `compact`
- Research mode: `no-research`
- Write scope: this refinement evidence folder and Arcanum runtime envelope evidence only.
- Target smoke write scope: none beyond the requested `--output` artifact and runtime envelope metadata.

## Done Criteria

- `tools/arcanum --resolve` succeeds for `refine` and required command-backed stages.
- A model-backed `tools/arcanum --exec --adapter codex-exec` smoke is attempted with `ARCANUM_RUNTIME_ENVELOPE=1`.
- The smoke returns either a clean minimal response or a classified adapter-safety blocker.
- Runtime envelope JSON validates with `jq`.
- The final result records exact status and next route.

## Validation Surface

```bash
tools/arcanum --resolve refine
tools/arcanum --resolve context-builder
tools/arcanum --resolve invoke
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
ARCANUM_RUNTIME_ENVELOPE=1 ARCANUM_RUNTIME_RUN_DIR=<run-folder>/runtime/codex-exec-smoke tools/arcanum --exec --adapter codex-exec --output <run-folder>/stages/00-codex-exec-smoke.md invoke "define runtime smoke: return a minimal non-mutating response"
jq empty <run-folder>/runtime/codex-exec-smoke/RUN.json
jq empty <run-folder>/runtime/codex-exec-smoke/STATUS.json
```

## Planned Stage Configuration

The canonical Refine loop is preserved. Because the user request is itself a runtime smoke check, command-backed design stages are treated as blocked after the smoke result when nested command execution cannot provide clean model output. This avoids replacing unavailable command-owned artifacts with freeform prose.
