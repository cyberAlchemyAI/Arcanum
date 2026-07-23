# Regime: STRATEGY-PROPOSAL-MEDIUM-001

## Goal

Verify degraded preflight handling, genuine tension, and the human stop gate.

## Prompt

- Prompt: `example-prompts/strategy-proposal-medium.md`

## Required Output Patterns

- `## Subagent Strategy Result`
- `Trigger decision: dispatch`
- `Tension gate: PASS/PASS`
- `Human gate: awaiting confirmation`
- `Registration: unregistered`
- `machine index unavailable|machine_index_gap`

## Forbidden Output Patterns

- `Registration: registered`
- `Execution: completed`
- `precedent-clean`

## Quality Bar

- The preflight gap must remain visible and must change agent inputs or lanes.
- The proposed pair must have differentiated angles and a predicted disagreement.
- The run must stop before registration and working-agent execution.

## Anti-Patterns

- Do not reinterpret a missing machine index as clean precedent evidence.
- Do not treat tension checks as human confirmation.

## Observability

- Record preflight status, design consequence, dual-check verdicts, and the
  awaiting-confirmation state.

## Lessons To Capture

- Degraded preflight handling.
- Nominal rather than substantive disagreement.
- Accidental execution before confirmation.

## Promotion Evidence

This deterministic fixture is a control. A real runtime output body is still
required.
