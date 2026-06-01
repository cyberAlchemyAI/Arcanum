# Context Pack: SWU-RUNTIME-008

## Context Pack Summary

- Task session: `SWU-RUNTIME-008`
- Work-pack: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- Selected task: `TASK-RUNTIME-007 Collapse Runtime Runner Into tools/arcanum`
- Mode: local execution
- Strict coverage: pass
- Runtime delegation: none

## Controlling Sources

- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/SINGLE-COMMAND-SURFACE-REFRESH.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md`
- `tools/arcanum`
- `tools/arcanum-runtime-run`
- `framework/runtime/README.md`
- `framework/runtime/adapters/codex-exec.md`

## Task Contract

`tools/arcanum --exec` must become the single active command execution path while preserving adapter selection.

Required behavior:

- `tools/arcanum --exec --adapter <adapter-id>` selects runtimes.
- `tools/arcanum --list-adapters` and `tools/arcanum --resolve-adapter <adapter-id>` expose available runtime profiles.
- `dry-run` proves a non-Codex adapter path.
- `codex-exec` remains selectable without owning the runtime model.
- Command output writes directly to requested `--output`.
- Runtime envelope evidence, when enabled, records status/events/profile without owning command output.
- Successful command execution does not create runtime `RESULT.md`.
- `tools/arcanum-runtime-run` is deprecated or shimmed.

## Write Scope

- `tools/arcanum`
- `tools/arcanum-runtime-run`
- `framework/runtime/README.md`
- `framework/runtime/adapters/codex-exec.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md`
- `tools/development/task-sessions/20260526T1301Z-swu-runtime-008.md`
- `tools/development/context-packs/20260526-swu-runtime-008-task-session.md`

## Gate Check

- Dependencies: pass; `SWU-RUNTIME-007` is recorded passed.
- Source context: pass; controlling design artifacts are present.
- Write scope: pass.
- Validation surface: pass.
- User approval: task-session invocation implies execute next ready SWU.

## Validation Surface

```bash
bash -n tools/arcanum tools/arcanum-runtime-run
tools/arcanum --resolve invoke
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter dry-run
tools/arcanum --resolve-adapter codex-exec
tools/arcanum --print-prompt invoke "define runtime smoke"
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-one-tool-output.md invoke "define runtime smoke"
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-shim-dry-run --output /tmp/arcanum-runtime-shim-dry-run.md
```
