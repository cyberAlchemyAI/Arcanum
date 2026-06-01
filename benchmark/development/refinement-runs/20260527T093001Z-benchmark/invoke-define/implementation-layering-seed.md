# Implementation Layering Seed

## Scope

This is a define-stage seed, not an execution plan. It exists so later `plan`, `full`, or `validate` stages do not lose the layer boundary implied by the no-rerun/no-rescore constraint.

## Layer Decision Snapshot

| Layer | Purpose | Entry Evidence | Promotion Evidence | Status |
| --- | --- | --- | --- | --- |
| L0 Definition | Establish a bounded refinement validation target from completed evidence. | Seed proposal and context-builder strict coverage. | Invoke Define artifacts exist and pass validation. | current |
| L1 Design | Define how the authoring loop should validate coherence across Refine, Invoke, and Distill. | L0 define artifacts. | Design artifact maps stage responsibilities, evidence flow, and failure modes. | downstream |
| L2 Plan | Convert the approved design into non-mutating stage tasks and checks. | L1 design artifact. | Work-pack or plan maps every stage to acceptance evidence without benchmark reruns. | downstream |
| L3 Validate | Synthesize final run result from stage artifacts. | L2 plan and stage outputs. | Final manifest, evidence index, and result file exist and preserve source boundaries. | downstream |

## Promotion Rules

- L1 cannot claim benchmark score validity; it may only validate the authoring loop over already completed evidence.
- L2 cannot introduce benchmark execution tasks unless the user changes the no-rerun/no-rescore constraint.
- L3 must treat any mutation outside the run folder as a validation failure.
- External research remains blocked unless a named evidence gap appears and is approved.

## Known Risks

| Risk | Layer | Mitigation |
| --- | --- | --- |
| Downstream stages over-expand into a new benchmark implementation. | L1/L2 | Keep Distill focused on the smallest validation unit. |
| Plan stage accidentally turns historical validation scripts into runnable tasks. | L2 | Mark benchmark scripts as historical validation surface only. |
| Final synthesis hides stage-level gaps. | L3 | Carry unresolved gaps into final `RESULT.md` and evidence index. |
