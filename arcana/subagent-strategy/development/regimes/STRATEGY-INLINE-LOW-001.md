# Regime: STRATEGY-INLINE-LOW-001

## Goal

Verify that coordination overhead is rejected when no dispatch trigger holds.

## Prompt

- Prompt: `example-prompts/strategy-inline-low.md`

## Required Output Patterns

- `## Subagent Strategy Result`
- `Trigger decision: inline`
- `Registration: not applicable`
- `Subagents: none`

## Forbidden Output Patterns

- `registered`
- `confirmed/frozen`

## Quality Bar

- The result must explain why no trigger holds.
- It must expose zero subagents and no registration or ledger activity.

## Anti-Patterns

- Do not spawn a helper merely to validate the no-dispatch decision.
- Do not require a runtime profile for inline work.

## Observability

- Record one meaningful inline trigger decision without a dispatch row.

## Lessons To Capture

- False-positive dispatch triggers.
- Output fields that imply execution despite the inline decision.

## Promotion Evidence

This deterministic fixture is a control. A real runtime output body is still
required.
