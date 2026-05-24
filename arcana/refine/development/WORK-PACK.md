# WORK-PACK: Refine Sigil

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Initial development package and sigil package are present; promotion still needs experiment evidence. |
| complexity | medium | Adds one new Arcana sigil and clarifies the refinement loop contract. |
| outputMode | single-file | Scope is navigable in one package-local work-pack. |
| executionPackRef | n/a | Not required for this initial package. |
| layeringArtifactRef | [REFINE-INVOKE-DESIGN-PLAN.md](REFINE-INVOKE-DESIGN-PLAN.md) | Contains implementation layering. |
| activeLayerWindow | L0-L3 | Create initial package and examples; defer promotion evidence. |
| readinessProfile | pilot | Initial reusable package, not promotion-ready. |

## Objective Summary

- Objective: create the initial `refine` sigil package from the one-loop refinement seed.
- Primary inputs: define, interrogation, research decision, Distill review, design/plan, and Sigil Development handoff.
- Success condition: README, SKILL, examples, registry entry, and validation evidence exist and preserve ownership boundaries.

## Task Status Board

| Task ID | Goal | Layer | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| TASK-REFINE-001 | Create `refine` sigil package. | L0-L2 | [REFINE-SIGIL-DEVELOPMENT-HANDOFF.md](REFINE-SIGIL-DEVELOPMENT-HANDOFF.md) | ready | completed |
| TASK-REFINE-002 | Add examples and validation evidence. | L3 | README/SKILL | ready-after-TASK-REFINE-001 | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-REFINE-001 | TASK-REFINE-001 | handoff + design/plan | none | `arcana/refine/README.md`, `arcana/refine/SKILL.md` | Initial sigil contract exists and preserves boundaries. | review README/SKILL for required terms | sigil-development | ready |
| SWU-REFINE-002 | TASK-REFINE-002 | README/SKILL | SWU-REFINE-001 | `arcana/refine/examples/` | Examples cover seed proposal, existing work-pack preflight, and blocked goal handoff. | review example fields | sigil-development | ready-after-SWU-REFINE-001 |
| SWU-REFINE-003 | TASK-REFINE-002 | registry requirements | SWU-REFINE-001 | `registry/SIGILS.md`, `arcana/README.md` | `refine` is discoverable. | grep registry and Arcana README | local-fallback | ready-after-SWU-REFINE-001 |

## Blockers

| Blocker ID | Scope | Description | Next Action |
| --- | --- | --- | --- |
| none | n/a | No blocker for initial package creation. | n/a |

## Gate Checks

1. `refine` delegates through Task Session.
2. `refine` references `REFINEMENT-LOOP.md` rather than duplicating loop mechanics.
3. Research offer is mandatory.
4. Codex Goal is default runtime route.
5. Unsafe Codex Goal handoff blocks.
6. Sigil Development owns promotion readiness.

## Next Route

Use `sigil-development` plus Experiment Harness for promotion evidence. Use `task-session` for future implementation or hardening SWUs:

```text
/task-session to arcana/refine/development/WORK-PACK.md --swu SWU-REFINE-002 --runtime codex --via goal
```
