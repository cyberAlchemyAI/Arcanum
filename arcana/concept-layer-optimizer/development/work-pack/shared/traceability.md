# Traceability: Concept Layer Optimizer Sigil Development

| Task | Layer | Micro-Layers | Slice | Source Contracts | SWUs |
| --- | --- | --- | --- | --- | --- |
| TASK-CLO-001 | L0 | L0.1, L0.4 | S-CLO-001 | SIGIL-HANDOFF, DESIGN-CONTINUATION-REVIEW | SWU-CLO-001, SWU-CLO-002 |
| TASK-CLO-002 | L0 | L0.2, L0.3, L0.4 | S-CLO-001 | SIGIL-HANDOFF, MODE-TECHNIQUE-SURFACE-DESIGN, techniques/README | SWU-CLO-003, SWU-CLO-004, SWU-CLO-005 |
| TASK-CLO-003 | L1 | L1.1, L1.2, L1.3 | S-CLO-002 | SIGIL-HANDOFF, IMPLEMENTATION-PLAN | SWU-CLO-006, SWU-CLO-007, SWU-CLO-008 |
| TASK-CLO-004 | L1 | L1.4 | S-CLO-002 | sigil-development SKILL, framework QUALITY-BAR | SWU-CLO-009 |
| TASK-CLO-005 | L2/L4 | L2.3, L4.1 | S-CLO-003 | sigil-development observability model | SWU-CLO-010, SWU-CLO-011 |
| TASK-CLO-006 | L2 | L2.1, L2.2, L2.4 | S-CLO-003 | SIGIL-HANDOFF runtime expectations | SWU-CLO-012, SWU-CLO-013, SWU-CLO-014 |
| TASK-CLO-007 | L3 | L3.1, L3.2, L3.3 | S-CLO-004 | registry rules, validation evidence | SWU-CLO-015, SWU-CLO-016, SWU-CLO-017 |
| TASK-CLO-008 | L4 | L4.1, L4.2, L4.3 | S-CLO-005 | workflow-reflect and sigil-development lifecycle | SWU-CLO-018, SWU-CLO-019, SWU-CLO-020 |

## Micro-Layer To SWU Map

| Micro-Layer | SWUs |
| --- | --- |
| L0.1 README Surface | SWU-CLO-001 |
| L0.2 SKILL Execution Contract | SWU-CLO-003 |
| L0.3 Balance And Complexity Contract | SWU-CLO-004 |
| L0.4 Navigation Closeout | SWU-CLO-002, SWU-CLO-005 |
| L1.1 Golden Runs | SWU-CLO-006 |
| L1.2 Technique Trigger Runs | SWU-CLO-007 |
| L1.3 Drift And Failure Runs | SWU-CLO-008 |
| L1.4 Validation Report | SWU-CLO-009 |
| L2.1 Command Surface | SWU-CLO-012 |
| L2.2 Role Execution Policy | SWU-CLO-013 |
| L2.3 Signal Schema | SWU-CLO-010 |
| L2.4 Runtime Validation | SWU-CLO-014 |
| L3.1 Candidate Metadata | SWU-CLO-015 |
| L3.2 Routing And Link Check | SWU-CLO-016 |
| L3.3 Promotion Recommendation | SWU-CLO-017 |
| L4.1 Reflection Signals | SWU-CLO-011 |
| L4.2 Maintenance Change Classes | SWU-CLO-018 |
| L4.3 Evolution Loop | SWU-CLO-019, SWU-CLO-020 |

## Layer Promotion Evidence

| Promotion | Required Evidence |
| --- | --- |
| L0 -> L1 | README.md and SKILL.md exist and pass package review. |
| L1 -> L2 | Examples and VALIDATION.md show pass/flag/block behavior. |
| L2 -> L3 | Runtime adapter resolves and representative run records observability closeout. |
| L3 -> L4 | Registry recommendation is recorded and docs links validate. |

## Micro-Layer Promotion Rule

Nested micro-layers promote only when their evidence still satisfies the parent layer's decision question. If a micro-layer adds detail that weakens the parent layer, return to the parent layer instead of promoting the micro-layer independently.

## Drift Watch

- If objective-output setup is omitted, return to TASK-CLO-002.
- If examples reveal unclear mode behavior, return to TASK-CLO-001 and TASK-CLO-002.
- If runtime supports true subagents, use them; if it does not, preserve the same trace through labeled role simulation.
- If registry approval is not explicit at the final gate, do not promote.
- If a nested layer creates new artifacts without improving execution, collapse it back into the parent SWU.
