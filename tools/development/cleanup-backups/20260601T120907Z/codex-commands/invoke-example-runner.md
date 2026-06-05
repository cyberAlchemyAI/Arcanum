# Arcanum Sigil: invoke example runner

<!-- arcanum:capability-id invoke-example-runner -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command invoke-example-runner -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-invoke-example-runner-<UTC timestamp>`.
- `capability.id`: `invoke-example-runner`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `invoke-example-runner` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `invoke-example-runner`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/invoke-example-runner/README.md

````markdown
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

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/invoke-example-runner/SKILL.md

````markdown
---
name: invoke-example-runner
description: "Use when selecting and running invoke template validation prompts in Codex, including picking a task by ID, template, complexity, or the next unrun prompt and saving the Invoke Result output."
argument-hint: "<task-id | template complexity | next>"
tier: arcana
domain: invoke-validation
version: 0.1.0
origin: created to make invoke template examples executable from generated prompt files
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Invoke Example Runner

<objective>
Select an invoke template validation prompt, run it through the active Codex session using `arcanum-spell-invoke`, and save the user-facing output as validation evidence.
</objective>

<process>
1. Resolve the requested example:
   - exact task ID such as `sigil-medium`,
   - template plus complexity such as `sigil medium`,
   - or `next` for the first prompt whose output file does not exist.
2. Use `arcanum/spells/invoke/development/select-template-example-prompt.sh` to locate the prompt and capture path.
3. Prefer `arcanum/spells/invoke/development/run-template-example-with-codex.sh` when the user wants automated CLI execution.
4. Otherwise read the selected prompt and execute its **Codex Prompt** instructions in the current Codex session.
5. Use `.codex/commands/arcanum-spell-invoke.md` as the command bridge.
6. Save the resulting user-facing `Invoke Result` to the prompt's `Expected Capture Path`.
7. Return selected prompt, output path, validation state, and next unrun prompt if any.
</process>

<quality-bar>
A successful run must:

- select exactly one prompt,
- preserve the prompt's task ID, template target, complexity, and user request,
- route through canonical `invoke` contracts,
- save a user-facing output file,
- avoid marking deferred modes as implemented,
- report any block or flag result honestly.
</quality-bar>

<anti-patterns>
Avoid:

- claiming a prompt was run when only selected,
- overwriting an existing output unless the user requested a rerun,
- bypassing `arcanum-spell-invoke`,
- editing canonical invoke contracts while running examples,
- replacing missing outputs with generic placeholder text.
</anti-patterns>

<output-contract>
Return:

```markdown
## Invoke Example Runner Result

- Selection: <task-id>
- Prompt: <path>
- Output: <path>
- Invoke status: pass | flag | block
- Saved output: yes | no
- Next unrun: <task-id | none>
```
</output-contract>

````
