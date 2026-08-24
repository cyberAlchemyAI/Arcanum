## Outcome Brief

<Two to five plain-language sentences explaining what Refine tried to clarify,
what the refinement established or why it stopped, and why that matters.>

- Objective: `<what the run was trying to refine>`
- Result: `<what is now known, designed, planned, flagged, or blocked>`
- Why it matters: `<practical consequence for the operator or next owner>`

## Boundary and Next Decision

- Changed: `<refinement artifacts, evidence, or state changed>`
- Unchanged: `<implementation, authority, promotion, publication, deployment, or other explicit boundaries>`
- Open questions: `<remaining uncertainty or none>`
- User decision: `<exact decision needed or none>`
- Next action: `<next bounded action and owner>`

## Technical Details

# Refine Result

- Status: `pass | flag | block`
- Target: `<target>`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`
- Seed proposal: `REFINE-SEED-PROPOSAL.md`
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass | flag | block`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Research mode: `no-research | bounded-research | research-if-gap-appears`
- Preset: `compact | standard | full | deep`
- Loop count: canonical default loop, budget tuned by preset
- Final synthesis: `<summary or blocked reason>`
- Execution designation: `execution-candidate | non-executing`
- Invoke Plan readiness binding: `INVOKE-PLAN-READINESS-BINDING.json`
- Implementation readiness: `<Invoke receipt path and pass | n/a with reason | block>`
- Exact acceptance: `<required next action | n/a>`
- Promotion evidence: `yes | no`

## Dispatch Evidence

- Dispatch ID: `<dispatch_id>`
- Techniques: `<applied technique ids>`
- Technique overlays: `<selected overlay ids and trigger evidence>`
- Gates: `pass | flag | block`
- Observability grouping: `<dispatch_id coverage>`

## Stage Evidence

- Context Builder evidence baseline: `pass | flag | block`
- Invoke Define: `pass | flag | block`
- Interrogation refine-review: `pass | flag | block`
- Research decision: `pass | flag | block`
- Distill: `pass | flag | block`
- Invoke Redefine / Design: `pass | flag | block`
- Interrogation refine-design-review: `pass | flag | block`
- Distill Repair: `pass | flag | block`
- Invoke Plan: `pass | flag | block`
- Invoke Plan readiness binding: `pass | not-applicable | block`
- Final Interrogation and Synthesis: `pass | flag | block`

## Recommended Next Routes

- `<route or none>`

## Blocked Fields

- `<field>`: `<reason>`
