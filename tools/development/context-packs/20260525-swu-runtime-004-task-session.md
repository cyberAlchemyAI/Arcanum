# Context Pack: SWU-RUNTIME-004

## Context Pack Summary

- Task: execute `SWU-RUNTIME-004`
- Mode: lean
- Work-pack: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- Selected SWU: `SWU-RUNTIME-004`
- Parent task: `TASK-RUNTIME-003 Migrate Arcanum Exec Compatibility Path`
- Write scope: `tools/arcanum`, `tools/arcanum-runtime-run`, task-session evidence, work-pack synchronization
- Validation surface: command resolution unchanged, feature-flag exec smoke, requested output copy, runtime JSON checks, runtime event ownership, `bash -n`, `git diff --check`
- Strict runtime-goal coverage: n/a
- Resulting session report: `tools/development/task-sessions/20260525T2055Z-swu-runtime-004.md`

## Controlling Sources

- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-SCHEMAS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md`
- `tools/arcanum`
- `tools/arcanum-runtime-run`

## Obligations

| ID | Obligation | Source | Coverage |
| --- | --- | --- | --- |
| O1 | Keep `tools/arcanum --resolve` unchanged. | `WORK-PACK.md` | covered |
| O2 | When `ARCANUM_RUNTIME_RUNNER=1`, generate a runtime handoff from command metadata, request, and output path. | `WORK-PACK.md`, `EXECUTION-PACK.md` | covered |
| O3 | Delegate `--exec` to `tools/arcanum-runtime-run --adapter codex-exec`. | `WORK-PACK.md` | covered |
| O4 | Preserve requested `--output`. | `RUNTIME-SCHEMAS.md`, `EXECUTION-PACK.md` | covered |
| O5 | Write blocked summary to requested output if adapter cannot produce a result. | `WORK-PACK.md` | covered |
| O6 | Preserve command summary output fields. | `WORK-PACK.md` | covered |
| O7 | Keep runtime status/events/result owned by the runner, not nested Codex. | `RUNTIME-SCHEMAS.md`, `CODEX-RUNTIME-ADAPTER-DESIGN.md` | covered after prompt repair |

## Gate Check

- Dependencies: `SWU-RUNTIME-003` passed in `tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md`.
- Remaining blocker before mutation: none.
- Assumption: a domain-level `Invoke Result` may report `Phase status: block` while the runtime compatibility path still passes, because the runtime successfully produced and copied the command output.
- Escalation boundary: sandboxed Codex startup may block on app-server initialization; execution proof may require running the smoke outside the sandbox.

## Decision Pack

| Decision | Selected | Rationale |
| --- | --- | --- |
| Migration gate | Use `ARCANUM_RUNTIME_RUNNER=1` only. | Preserves the existing direct Codex path while proving runtime compatibility. |
| Handoff storage | Store generated handoffs under `.arcanum/runtime/handoffs/`. | Keeps request evidence durable and separate from runtime run state. |
| Runtime status mapping | Treat runtime `passed` and `flagged` as command-surface completed; `blocked` and `failed` remain failed. | Preserves shell exit semantics while allowing command output to carry domain-level block verdicts. |
| Prompt repair | Tell Codex not to write runtime artifacts directly. | Runner-owned status/events/result is a hard contract. |

## Validation Commands

```bash
bash -n tools/arcanum tools/arcanum-runtime-run
tools/arcanum --resolve invoke
tools/arcanum --resolve /invoke
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-output-swu004-final.md invoke "define runtime smoke"
jq empty .arcanum/runtime/runs/arcanum-command-invoke-20260525T205403Z/RUN.json .arcanum/runtime/runs/arcanum-command-invoke-20260525T205403Z/STATUS.json .arcanum/runtime/runs/arcanum-command-invoke-20260525T205403Z/artifacts/adapter-profile.json
jq -e '.status == "passed" and .validation_grade == "execution" and (.output_paths | index("/tmp/arcanum-runtime-invoke-output-swu004-final.md"))' .arcanum/runtime/runs/arcanum-command-invoke-20260525T205403Z/STATUS.json
test -f /tmp/arcanum-runtime-invoke-output-swu004-final.md
cmp -s .arcanum/runtime/runs/arcanum-command-invoke-20260525T205403Z/RESULT.md /tmp/arcanum-runtime-invoke-output-swu004-final.md
git diff --check -- tools/arcanum tools/arcanum-runtime-run tools/development/context-packs/20260525-swu-runtime-004-task-session.md tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md tools/development/task-sessions/20260525T2055Z-swu-runtime-004.md
```
