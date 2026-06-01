# Refinement Run Manifest

## Identity

- Run ID: `<run-id>`
- Target: `<target>`
- Refine loop: `arcana/refine/REFINEMENT-LOOP.md`
- Preset: `compact | standard | full | deep`
- Research mode: `no-research | bounded-research | research-if-gap-appears`
- Status: `pass | flag | block`

## Run Artifacts

- Evidence index: `evidence-index.json`
- Seed proposal: `REFINE-SEED-PROPOSAL.md`
- Dispatch route: `REFINE-DISPATCH.json`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Result: `RESULT.md`
- Stage artifacts: `stages/`

## Stage Evidence

| Stage | Command | Command file | Mode/config | Status | Artifact path | Observer status | Verdict | Blocked reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Context Builder evidence baseline | context-builder |  | standard; --strict --emit both --handoff runtime | block |  |  | block | <reason> |
| Invoke Define | invoke |  | define | block |  |  | block | <reason> |
| Interrogation refine-review | interrogation |  | refine-review | block |  |  | block | <reason> |
| Research decision | refine | arcana/refine/SKILL.md | no-research \| bounded-research \| research-if-gap-appears | block |  | n/a | block | <reason> |
| Distill | distill |  | standard | block |  |  | block | <reason> |
| Invoke Redefine / Design | invoke |  | design | block |  |  | block | <reason> |
| Interrogation refine-design-review | interrogation |  | refine-design-review | block |  |  | block | <reason> |
| Distill Repair | distill |  | validate or repair-focused request | block |  |  | block | <reason> |
| Invoke Plan | invoke |  | plan | block |  |  | block | <reason> |
| Final Interrogation and Synthesis | interrogation + refine |  | refine-final | block |  |  | block | <reason> |

## Notes

- This manifest references stage artifacts; it does not copy or redefine them.
- `REFINE-DISPATCH.json` is the route contract for the stage sequence and must validate before command-backed stages run.
- A selected stage must have an artifact path or blocked reason.
- A stage marked `pass` must reference an artifact path that exists.
- Task Session and Sigil Development are not loop stages; they may appear only as recommended next routes in `RESULT.md`.
