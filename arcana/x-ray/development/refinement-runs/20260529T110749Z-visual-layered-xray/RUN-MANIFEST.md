# Run Manifest: visual layered x-ray

| Field | Value |
| --- | --- |
| run_id | `20260529T110749Z-visual-layered-xray` |
| target | `arcana/x-ray` |
| status | `flag` |
| preset | `standard` |
| research | `bounded-research` |
| dispatch_id | `refine-xray-20260529T110749Z` |

## Required Artifacts

| Artifact | Path | Status |
| --- | --- | --- |
| Seed proposal | `REFINE-SEED-PROPOSAL.md` | pass |
| Dispatch route | `REFINE-DISPATCH.json` | pass |
| Runtime handoff | `RUNTIME-HANDOFF.md` | pass |
| Evidence index | `evidence-index.json` | pass |
| Result | `RESULT.md` | flag |

## Command Resolution

| Command | Status | Resolved File |
| --- | --- | --- |
| `context-builder` | pass | `.codex/commands/context-builder.md` |
| `invoke` | pass | `.codex/commands/invoke.md` |
| `interrogation` | pass | `.codex/commands/interrogation.md` |
| `distill` | pass | `.codex/commands/distill.md` |

## Stage Artifacts

| Stage | Owner | Status | Artifact |
| --- | --- | --- | --- |
| Context Builder evidence baseline | context-builder | pass | `stages/01-context-builder.md` |
| Invoke Define | invoke | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | interrogation | pass | `stages/03-interrogation-refine-review.md` |
| Research decision | refine | pass | `stages/04-research-decision.md` |
| Distill | distill | pass | `stages/05-distill.md` |
| Invoke Redefine / Design | invoke | pass | `stages/06-invoke-design.md` |
| Interrogation refine-design-review | interrogation | flag | `stages/07-interrogation-design-review.md` |
| Distill Repair | distill | pass | `stages/08-distill-repair.md` |
| Invoke Plan | invoke | pass | `stages/09-invoke-plan.md` |
| Final Interrogation and Synthesis | interrogation/refine | flag | `stages/10-final-interrogation-and-synthesis.md` |

## Validation

Dispatch validation passed with:

```bash
python3 formulae/dispatch-spec/scripts/validate-dispatch.py arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/REFINE-DISPATCH.json --json
```

Result: `validation=pass`, `blocks=[]`, `flags=[]`.

Command-surface dry-run receipts exist under `stages/*.dry-run.md`.
