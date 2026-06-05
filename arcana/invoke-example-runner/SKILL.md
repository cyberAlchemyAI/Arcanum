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
5. Use the active native `invoke` skill package as the execution surface; use `.codex/commands/arcanum-spell-invoke.md` only when explicit legacy command compatibility is being validated.
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
