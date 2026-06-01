# Arcanum Runtime-Native Handoff

STATUS: flag

The `local-skill` adapter does not spawn a nested model-backed CLI process. It preserves the command prompt, requested output path, and receipt contract so the parent native runtime surface can execute the stage directly.

## Command

- Command: `invoke`
- Command file: `.codex/commands/invoke.md`
- Output: `/home/vrondelli/projects/domainspec-core/arcanum/development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/02-invoke-define.md`
- Adapter: `local-skill`

## Request

define refinement target=development/craft/CRAFT-VALIDATION.md using seed=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/REFINE-SEED-PROPOSAL.md and context=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/01-context-builder.md; preset=standard; preserve native output contract

## Receipt Contract

The parent runner or subagent must return:

- `dispatch_id` or run id when available
- `step_id` or command name
- `capability_ref`: `invoke`
- `execution_surface`: `codex-skill`, `claude-skill`, `copilot-instructions`, `native-subagent`, or `local-inline`
- `status`: `pass`, `flag`, `block`, `interrupted`, or `timeout`
- artifact paths
- validation result
- observability status or returned telemetry receipt
- blockers and handoff note

## Prompt

```markdown
Execute the already-dispatched Arcanum command `invoke`.

1. Read `.codex/commands/invoke.md`.
2. Follow that command's process and embedded canonical contract.
3. Treat the user request below as the command arguments.
4. Treat observer envelope setup as task zero.
5. Preserve the command output contract and include observability closeout status when available.
6. Do not call `tools/arcanum --exec`, `codex exec`, or any nested model-backed runtime for this same command. This process is already the command-backed stage execution; produce the command artifact directly.

User request:
define refinement target=development/craft/CRAFT-VALIDATION.md using seed=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/REFINE-SEED-PROPOSAL.md and context=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/01-context-builder.md; preset=standard; preserve native output contract
```
