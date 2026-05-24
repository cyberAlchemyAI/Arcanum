# TASK-CLO-006: Add Runtime Command Adapter

## Goal

Add a local command/runtime adapter only after manual validation proves behavior.

## Layer

L2 Runtime And Observability

## Micro-Layers

- L2.1 Command Surface
- L2.2 Role Execution Policy
- L2.4 Runtime Validation

## Resolved Runtime Policy

- B-CLO-001 is resolved: use true subagents when the runtime supports them. If the runtime does not support subagents, use labeled Proposer/Balancer role simulation with the same trace contract.

## Source Contracts

- `arcana/distill/SKILL.md`
- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../PLAN-TRANSPORT.md](../../PLAN-TRANSPORT.md)
- existing command adapter conventions under `.codex/commands/`

## Inputs

- validated SKILL from TASK-CLO-002,
- validation report from TASK-CLO-004,
- telemetry contract from TASK-CLO-005,
- resolved runtime role policy: subagent-first, role simulation fallback.

## Output Artifacts

- command adapter or route entry for `/distill`,
- runtime role policy documentation,
- representative runtime run evidence.

## Implementation Steps

1. Confirm TASK-CLO-004 permits L2 runtime work.
2. Choose the runtime path that matches local command conventions.
3. Add an adapter that points to the canonical SKILL instead of duplicating the sigil process.
4. Implement the subagent-first role policy: use true subagents when supported by the runtime; otherwise use labeled role simulation.
5. Preserve finite recursion, budget confirmation, technique trace, output contract, and navigable result closeout.
6. Run a representative resolution check.
7. Compare the representative runtime behavior with L1 golden behavior.

## Edge Cases

- Do not make true subagents mandatory for runtimes that do not support them.
- Do not choose role simulation when the active runtime can support true subagents for the Proposer/Balancer roles.
- Do not allow runtime access to weaken the manual SKILL contract.
- Do not promote registry work merely because the command resolves.
- If adapter conventions are unclear, return a flag without reopening B-CLO-001 unless both true subagents and role simulation are impossible.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-012 | L2.1 | Add runtime adapter. | Adapter points to canonical SKILL and preserves closeout. |
| SWU-CLO-013 | L2.2 | Define runtime role execution policy. | Runtime states subagent-first execution, role simulation fallback, and tournament limits. |
| SWU-CLO-014 | L2.4 | Validate runtime representative run. | Closeout includes observation fields, role policy, and output contract. |

## Verification

```bash
tools/arcanum --resolve /distill
```

Representative run review is required after resolution succeeds.

## Done When

- Command resolves through `tools/arcanum`.
- Runtime role policy is explicit.
- Representative run preserves closeout and result contract.
