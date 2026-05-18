# Invoke Example Prompt: invoke-define-design-plan-live-pass

## Invocation

```text
arcanum-spell-invoke define design plan a Mars rover maintenance log module
```

## Codex Prompt

Use the Codex command adapter at `.codex/commands/arcanum-spell-invoke.md`.

Run `invoke` for this required L2 integration live example:

- Task ID: `invoke-define-design-plan-live-pass`
- Regime: `LIVE-DEFINE-DESIGN-PLAN-001`
- Modes: `define`, `design`, then `plan`
- User request: Define, design, and plan a Mars rover maintenance log module. Use the terms Mars rover maintenance log, daily inspection note, component status, operator decision, and unresolved repair question.
- Expected define use:
  - produce spec evidence,
  - produce glossary evidence,
  - produce define transport evidence.
- Expected design use:
  - consume the approved define outputs,
  - produce source contracts,
  - produce all six design views,
  - produce glossary consistency evidence,
  - produce design transport evidence.
- Expected plan use:
  - consume approved design outputs,
  - produce implementation plan evidence,
  - produce global implementation-layering evidence,
  - produce a low-complexity single-file work-pack with compact layer mapping,
  - produce inline implementation details for each low-complexity task so execution is not handed vague bundle-level instructions,
  - produce validation strategy,
  - produce plan transport evidence,
  - keep implementation execution deferred.

Return an inspectable multi-phase output using the standard `Invoke Result` shape for each phase.

The output must include:

- `## Invoke Result`
- `Mode: define`
- `Mode: design`
- `Mode: plan`
- `Phase status: pass`
- spec and glossary evidence,
- define transport evidence,
- all six design views,
- glossary consistency and design transport evidence,
- implementation plan evidence,
- implementation layering evidence,
- work-pack evidence,
- implementation detail evidence,
- validation strategy,
- plan transport evidence,
- text stating that plan consumes approved design outputs.

Also include the primary user-facing artifact bodies after the `Invoke Result` sections. Do not collapse the chain into one summary line.

Important capture rule:

- Do not edit or save files yourself.
- Return only the full markdown output that should be saved.
- The outer runner will save your final response to the output path.
- Do not respond with a summary like "Saved the output to ...".

## Expected Capture Path

The outer runner saves the final response as:

```text
arcanum/spells/invoke/development/example-outputs/invoke-define-design-plan-live-pass.output.md
```
