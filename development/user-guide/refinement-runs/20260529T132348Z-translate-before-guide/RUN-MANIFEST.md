# Refine Run Manifest: Translate Before Guide

## Run

| Field | Value |
| --- | --- |
| Run ID | `20260529T132348Z-translate-before-guide` |
| Target | `development/user-guide/` |
| Objective | Decide whether Translate should be a separate sigil candidate before Guide. |
| Preset | `standard` |
| Research | `no-research` |
| Status | `pass-with-runtime-caveat` |

## Verdict

Create `Translate` before general `Guide`. Guide should call Translate rather than own vocabulary/domain bridging internally.

## Dispatch Validation

```text
VALIDATION=pass
DISPATCH=development/user-guide/refinement-runs/20260529T132348Z-translate-before-guide/REFINE-DISPATCH.json
SCHEMA=formulae/dispatch-spec/dispatch.schema.yml
```

## Command Resolution

| Command | Status | Evidence |
| --- | --- | --- |
| `context-builder` | resolved | `.codex/commands/context-builder.md` |
| `invoke` | resolved | `.codex/commands/invoke.md` |
| `interrogation` | resolved | `.codex/commands/interrogation.md` |
| `distill` | resolved | `.codex/commands/distill.md` |
| `refine` | resolved | `.codex/commands/refine.md` |
| `dispatch-spec` | missing | local command route absent |
| `runtime-handoff` | missing | local command route absent |

## Stage Evidence

| Stage | Status | Artifact |
| --- | --- | --- |
| Context Builder evidence baseline | pass | `stages/01-context-builder.md` |
| Invoke Define | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | pass | `stages/03-interrogation-refine-review.md` |
| Research decision | pass | `stages/04-research-decision.md` |
| Distill | pass | `stages/05-distill.md` |
| Invoke Redefine / Design | pass | `stages/06-invoke-design.md` |
| Interrogation refine-design-review | flag | `stages/07-interrogation-design-review.md` |
| Distill Repair | pass | `stages/08-distill-repair.md` |
| Invoke Plan | pass | `stages/09-invoke-plan.md` |
| Final Interrogation and Synthesis | pass | `stages/10-final-interrogation-and-synthesis.md`, `RESULT.md` |

## Owner Boundary

This run writes only refine-owned route-decision evidence under `development/user-guide/refinement-runs/20260529T132348Z-translate-before-guide/`.
