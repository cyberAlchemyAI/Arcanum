# Runtime Handoff

## Objective

Execute Arcanum command "invoke" through the durable runtime runner and preserve the command surface output contract.

## Orchestrator

- orchestrator_id: tools-arcanum
- orchestrator_run_id: codex-exec-smoke

## Target

- target_kind: command
- target_id: invoke

## Inputs

- command: invoke
- command_file: .codex/commands/invoke.md
- request: define runtime smoke: return exactly PASS if you can start and respond; do not inspect or modify files
- requested_output: framework/runtime/development/refinement-runs/arcanum-refine-20260526T222905Z/stages/00-codex-exec-smoke.md
- target_artifact_dir: none inferred

## Allowed Write Scope

- framework/runtime/development/refinement-runs/arcanum-refine-20260526T222905Z/stages/00-codex-exec-smoke.md
- .arcanum/runtime/runs/
- .arcanum/runtime/handoffs/
- .arcanum/observability/runs/arcanum-command/

## Expected Outputs

- command output: framework/runtime/development/refinement-runs/arcanum-refine-20260526T222905Z/stages/00-codex-exec-smoke.md
- runtime RUN.json
- runtime STATUS.json
- runtime events.jsonl

## Expected Command-Owned Artifacts

- none inferred

## Validation

- requested output path exists
- runtime RUN.json and STATUS.json are valid JSON
- runtime status is passed, flagged, blocked, or failed
- expected command-owned artifacts exist when listed

## Blocked Conditions

- command cannot be resolved
- runtime runner is unavailable
- adapter is unavailable
- requested output cannot be written
- Codex cannot start safely

## Adapter Preference

- adapter_id: codex-exec

## Nesting Policy

- loop_role: root
- loop_id: arcanum-command-invoke
- parent_loop_id: null
- parent_run_id: null

## Command Prompt

BEGIN COMMAND PROMPT
Use the Arcanum command surface for command `invoke`.

1. Read `.codex/commands/invoke.md`.
2. Follow that command's process and embedded canonical contract.
3. Treat the user request below as the command arguments.
4. Treat observer envelope setup as task zero.
5. Preserve the command output contract and include observability closeout status when available.

User request:
define runtime smoke: return exactly PASS if you can start and respond; do not inspect or modify files
END COMMAND PROMPT
