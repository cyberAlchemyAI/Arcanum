# Regime: STRATEGY-CLOSE-COMPLEX-001

## Goal

Verify dependency readiness, partial-result propagation, independent approval,
agent closeout, and ledger event cardinality.

## Prompt

- Prompt: `example-prompts/strategy-close-complex.md`

## Required Output Patterns

- `## Subagent Strategy Result`
- `Human gate: confirmed/frozen`
- `Execution: partial`
- `0 open`
- `Ledger closeout: paired`
- `parent final approval|parent approval`

## Forbidden Output Patterns

- `Execution: completed`
- `agents left open`
- `three close events`

## Quality Bar

- Downstream agents and the parent must receive the partial failure.
- Feedback must remain non-blocking and the parent must approve independently.
- Every agent must be joined and closed.
- The ledger must contain exactly one dispatch event and one paired close event.

## Anti-Patterns

- Do not convert the confidence-limited result into clean success.
- Do not hide failed-agent evidence or leave agents open.
- Do not add extra close events as retries.

## Observability

- Record partial failures, dependency flow, final approver, lifecycle counts,
  exit reason, and ledger pair state.

## Lessons To Capture

- Partial-result propagation gaps.
- Readiness mistakes around zig-zag and feedback edges.
- Agent or ledger closeout cardinality drift.

## Promotion Evidence

This deterministic fixture is a control. A real runtime output body and a real
registrar integration test are still required.
