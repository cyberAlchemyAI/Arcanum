# Arcanum Runtime-Native Handoff

STATUS: flag

The `local-skill` adapter does not spawn a nested model-backed CLI process. It preserves the command prompt, requested output path, and receipt contract so the parent native runtime surface can execute the stage directly.

## Command

- Command: `distill`
- Command file: `.codex/commands/distill.md`
- Output: `/home/vrondelli/projects/domainspec-core/arcanum/development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/05-distill.md`
- Adapter: `local-skill`

## Request

distill target=development/craft/CRAFT-VALIDATION.md using seed=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/REFINE-SEED-PROPOSAL.md, define=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/02-invoke-define.md, review=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/03-interrogation-refine-review.md, research=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/04-research-decision.md; select smallest coherent refinement unit and rejected alternatives

## Receipt Contract

The parent runner or subagent must return:

- `dispatch_id` or run id when available
- `step_id` or command name
- `capability_ref`: `distill`
- `execution_surface`: `codex-skill`, `claude-skill`, `copilot-instructions`, `native-subagent`, or `local-inline`
- `status`: `pass`, `flag`, `block`, `interrupted`, or `timeout`
- artifact paths
- validation result
- observability status or returned telemetry receipt
- blockers and handoff note

## Prompt

```markdown
Execute the already-dispatched Arcanum command `distill`.

1. Read `.codex/commands/distill.md`.
2. Follow that command's process and embedded canonical contract.
3. Treat the user request below as the command arguments.
4. Treat observer envelope setup as task zero.
5. Preserve the command output contract and include observability closeout status when available.
6. Do not call `tools/arcanum --exec`, `codex exec`, or any nested model-backed runtime for this same command. This process is already the command-backed stage execution; produce the command artifact directly.

User request:
distill target=development/craft/CRAFT-VALIDATION.md using seed=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/REFINE-SEED-PROPOSAL.md, define=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/02-invoke-define.md, review=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/03-interrogation-refine-review.md, research=development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/stages/04-research-decision.md; select smallest coherent refinement unit and rejected alternatives
```
