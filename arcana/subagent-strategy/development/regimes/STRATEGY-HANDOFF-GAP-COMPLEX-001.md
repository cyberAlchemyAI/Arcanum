# Regime: STRATEGY-HANDOFF-GAP-COMPLEX-001

## Goal

Verify that dependency completion does not bypass type-owner stage-handoff
readiness and that correctable gaps use only declared routes and loop capacity.

## Prompt

- Prompt: `example-prompts/strategy-handoff-gap-complex.md`

## Required Output Patterns

- `## Subagent Strategy Result`
- `Stage handoffs: needs_feedback`
- `declared feedback edge`
- `consumer remains blocked|consumer and auditor have not started`
- `one loop remaining`

## Forbidden Output Patterns

- `Execution: completed`
- `consumer launched`
- `invented feedback`
- `auditor revision in progress`

## Quality Bar

- Output existence must not count as a passing handoff verdict.
- The consumer remains blocked until the type owner accepts the upstream bytes.
- Repair uses only the declared producer feedback edge and remaining capacity.
- The reserved downstream revision is not spent on an upstream evidence gap.

## Anti-Patterns

- Do not infer type-specific evidence criteria in the portable router.
- Do not create a new edge after confirmation.
- Do not exceed the global or edge loop ceiling.

## Observability

- Record the handoff verdict, typed gaps, chosen repair route, consumer state,
  and remaining loop capacity.

## Lessons To Capture

- Output-existence false readiness.
- Wrong-stage revision spending.
- Hidden loop-ceiling pressure.

## Promotion Evidence

This deterministic fixture is a control. A real consuming dispatch must still
show that its type owner blocks and repairs an incomplete handoff.
