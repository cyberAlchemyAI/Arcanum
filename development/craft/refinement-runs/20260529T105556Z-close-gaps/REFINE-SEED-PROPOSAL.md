# Refine Seed Proposal: Close Craft Gaps Before Architecture Planning

## Target

`development/craft/`

## Operator Intent

Close gaps first before moving from the validated recursive-ledger MVP into broader Craft method architecture planning.

## Refinement Objective

Classify the current Craft gaps into:

1. gaps that are already closed by the recursive-ledger MVP,
2. gaps that must close before architecture planning,
3. gaps that should be folded into the architecture package,
4. gaps that should remain deferred side-thread work.

The output should prevent the next architecture plan from starting with stale blockers or vague gap ownership.

## Source Context

| Source | Role |
| --- | --- |
| [../../SESSION-LEDGER.md](../../SESSION-LEDGER.md) | Current gap ledger, decisions, and next move. |
| [../../LEDGER.md](../../LEDGER.md) | Validated recursive-ledger fixture and current context state. |
| [../../LEDGER-VALIDATION.md](../../LEDGER-VALIDATION.md) | Validation result and deferred future work. |
| [../../CRAFT-MVP-WORK-PACK.md](../../CRAFT-MVP-WORK-PACK.md) | Completed MVP task sequence and next route. |
| [../../CRAFT-INITIAL-DEFINITION.md](../../CRAFT-INITIAL-DEFINITION.md) | Broader Craft concept baseline. |
| [../../CRAFT-REFINE-RUNTIME-STRATEGY.md](../../CRAFT-REFINE-RUNTIME-STRATEGY.md) | Runtime/refine side-thread evidence. |
| [../../ARCANUM-SKILL-RUNTIME-HANDOFF.md](../../ARCANUM-SKILL-RUNTIME-HANDOFF.md) | Runtime interface handoff, outside Craft MVP acceptance. |

## Preset

`compact`

## Research Mode

`no-research`

External research is not needed. The relevant gaps are local artifact-state and lifecycle-routing gaps.

## Technique Overlay Selection

| Overlay | Selected | Reason |
| --- | --- | --- |
| `baseline_sequence` | yes | Ordinary refinement needs the canonical staged route and owner-boundary checks. |
| `route_menu_for_ambiguity` | yes | The main ambiguity is which gap route should happen before architecture. |
| `memory_residue_for_context_recovery` | yes | Prior session state and completed MVP evidence determine what is stale, closed, or deferred. |
| `dialectic_for_tension` | no | There is no unresolved principle conflict; this is a routing/closure pass. |
| `tournament_for_alternatives` | no | We are not selecting among multiple architecture designs yet. |
| `xray_for_hidden_structure` | no | Hidden structure is already exposed through the MVP ledger. |
| `toy_game_for_low_cost_falsification` | no | Validation evidence exists; no toy test is needed before gap triage. |
| `protected_context_for_external_or_sensitive_evidence` | no | No external or sensitive context is used. |

## Done Criteria

- Gap closure statuses are explicit.
- Architecture-blocking gaps are separated from architecture-owned inputs.
- Runtime/refine interface work remains a side-thread unless explicitly promoted.
- The next route is one bounded task or one invoke/refine target, not a vague "continue".

## Validation Surface

- Dispatch route shape validates against `formulae/dispatch-spec/dispatch.schema.json`.
- Any unavailable command-backed capability is recorded as a blocker.
- Final synthesis names recommended next routes without executing them.
