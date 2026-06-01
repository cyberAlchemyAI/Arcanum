# Task Session Report: TASK-ORCH-007-009

## Status

`flag`: core migration executed; one validation remains blocked by pre-existing parent-repo install gap.

## Scope

Executed the runtime/install/observability migration slice from the Invoke plan:

- `TASK-ORCH-007`: active runtime and installer surfaces
- `TASK-ORCH-008`: experiment and Invoke example-runner surfaces
- `TASK-ORCH-009`: observability and command-surface language

This session also extended the installer to create Claude and Copilot agent surfaces.

## Changes

- Added `local-skill` as the native agent skill/subagent handoff adapter in `tools/arcanum`.
- Changed no-config and repo-local runtime defaults from `codex-exec` to `local-skill`.
- Kept `codex-exec` and `codex-bypass` as explicit legacy adapters.
- Added bootstrap surface selection through `--surfaces codex,claude,copilot|all|none`.
- Added Claude install output:
  - `.claude/skills/arcanum-orchestrate/SKILL.md`
  - `.claude/agents/arcanum-stage-worker.md`
  - `CLAUDE.md`
- Added Copilot install output:
  - `.github/copilot-instructions.md`
  - `.github/instructions/arcanum.instructions.md`
  - `AGENTS.md`
- Updated Task Session, Refine, Experiment Harness, Invoke runbook, Observed Invocation Loop, observability docs, and Whisper runtime language toward native skills/subagents plus returned receipts.
- Updated the orchestration runtime plan and codex-exec surface inventory closeout.

## Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Shell syntax | pass | `bash -n tools/bootstrap_arcanum.sh tools/install_arcanum.sh tools/arcanum tools/arcanum-runtime-run` |
| Adapter list | pass | `tools/arcanum --list-adapters` returned `local-skill`, `dry-run`, `codex-exec`, `codex-bypass` |
| Local-skill profile | pass | `tools/arcanum --resolve-adapter local-skill` returned native agent profile |
| Repo default adapter | pass | `tools/arcanum --get-default-adapter` returned `DEFAULT_ADAPTER=local-skill` |
| Local-skill handoff smoke | pass | `tools/arcanum --exec --adapter local-skill --output /tmp/arcanum-local-skill-output.md invoke "define runtime smoke"` wrote a receipt contract and observed telemetry |
| Dispatch profile | pass | `formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/orchestration-runtime.dispatch.json` |
| Bootstrap all surfaces dry-run | pass | generated Codex, Claude, Copilot, runtime, and hooks paths |
| Bootstrap Claude/Copilot dry-run | pass | generated Claude/Copilot paths without Codex commands |
| Bootstrap all surfaces temp install | pass | temp install contained `.claude`, `.github`, `.codex`, `.arcanum/runtime`, `AGENTS.md`, and `CLAUDE.md` |
| Invoke validation fixtures | block | missing parent-repo generated commands under `/home/vrondelli/projects/domainspec-core/.codex` and `/home/vrondelli/projects/domainspec-core/.arcanum/runtimes/codex/commands` |

## Blocked Follow-Up

`spells/invoke/development/run-validation-fixtures.sh` now blocks on missing generated parent-repo command surfaces, not on the local-skill migration itself:

- `/home/vrondelli/projects/domainspec-core/.codex/commands/arcanum-sigil-invoke-example-runner.md`
- `/home/vrondelli/projects/domainspec-core/.codex/commands/invoke-example-next.md`
- `/home/vrondelli/projects/domainspec-core/.codex/commands/invoke-example-run.md`
- `/home/vrondelli/projects/domainspec-core/.arcanum/runtimes/codex/commands/arcanum-sigil-invoke-example-runner.md`

Recommended next task: reinstall or regenerate the parent-repo Invoke example-runner command surface, then rerun `spells/invoke/development/run-validation-fixtures.sh`.

## Decision

The migration is complete for the active runtime/install/documentation path. Historical generated evidence was preserved by design.
