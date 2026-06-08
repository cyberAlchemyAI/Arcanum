# Refinement Loop

## Identity

- Owner: `refine`
- Status: pilot
- Use for: concept, architecture, ontology, lifecycle, governance, research-informed synthesis, article-quality design, repository-area understanding, and unclear refinement targets.
- Avoid for: already-approved implementation tasks, simple direct edits, lifecycle promotion, or tasks that already have a selected execution-ready SWU.

## Objective

Run bounded discovery and design refinement. The loop turns a vague target or design concern into a refined seed, design, non-executed plan, and final synthesis that can recommend a next route.

## Ownership Boundary

- Refine owns target understanding, research decision, loop budget, seed proposal, dispatch request, runtime handoff, run manifest, evidence index, final synthesis, and recommended next routes.
- Dispatch Spec owns route-shape validation for the canonical loop, technique references, gates, handoffs, and observability grouping.
- Context Builder owns the evidence baseline and runtime handoff pack outputs.
- Invoke owns the phase artifacts it is asked to produce: define, design, and plan.
- Interrogation owns critique, blocker questions, and pass/flag/block verdicts.
- Distill owns coherent-unit selection, optimization, repair, and validate passes.
- Research is bounded evidence gathering. It cannot override local repo evidence.
- Task Session and Sigil Development are possible next routes after refinement; they are not loop stages.

## Execution Rule

Refine first writes `REFINE-DISPATCH.json`, a dispatch-spec route for the canonical ten-stage loop. That route must validate before runtime-backed stages run.

The dispatch route records stage order, capability owners, mode/configuration, inputs, outputs, gates, observability events, route-menu decisions, native receipts, and technique references from `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`.

Refine then runs runtime-backed stages through parent-owned native runtime execution. Deprecated command files, slash commands, and command-resolution checks are not active success gates. A stage passes only when it records a native receipt from the owning capability, an approved subagent receipt, or an explicit blocked reason.

`tools/arcanum` may still prepare deterministic handoff contracts or explicit legacy adapter runs, but that compatibility surface is outside the native Refine success gate. The loop is not valid if execution merely labels hand-written prose as Context Builder, Invoke, Interrogation, or Distill output, or if `REFINE-DISPATCH.json` is missing for a materialized run.

Each dispatched stage must preserve:

- the capability handle,
- the receipt kind,
- the runtime surface,
- the requested mode/configuration,
- the stage artifact path,
- the stage observation envelope or invocation summary when available,
- the receipt artifact or structured receipt fields,
- a pass/flag/block verdict when the stage provides one,
- or an explicit blocked reason when the native capability is unavailable.

## Required Local Baseline

1. Build or consume a bounded context pack first.
2. Treat the context pack as the local evidence baseline.
3. Use context gaps and uncovered obligations to guide any extra local search.
4. Do not redo broad repository discovery unless the pack is missing required evidence.
5. If context coverage cannot support a coherent seed, return `BLOCK`.

## Canonical Default Loop

Every refine run uses this stage list. Presets tune budget/configuration; they do not remove stages.

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation using `refine-review`.
4. Research decision, with bounded research only when selected or triggered by a named gap.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation using `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Synthesis using `refine-final`.

## Stage Configuration

| Stage | Capability | Mode/Config | Output |
| --- | --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | `standard`; include `--strict --emit both --handoff runtime --persist <run-folder>/context-builder` | Context pack and index, or blocked coverage reason. |
| Invoke Define | `invoke` | `define` | Define artifact or blocked reason. |
| Interrogation | `interrogation` | `refine-review` | Critique verdict for define-stage output. |
| Research decision | `refine` | `no-research`, `bounded-research`, or `research-if-gap-appears` | Decision record and optional research notes. |
| Distill | `distill` | `standard` | Coherent-unit selection and optimization trace. |
| Invoke Redefine / Design | `invoke` | `design`, framed as redefine/design from previous artifacts | Design artifact or blocked reason. |
| Interrogation | `interrogation` | `refine-design-review` | Critique verdict for design-stage output. |
| Distill Repair | `distill` | `validate` or repair-focused request | Repair verdict, tensions, and selected repair. |
| Invoke Plan | `invoke` | `plan` | Non-executed plan artifact. |
| Final Interrogation and Synthesis | `interrogation` then `refine` | `refine-final` | Final verdict and Refine-owned synthesis. |

## Dispatch Technique Overlays

Refine dispatches should normally cite the baseline sequence techniques:

- `sequence`
- `frame_handoff`
- `handle_handoff`
- `validation_loop`
- `owner_boundary_check`
- `observability_grouping`
- `minimum_component_catalog`
- `mandatory_component`
- `conditional_component`
- `orphan_record_check`
- `data_quality_completeness`
- `data_quality_conformity`

Refine may add technique overlays when the target needs them:

| Overlay | Trigger | Techniques |
| --- | --- | --- |
| `route_menu_for_ambiguity` | Multiple plausible owners, routes, outputs, or research choices. | `route_menu`, `one_or_more_option_set`, `approval_checkpoint` |
| `dialectic_for_tension` | Competing principles, explore/exploit pressure, or likely disagreement. | `dialectic`, `zig_zag`, `residue_ledger` |
| `tournament_for_alternatives` | Several candidate abstractions, designs, or SWU boundaries need comparison. | `tournament`, `pareto_gate`, `recomposition_proof` |
| `xray_for_hidden_structure` | Hidden architecture, workflow, transformation, or relationship structure is the main uncertainty. | `x_ray`, `component_descriptor`, `entity_component_reference` |
| `toy_game_for_low_cost_falsification` | A selected abstraction needs low-cost failure testing before planning. | `toy_game`, `validation_loop`, `assessment_failure_reference` |
| `memory_residue_for_context_recovery` | Prior sessions, rejected candidates, or repository memory matter. | `memory_loop`, `residue_ledger`, `data_quality_deduplication` |
| `protected_context_for_external_or_sensitive_evidence` | External, sensitive, or non-canonical evidence is used. | `protected_context_flag`, `system_agnostic_standard`, `local_nuance_coordination` |

Additional techniques may be cited when the route actually uses them. Technique citations without step, gate, route-menu, observability, or validation consequences should be treated as `flag`.

## Presets

| Preset | Budget Effect | Use When |
| --- | --- | --- |
| compact | Shortest stage outputs and leanest acceptable context. | The target is narrow and mostly local. |
| standard | Default stage depth and standard Context Builder/Distill budget. | The target needs critique and repair but not maximal exploration. |
| full | Deeper stage requests, stronger design/plan detail, and more explicit repair evidence. | Architecture, lifecycle, governance, or multi-artifact development needs a strong result. |
| deep | Full behavior plus checkpointing before expensive or mutation-heavy next-route recommendations. | The target is high-risk, broad, or likely to span several follow-up tasks. |

## Loop Limits

- Context Builder: at most 1 pass.
- Invoke: at most 3 passes.
- Interrogation: at most 3 passes.
- Distill: at most 2 passes.
- Bounded online research: at most 1 pass.

If the same disagreement appears twice without new evidence, stop and record it as an open decision.

## Research Bounds

When research is selected:

- use at most 8 external sources,
- use max depth 2,
- prefer standards, research papers, official docs, mature OSS architecture docs, and well-cited essays,
- record what each useful source contributes,
- record what does not fit the local domain,
- label influence as evidence, analogy, or rejected alternative,
- never let online research override local repo evidence.

## Handoff Output

A completed refinement loop should produce either:

- a refined seed/design/plan result with recommended next routes,
- or a `BLOCK` report with the smallest missing context, decision, command, write scope, validation surface, or runtime handoff field.

The output must include required-stage evidence for every stage in the canonical loop.

## Run Manifest

Every materialized refinement run must produce a target-local run folder:

```text
<target>/development/refinement-runs/<run-id>/
```

Required contents:

- `RUN-MANIFEST.md`
- `evidence-index.json`
- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `RUNTIME-HANDOFF.md`
- `RESULT.md`
- `stages/`

The manifest is an index, not a replacement for stage artifacts. Each stage row must reference the artifact produced by its owning capability plus the native receipt, or record an explicit blocked reason. A selected stage without an artifact path or blocked reason is invalid. A stage marked `pass` must reference an artifact path or receipt that exists.
