# Invoke Define Transport Report

## Target Artifact Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Invoke mode | `define` |
| Target artifact name | `benchmark refine-distill-invoke validation definition` |
| Target artifact type | refinement target definition |
| Target owner / lifecycle cycle | `refine` run `20260527T093001Z-benchmark` |
| Output paths owned by target run | `benchmark/development/refinement-runs/20260527T093001Z-benchmark/invoke-define/` |
| Invoke-specific gaps | None blocking. |
| Target-artifact gaps | Downstream Refine stages still need to prove design, distill, plan, and final synthesis quality. |
| Recommended next route | `refine` |

## Template Selection Evidence

| Template Family | Eligible | Rationale |
| --- | --- | --- |
| `module-formulae` | no | The target is not a durable repository module specification; it is a run-local refinement validation definition. |
| `generic` | yes | The target needs objective, scope, source evidence, constraints, acceptance criteria, gaps, and next route without claiming a specialized lifecycle family. |
| `research` | no | No named evidence gap appeared; research is deferred by policy. |
| `architecture` | no | Design is a downstream stage; define should not emit the architecture artifact now. |
| `implementation-plan` | no | Plan is downstream and must wait for approved design/layering evidence. |
| `spell` | no | The target does not author or revise a spell. |
| `sigil` | no | The target does not author or revise a sigil. |
| `ux-plan` | no | No UX workflow or interface plan is requested. |

Selected template: `invoke.generic` with run-local companion artifacts for glossary, implementation-layering seed, and transport report.

## Decisions

| Decision | Outcome | Evidence |
| --- | --- | --- |
| Mode | `define` | User request: `define refinement target=benchmark`. |
| Preset | `standard` | Seed proposal runtime configuration. |
| Context source | Existing context-builder handoff | Context-builder status is `pass`; strict coverage is `pass`. |
| Mutation policy | Non-mutating run-local artifact authoring only | Seed source request and context-builder write scope. |
| Benchmark scores | Historical evidence only | Seed forbids recomputing scores. |
| Research | Deferred | No named gap appeared. |

## Validation

| Check | Result |
| --- | --- |
| Core goal identified | pass |
| Context-builder baseline available | pass |
| Template eligibility recorded | pass |
| Glossary link statuses deterministic | pass |
| Implementation-layering downstream need recorded | pass |
| Benchmark source mutation required | no |

## Unresolved Gaps

| Gap ID | Owner | Description | Next Route |
| --- | --- | --- | --- |
| G-001 | `refine` | Downstream stages must validate interrogation, distill, design, repair, plan, and synthesis behavior. | Continue Refine loop. |
| G-002 | `refine` | Prior run blocked at Invoke Define; current define pass should be preserved as evidence, not treated as proof of full-loop success. | Carry to final synthesis. |

## Necronomicon Transport

- Status: no-op
- Rationale: No matching Necronomicon section was selected in the context-builder evidence baseline, and direct upstream mutation was not approved.
