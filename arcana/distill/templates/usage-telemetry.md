# Distill Usage Telemetry

## Purpose

This template defines meaningful execution telemetry for Distill runs.

Telemetry is used for maintenance and reflection, not surveillance. A signal should exist only when it can drive a review question, validation update, or lifecycle decision.

## Meaningful Execution

A Distill execution is meaningful when all of these are true:

- the run confirms or infers a seed point,
- the run confirms a target context,
- the run names an objective-output artifact pair,
- the run selects a mode budget,
- at least one Proposer/Balancer pass or Validate-mode critique occurs,
- the run returns pass, flag, or block.

Do not emit full telemetry for casual mentions, abandoned setup, or a request that routes away before the sigil begins.

## Signal Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `capability_id` | yes | `distill` |
| `capability_kind` | yes | `sigil` |
| `tier` | yes | `arcana` |
| `run_id` | yes | Unique Distill child or direct run identifier and observer dedupe identity. |
| `invocation_source` | yes | `direct` or `invoked-by`. |
| `parent_run_id` | when invoked | Caller run identifier. |
| `caller_capability_id` | when invoked | Capability that invoked Distill, such as `invoke`. |
| `caller_mode` | when invoked | Caller mode that selected Distill. |
| `mode` | yes | `compact`, `standard`, `tournament`, `deep`, or `validate` |
| `target_context` | yes | Summary of context size and purpose. |
| `objective` | yes | Problem the run is solving. |
| `output_artifact` | yes | Artifact shape optimized by the run. |
| `output_artifact_revised` | yes | Whether discovery changed the artifact shape. |
| `proposal_tracks` | yes | Count and short role summary. |
| `role_execution` | yes | `true-subagents`, `role-simulation`, or `mixed`. |
| `recursive_rounds_completed` | yes | Count completed. |
| `recursive_round_budget` | yes | Selected budget. |
| `techniques_run` | yes | Technique IDs that ran. |
| `techniques_skipped` | yes | Technique IDs skipped with reason. |
| `verdict` | yes | `pass`, `flag`, or `block`. |
| `smallest_coherent_unit` | no | Selected unit when one exists. |
| `cycle_guard_triggered` | yes | True when a cycle/infinite-reduction guard fired. |
| `objective_output_drift` | yes | True when artifact drift occurred. |
| `navigation_closeout` | yes | `pass`, `flag`, or `block`. |
| `execution_evidence_status` | yes | `complete`, `partial`, or `unavailable`. |
| `execution_evidence_refs` | yes | Available request, runtime-event, execution-receipt, and validator-result references. |
| `evidence_emission_status` | yes | `complete`, `partial`, `failed`, `not-required`, or `not-configured`; stored as `evidence.emission_status` in the invocation envelope. |
| `telemetry_status` | yes | `recorded`, `failed`, or `not-configured`. |
| `next_route` | yes | Recommended lifecycle route. |
| `reflection_hint` | no | Optional reason a maintainer should inspect the run. |

## Invoked-By Telemetry

When Invoke or another capability runs Distill:

- Distill receives a distinct child `run_id`;
- the child row carries `parent_run_id`, caller capability, caller mode, and
  `invocation_source: invoked-by`;
- completed, partial, blocked, and failed meaningful child runs are observed;
- skipped or not-required routes are recorded only in caller telemetry;
- Signal Observer appends exactly one child row, deduped by the child run ID;
- the caller and child rows remain separate central-ledger events; and
- telemetry failure is reported as residue without changing either capability's
  substantive result.

## Direct Telemetry

For a meaningful direct Distill run:

- Distill owns the post-run append through
  `scripts/observe-direct-invocation.sh`;
- the envelope uses `invocation_source: direct` and has no caller lineage;
- Signal Observer deduplicates by the direct Distill run ID; and
- a skipped or abandoned setup emits no signal.

Direct and invoked routes must never both append the same run.

## Evidence-Emission Status

| Status | Meaning | Handoff Effect |
| --- | --- | --- |
| `complete` | The full accepted role/process event sequence resolves. | Evidence validation may continue; no authority is implied. |
| `partial` | At least one event exists, but the accepted sequence does not resolve. | Evidence-gated handoff blocks. |
| `failed` | Emission was configured but produced no usable event evidence. | Evidence-gated handoff blocks. |
| `not-required` | No downstream evidence gate applied to the run. | No evidence claim is made. |
| `not-configured` | Evidence was required but no usable event context was available. | Evidence-gated handoff blocks. |

This field reports producer state. It cannot change the Distill verdict,
validator result, or mutation authority.

## Invoke-Owned Versus Target-Owned Gaps

When Distill runs through `invoke`, classify gaps carefully:

| Gap Type | Owner | Example |
| --- | --- | --- |
| invocation setup missing | invoke | `invoke` did not pass a target artifact or mode request. |
| sigil contract drift | distill | Result omits role trace or navigation guide. |
| target artifact blocked | target owner | Architecture cannot close because product decision is missing. |
| runtime trace gap | runtime adapter | Adapter cannot tell whether true subagents or role simulation was used. |

## Reflection Thresholds

Trigger manual reflection when any threshold appears:

| Signal | Threshold | Review Question |
| --- | --- | --- |
| repeated `block` verdicts | 3 in 10 meaningful runs | Is the setup contract unclear or are users invoking the wrong sigil? |
| navigation closeout `flag` or `block` | 2 in 5 meaningful runs | Does the output contract need a clearer closeout template? |
| objective-output drift | 3 in 10 meaningful runs | Should first-turn artifact confirmation be sharpened? |
| missing evolution profile | 2 in 5 future-scale runs | Is the complexity balance rule too implicit? |
| technique overuse | one conditional technique appears in every run | Has a technique become hidden mandatory structure? |
| role trace mismatch | any true-subagent run differs from role-simulation trace shape | Does runtime policy need repair? |
| evidence emission `partial`, `failed`, or `not-configured` | any evidence-gated run | Is the runtime producer or evidence context incomplete? |

## Reflection Route

Reflection should route through sigil-development or workflow-reflect.

Reflection may propose:

- wording fixes,
- new examples,
- technique trigger tuning,
- output contract clarification,
- runtime adapter repair,
- registry hold or revision.

Reflection must not silently rewrite the core contract without validation rerun.
