# TASK-CLO-006: Add Runtime Command Adapter

## Goal

Add a local command/runtime adapter only after manual validation proves behavior.

## Layer

L2 Runtime And Observability

## Micro-Layers

- L2.1 Command Surface
- L2.2 Role Execution Policy
- L2.4 Runtime Validation

## Blocker

- B-CLO-001: decide true subagents versus role simulation fallback.

## Source Contracts

- `arcana/concept-layer-optimizer/SKILL.md`
- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../PLAN-TRANSPORT.md](../../PLAN-TRANSPORT.md)
- existing command adapter conventions under `.codex/commands/`

## Inputs

- validated SKILL from TASK-CLO-002,
- validation report from TASK-CLO-004,
- telemetry contract from TASK-CLO-005,
- runtime adapter decision for role simulation versus true subagents.

## Output Artifacts

- command adapter or route entry for `/concept-layer-optimizer`,
- runtime role policy documentation,
- representative runtime run evidence.

## Implementation Steps

1. Confirm TASK-CLO-004 permits L2 runtime work.
2. Choose the runtime path that matches local command conventions.
3. Add an adapter that points to the canonical SKILL instead of duplicating the sigil process.
4. State whether runtime uses role simulation, true subagents, or a configurable fallback.
5. Preserve finite recursion, budget confirmation, technique trace, output contract, and navigable result closeout.
6. Run a representative resolution check.
7. Compare the representative runtime behavior with L1 golden behavior.

## Edge Cases

- Do not make true subagents mandatory.
- Do not allow runtime access to weaken the manual SKILL contract.
- Do not promote registry work merely because the command resolves.
- If adapter conventions are unclear, keep B-CLO-001 open and return a flag.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-012 | L2.1 | Add runtime adapter. | Adapter points to canonical SKILL and preserves closeout. |
| SWU-CLO-013 | L2.2 | Define runtime role execution policy. | Runtime states true-subagent support, role simulation fallback, and tournament limits. |
| SWU-CLO-014 | L2.4 | Validate runtime representative run. | Closeout includes observation fields, role policy, and output contract. |

## Verification

```bash
tools/arcanum --resolve /concept-layer-optimizer
```

Representative run review is required after resolution succeeds.

## Done When

- Command resolves through `tools/arcanum`.
- Runtime role policy is explicit.
- Representative run preserves closeout and result contract.
