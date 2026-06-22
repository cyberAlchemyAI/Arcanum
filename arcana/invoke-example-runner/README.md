# Invoke Example Runner

Invoke Example Runner is an Arcana sigil for selecting Invoke template validation prompts and running them through the active Codex session.

It turns the template validation task matrix into an executable workflow: pick one low, medium, or complex example, load the generated prompt, run the native `invoke` skill package by default, and save the user-facing output for later validation.

Legacy command files remain compatibility adapters only. The runner may use `.codex/commands/arcanum-spell-invoke.md`, `invoke-example-next`, `invoke-example-run`, or `run-template-example-with-codex.sh` when the task is explicitly validating the legacy command surface.

## Use When

- a maintainer wants to run one invoke template example,
- a maintainer wants the next unrun example from the template matrix,
- an invoke template family needs low, medium, or complex output evidence,
- generated prompt files need to become saved example outputs.

## Do Not Use When

- the user only wants to inspect the template matrix,
- the prompt has already been run and no rerun is requested,
- the task is to validate saved outputs rather than produce them.

## Default Inputs

- task ID, for example `sigil-medium`,
- or template and complexity, for example `sigil medium`,
- or `next` to select the first prompt without a saved output.

## Default Outputs

- selected prompt path,
- selected output capture path,
- `Invoke Result` saved under `arcanum/spells/invoke/development/example-outputs/`,
- execution surface used: native `invoke`, legacy command, or legacy CLI,
- Dispatch Spec technique trace status,
- Distill validation status for `plan`, `full`, and `validate`,
- Task Session handoff readiness when the result routes to bounded execution,
- run summary with pass, flag, or block.

## Validation Expectations

The saved output must be a real user-facing `Invoke Result`, not a placeholder or save-summary response. Every result must preserve the Invoke Dispatch Spec technique trace requirement. `plan`, `full`, and `validate` results must include Distill validation status before any mutation-capable handoff. If the result routes to `task-session`, the runner records handoff readiness but does not mark implementation work complete.

## Why This Is Arcana

The sigil coordinates prompt selection, Codex command routing, output capture, and validation evidence across invoke templates. It is orchestration around another spell, not a deterministic transformation by itself.
