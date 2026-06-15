# Run Manifest: Craft Ledger CSV And JSON Indexes

## Control

| Field | Value |
| --- | --- |
| run_id | `20260615T121512Z-craft-ledger-csv-json-indexes` |
| target | `arcana/craft` |
| skill | `refine` |
| status | `executed-with-flag` |
| mutation_scope | refinement run artifacts only |
| canonical_mutation | blocked until owner approval |
| research_mode | no-research |

## Files

| Path | Purpose |
| --- | --- |
| `REFINE-SEED-PROPOSAL.md` | Initial refined seed for CSV projections and JSON indexes. |
| `REFINE-DISPATCH.json` | Dispatch route for a full native Refine run. |
| `RUNTIME-HANDOFF.md` | Handoff for the next executor if the route is approved. |
| `RESULT.md` | Current strategy result and proposed implementation shape. |
| `evidence-index.json` | Source evidence used by this proposal. |
| `stages/STRATEGY-PREVIEW.md` | Non-executed stage preview. |
| `stages/subagent-findings.md` | Sidecar reviewer findings incorporated into the proposal. |
| `DEFINE.md` | Invoke Define artifact. |
| `INVOKE-DESIGN.md` | Invoke Design artifact. |
| `INVOKE-PLAN.md` | Invoke Plan artifact. |
| `IMPLEMENTATION-LAYERING.md` | Layering model for executable SWUs. |
| `WORK-PACK.md` | Work-pack and SWU manifest. |
| `stages/S01-CONTEXT-BUILDER.md` | Context-builder receipt. |
| `stages/S02-INVOKE-DEFINE.md` | Invoke Define receipt. |
| `stages/S03-INTERROGATION-REFINE-REVIEW.md` | Refine-review receipt. |
| `stages/S04-RESEARCH-DECISION.md` | Research decision receipt. |
| `stages/S05-DISTILL.md` | Distill receipt. |
| `stages/S06-INVOKE-DESIGN-RECEIPT.md` | Invoke Design receipt. |
| `stages/S07-INTERROGATION-DESIGN-REVIEW.md` | Design-review receipt. |
| `stages/S08-DISTILL-REPAIR.md` | Distill repair receipt. |
| `stages/S09-INVOKE-PLAN-RECEIPT.md` | Invoke Plan receipt. |
| `stages/S10-FINAL-INTERROGATION-SYNTHESIS.md` | Final synthesis receipt. |
| `stages/execution-receipt.json` | Machine-readable execution receipt. |

## Boundary

This run lives in the public `arcanum` submodule. It must avoid private
workspace details and should only reference public Craft source files, public
example files already present under `arcana/craft`, and this run's own
artifacts.

## Next Gate

The refine loop is executed and stopped at design/plan. Owner approval is
required before mutating canonical Craft files such as
`SKILL.md`, `README.md`, `templates/ledger.schema.yml`, examples, runtime
mirrors, or generator scripts.
