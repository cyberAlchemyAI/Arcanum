# Invoke Example Runner

Invoke Example Runner is an Arcana sigil for selecting invoke template validation prompts and running them through the active Codex session.

It turns the template validation task matrix into an executable workflow: pick one low, medium, or complex example, load the generated prompt, run `arcanum-spell-invoke`, and save the user-facing output for later validation.

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
- run summary with pass, flag, or block.

## Why This Is Arcana

The sigil coordinates prompt selection, Codex command routing, output capture, and validation evidence across invoke templates. It is orchestration around another spell, not a deterministic transformation by itself.
