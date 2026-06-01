# Context Pack: SWU-RUNTIME-003

## Context Pack Summary

- Task: execute `SWU-RUNTIME-003`
- Mode: lean
- Work-pack: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- Selected SWU: `SWU-RUNTIME-003`
- Parent task: `TASK-RUNTIME-002 Add Codex Exec Adapter`
- Write scope: `tools/arcanum-runtime-run`, `framework/runtime/adapters/`, `framework/runtime/development/fixtures/codex-exec/`, task-session evidence, work-pack synchronization
- Validation surface: runtime fixture runs, JSON checks, adapter profile evidence, validation grade checks, SQLite symlink/resolved-path checks, `bash -n`, `git diff --check`
- Strict runtime-goal coverage: n/a
- Resulting session report: `tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md`

## Controlling Sources

- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-SCHEMAS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/ADAPTER-CONTRACT-DECISIONS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/SCHEMA-DISCIPLINE-INTEGRATION.md`
- `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md`
- `tools/arcanum-runtime-run`
- `framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md`

## Obligations

| ID | Obligation | Source | Coverage |
| --- | --- | --- | --- |
| O1 | Use isolated per-run `CODEX_HOME`. | `WORK-PACK.md`, `CODEX-RUNTIME-ADAPTER-DESIGN.md` | covered |
| O2 | Allow contained run-local SQLite. | `ADAPTER-CONTRACT-DECISIONS.md`, `RUNTIME-SCHEMAS.md` | covered |
| O3 | Reject symlinked or outside-resolving SQLite. | `ADAPTER-CONTRACT-DECISIONS.md`, `RUNTIME-SCHEMAS.md` | covered |
| O4 | Record adapter profile evidence. | `RUNTIME-SCHEMAS.md`, `SCHEMA-DISCIPLINE-INTEGRATION.md` | covered |
| O5 | Classify Codex outcomes before runtime status mutation. | `ADAPTER-CONTRACT-DECISIONS.md` | covered |
| O6 | Record validation grade evidence. | `RUNTIME-SCHEMAS.md` | covered |
| O7 | Preserve runner-owned `events.jsonl`. | `RUNTIME-SCHEMAS.md`, `ADAPTER-CONTRACT-DECISIONS.md` | covered |

## Gate Check

- Dependencies: `SWU-RUNTIME-001` and `SWU-RUNTIME-002` passed in `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md`.
- Remaining blocker before mutation: none after the corrected SQLite policy.
- Assumption: `codex-exec` can pass as `adapter-safety` when backend/startup is blocked, but execution proof requires a clean Codex run.
- Escalation boundary: rerun Codex fixture outside the sandbox if the sandbox prevents Codex startup.

## Decision Pack

| Decision | Selected | Rationale |
| --- | --- | --- |
| Adapter shape | Keep `codex-exec` inside `tools/arcanum-runtime-run` for v1 and add a Markdown adapter profile. | Static dispatch is already the v1 runner pattern; dynamic adapter loading is deferred. |
| SQLite policy | Allow regular SQLite files inside run-local adapter state; block symlinks and outside-resolving paths. | This preserves the real safety property without rejecting normal Codex startup. |

## Validation Commands

```bash
bash -n tools/arcanum-runtime-run
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run-swu003
tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec-swu003
tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec-swu003-escalated
jq empty /tmp/arcanum-runtime-codex-exec-swu003-escalated/RUN.json /tmp/arcanum-runtime-codex-exec-swu003-escalated/STATUS.json /tmp/arcanum-runtime-codex-exec-swu003-escalated/artifacts/adapter-profile.json
git diff --check -- tools/arcanum-runtime-run framework/runtime tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md
```
