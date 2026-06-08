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
- Final Interrogation and Synthesis: `pass | flag | block`

## Recommended Next Routes

- `<route or none>`

## Blocked Fields

- `<field>`: `<reason>`
