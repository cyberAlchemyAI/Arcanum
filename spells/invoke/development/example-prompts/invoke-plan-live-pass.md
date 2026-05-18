# Invoke Example Prompt: invoke-plan-live-pass

## Invocation

```text
arcanum-spell-invoke plan a Mars habitat supply request module from approved design outputs
```

## Codex Prompt

Use the Codex command adapter at `.codex/commands/arcanum-spell-invoke.md`.

Run `invoke` for this required L2 live example:

- Task ID: `invoke-plan-live-pass`
- Regime: `LIVE-PLAN-001`
- Mode: `plan`
- User request: Plan implementation for a Mars habitat supply request module from approved design outputs. Use the approved terms supply request, item category, urgency, approval status, operator note, and unresolved planning question.
- Approved design outputs:
  - Architecture: six-view design bundle exists for supply request intake, item category classification, urgency triage, approval status transition, and operator note capture.
  - Glossary consistency: pass for supply request, item category, urgency, approval status, operator note, and unresolved planning question.
  - Design transport: design outputs are approved for plan consumption.
  - Constraint: plan mode must not execute tasks or mutate source code.
- Planning scope:
  - Complexity: medium.
  - Task estimate: seven tasks.
  - Output artifacts: implementation plan, implementation-layering artifact, split work-pack, and execution-pack handoff.
  - Per-layer planning: required for L0, L1, L2, and L3.
  - Smallest Working Units: required because complexity is medium.
- Implementation detail requirement:
  - Include implementation-detail specs for every execution task.
  - For classification, triage, approval status transition, operator note handling, and unresolved planning question handling, include concrete implementation notes such as ordered rules, pseudocode, inputs, outputs, edge cases, and validation evidence.
  - Do not leave any task as a vague instruction like "implement this bundle" or "build this workflow" without explaining how the worker should implement the domain logic.
- Expected invoke use: Produce a governed plan artifact with implementation plan, global implementation layering, split work-pack, per-layer planning slices, validation strategy, blocker ledger, plan transport, and next route.

Return the standard `Invoke Result` shape from the canonical invoke contract.

The output must include:

- `## Invoke Result`
- `Mode: plan`
- `Phase status: pass`
- implementation plan evidence,
- implementation layering evidence,
- work-pack evidence,
- complexity and output mode,
- L0, L1, L2, and L3 per-layer planning slices,
- implementation-detail specs for execution tasks,
- Smallest Working Units manifest and task-local SWU lists,
- SWU rows with parent task, write scope, acceptance evidence, and verification command or reviewable check,
- algorithm, state-transition, classification, or data-flow details for domain-logic tasks,
- validation strategy,
- blocker ledger or unresolved gaps,
- plan transport evidence,
- next route evidence.

Also include the primary user-facing plan artifact body after the `Invoke Result`. Do not collapse the artifact into one summary line.

Important capture rule:

- Do not edit or save files yourself.
- Return only the full markdown output that should be saved.
- The outer runner will save your final response to the output path.
- Do not respond with a summary like "Saved the output to ...".

## Expected Capture Path

The outer runner saves the final response as:

```text
arcanum/spells/invoke/development/example-outputs/invoke-plan-live-pass.output.md
```
