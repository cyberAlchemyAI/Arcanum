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

| Stage | Capability | Capability source | Mode/config | Status | Artifact path | Receipt kind | Receipt artifact | Observer status | Verdict | Blocked reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Context Builder evidence baseline | context-builder | native capability | standard; --strict --emit both --handoff runtime | block |  | blocked |  |  | block | <reason> |
| Invoke Define | invoke | native capability | define | block |  | blocked |  |  | block | <reason> |
| Interrogation refine-review | interrogation | native capability | refine-review | block |  | blocked |  |  | block | <reason> |
| Research decision | refine | arcana/refine/SKILL.md | no-research \| bounded-research \| research-if-gap-appears | block |  | blocked |  | n/a | block | <reason> |
| Distill | distill | native capability | standard | block |  | blocked |  |  | block | <reason> |
| Invoke Redefine / Design | invoke | native capability | design | block |  | blocked |  |  | block | <reason> |
| Interrogation refine-design-review | interrogation | native capability | refine-design-review | block |  | blocked |  |  | block | <reason> |
| Distill Repair | distill | native capability | validate or repair-focused request | block |  | blocked |  |  | block | <reason> |
| Invoke Plan | invoke | native capability | plan | block |  | blocked |  |  | block | <reason> |
| Final Interrogation and Synthesis | interrogation + refine | native capability + refine synthesis | refine-final | block |  | blocked |  |  | block | <reason> |

## Notes

- This manifest references stage artifacts; it does not copy or redefine them.
- `REFINE-DISPATCH.json` is the route contract for the stage sequence and must validate before native runtime-backed stages run.
- A selected stage must have an artifact path or blocked reason.
- A stage marked `pass` must reference an artifact path or receipt artifact that exists.
- Task Session and Sigil Development are not loop stages; they may appear only as recommended next routes in `RESULT.md`.
