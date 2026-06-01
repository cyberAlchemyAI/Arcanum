# Glossary And Ontology: Benchmark Refine-Distill-Invoke Validation

This glossary is the terminology authority for the current Invoke Define output. Terms are candidate terms for this refinement run and are not promoted into a canonical repository glossary.

## Plain Language Terms

| Term | Meaning In This Run | Related Concepts |
| --- | --- | --- |
| Completed benchmark smoke evidence | Existing benchmark campaign, score, and audit artifacts already produced before this refinement run. | Completed Evidence Baseline |
| Non-mutating validation | Validation that inspects and authors around existing artifacts without changing benchmark source, fixtures, tests, scores, or raw outputs. | Boundary Enforcement |
| Authoring loop | The Refine-driven sequence that uses Invoke and Distill to shape definition, design, plan, and synthesis artifacts. | Authoring Loop |
| Smallest validation unit | The narrowest useful question the run should validate before expanding scope. | Smallest Validation Unit |

## Formal Terms

| Term | Category | Definition | Source Or Rationale | Linked Authority Concepts | Link Status | No Match Reason | Usage References | Status | Created At | Updated At |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Refinement Target | system | The bounded subject of the current Refine run, set to `benchmark`. | Seed proposal target and context-builder identity. | `benchmark` run target | linked |  | `spec.md#Mission` | candidate | 2026-05-27 | 2026-05-27 |
| Completed Evidence Baseline | system | The persisted benchmark work-pack, smoke campaign, and verification audit artifacts used as source evidence. | Context-builder obligations O2 and O3. | Benchmark closure artifacts | partial | No single canonical concept ID exists in this run. | `spec.md#Source Evidence` | candidate | 2026-05-27 | 2026-05-27 |
| Authoring-Loop Validation | system | A check that Refine, Invoke, and Distill can produce coherent governed authoring artifacts from completed benchmark evidence. | Seed source request and context-builder architecture guidance. | Refine, Invoke, Distill contracts | partial | The combined loop is a run-local validation concept. | `spec.md#Capabilities` | candidate | 2026-05-27 | 2026-05-27 |
| Boundary Enforcement | system | The rule that this run may write refinement artifacts but must not mutate benchmark source, fixtures, tests, score artifacts, or official raw outputs. | Seed source request and context-builder write scope. | Context-builder constraints | linked |  | `spec.md#Constraints And Non-Goals` | candidate | 2026-05-27 | 2026-05-27 |
| Stage Artifact | system | A command-owned artifact emitted under the current refinement run folder for a specific Refine stage. | Refine stage dispatch contract and seed validation surface. | Native stage evidence | linked |  | `spec.md#Acceptance Criteria` | candidate | 2026-05-27 | 2026-05-27 |
| Smallest Validation Unit | shared | The minimal coherent validation question: whether Refine can turn completed benchmark smoke evidence into a bounded, non-executed validation design for Arcanum. | Context-builder architecture guidance and Distill boundary. | Distill optimization boundary | partial | Run-local phrasing, not a canonical Distill term. | `spec.md#Concept Model` | candidate | 2026-05-27 | 2026-05-27 |
| Research If Gap Appears | system | The research policy that external research is deferred unless a named local evidence gap appears. | Seed runtime configuration and Refine research policy. | Refine research policy | linked |  | `transport-report.md#Decisions` | candidate | 2026-05-27 | 2026-05-27 |

Allowed link status values used: `linked`, `partial`, `no-match`.

## External Terms

| Term | Source Scope | Definition In This Run | Source Reference |
| --- | --- | --- | --- |
| Refine | Arcanum skill/runtime | Owns the refinement loop and downstream stage sequencing for this run. | `arcana/refine/SKILL.md` |
| Invoke | Arcanum spell | Owns definition, design, plan, handoff, and refresh authoring artifacts, not benchmark lifecycle execution. | `.codex/commands/invoke.md`, `spells/invoke/define.md` |
| Distill | Arcanum skill | Owns smallest-coherent-unit optimization inside the refinement loop. | `arcana/distill/SKILL.md` |

## Maintenance Rules

- Keep terms candidate-scoped to this refinement run unless a separate glossary-governance action promotes them.
- Update usage references when downstream stage artifacts are materialized.
- Do not define new benchmark behavior in this glossary.
