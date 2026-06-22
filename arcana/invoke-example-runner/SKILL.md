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
Select one Invoke template validation prompt, run it through the active native `invoke` skill package or an explicit legacy compatibility adapter, validate the returned `Invoke Result`, and save the user-facing output as validation evidence.
</objective>

<execution-surface>
Default to the active native `invoke` skill package. Use `.codex/commands/arcanum-spell-invoke.md`, `invoke-example-next`, `invoke-example-run`, or `arcanum/spells/invoke/development/run-template-example-with-codex.sh` only when explicit legacy command compatibility is being validated.

The short legacy commands are discovery bridges into this sigil:

- `invoke-example-next` resolves `next`,
- `invoke-example-run <selection>` resolves an exact task ID, template/complexity pair, or `next`.
</execution-surface>

<process>
1. Resolve the requested example:
   - exact task ID such as `sigil-medium`,
   - template plus complexity such as `sigil medium`,
   - or `next` for the first prompt whose output file does not exist.
2. Use `arcanum/spells/invoke/development/select-template-example-prompt.sh` to locate the prompt and capture path.
3. If the selected output already exists and the user did not request a rerun, return `FLAG` with the existing output path instead of overwriting it.
4. Use the active native `invoke` skill package as the default execution surface. Use `arcanum/spells/invoke/development/run-template-example-with-codex.sh` only when the user wants automated legacy CLI execution.
5. Otherwise read the selected prompt and execute its **Codex Prompt** instructions in the current Codex session.
6. Save the resulting user-facing `Invoke Result` to the prompt's `Expected Capture Path`.
7. Validate the saved result:
   - the output must contain a real `Invoke Result`, not a save-summary response or placeholder,
   - the selected mode must route through canonical `invoke` contracts,
   - every mode result must preserve the Dispatch Spec technique trace or report a block/flag,
   - `plan`, `full`, and `validate` results must include Distill validation status before any mutation-capable handoff,
   - a `task-session` next route must remain a handoff, not completed execution,
   - any subagent strategy must include explicit subagent/local fallback boundaries and expected receipt shape.
8. Return selected prompt, output path, execution surface, validation state, Dispatch trace status, Distill validation status, Task Session handoff readiness, and next unrun prompt if any.
</process>

<quality-bar>
A successful run must:

- select exactly one prompt,
- preserve the prompt's task ID, template target, complexity, and user request,
- route through canonical `invoke` contracts and the active native skill surface by default,
- save a user-facing output file,
- verify Dispatch Spec technique trace evidence,
- verify Distill validation evidence for `plan`, `full`, and `validate`,
- preserve `task-session` as the next owner for bounded execution,
- avoid marking deferred modes as implemented,
- report any block or flag result honestly,
- leave canonical invoke contracts unchanged while running examples.
</quality-bar>

<anti-patterns>
Avoid:

- claiming a prompt was run when only selected,
- overwriting an existing output unless the user requested a rerun,
- bypassing the active native `invoke` skill package,
- treating legacy command compatibility as native authoring readiness,
- editing canonical invoke contracts while running examples,
- accepting an output that lacks Dispatch trace or required Distill validation evidence,
- marking task execution complete when Invoke only emitted a Task Session handoff,
- replacing missing outputs with generic placeholder text.
</anti-patterns>

<output-contract>
Return:

```markdown
## Invoke Example Runner Result

- Selection: <task-id>
- Prompt: <path>
- Output: <path>
- Execution surface: native invoke | legacy command | legacy CLI
- Invoke mode: define | design | plan | handoff | refresh | full | validate
- Invoke status: pass | flag | block
- Dispatch trace: pass | flag | block
- Distill validation: pass | flag | block | skipped | not_applicable
- Task-session handoff: ready | blocked | not_applicable
- Saved output: yes | no
- Next unrun: <task-id | none>
- Follow-up: <items | none>
```
</output-contract>
