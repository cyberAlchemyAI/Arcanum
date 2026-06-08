---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/refine/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: refine
description: "Use when: turning a vague refinement target, design concern, folder, idea, repository area, or existing work-pack into a refined seed, design, or non-executed plan through the Arcanum refinement loop."
argument-hint: "<target> [--preset compact|standard|full|deep] [--research no|bounded|if-gap]"
tier: arcana
domain: refinement-governance
version: 0.2.0
origin: redesigned as discovery/design loop using dispatch-spec route contracts and native runtime handoff receipts
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash, Agent
---

# Sigil: Refine

<objective>
Design an initial refinement seed, emit a dispatch-spec route for the canonical Arcanum refinement loop, run or hand off the validated route through native runtime stage receipts, index each stage artifact, and return a final refined synthesis.
</objective>

<logic-type>
Arcana: discovery and design orchestration with research decision, critique, repair, non-executed planning, and auditable stage evidence.
</logic-type>

<required-capabilities>

Refine owns the seed, research decision, dispatch request, run manifest, evidence index, and final synthesis. Dispatch Spec owns route-shape validation. Stage capabilities own their native artifacts.

| Capability | Required For | Evidence Required |
| --- | --- | --- |
| `context-builder` | Build the evidence baseline and runtime handoff context. | Context pack path or blocked coverage reason. |
| `invoke` | Produce Define, Redefine/Design, and Plan artifacts. | Invoke artifact path, mode, capability handle, and verdict. |
| `interrogation` | Critique Define, Design, and final synthesis. | Interrogation artifact path, mode, capability handle, and pass/flag/block verdict. |
| `distill` | Select the coherent unit and run repair/validation before planning. | Distill artifact path, mode, selected unit or repair verdict, and rejected alternatives. |
| `dispatch-spec` | Validate the canonical stage route, technique references, gates, handoffs, subagent strategy, and observability grouping before execution. | `REFINE-DISPATCH.json`, validation status, blocked fields, cited techniques, subagent strategy, and permission state. |
| `runtime-handoff` | Prepare or validate the durable runtime handoff when available. | Runtime handoff path, adapter, run folder, or blocked reason. |

</required-capabilities>

<canonical-loop>

Every refine run uses this stage list. Presets tune budget, depth, and configuration; they do not remove stages.

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation using `refine-review`.
4. Research decision, with bounded research only when selected or triggered by a named gap.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation using `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine-owned synthesis using `refine-final`.

</canonical-loop>

<dispatch-spec-contract>

Every materialized refine run must write `REFINE-DISPATCH.json` before native runtime-backed stage execution. The dispatch must conform to `formulae/dispatch-spec/dispatch.schema.yml` and should cite applicable techniques from `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`.

The dispatch document replaces Refine as a freeform orchestrator. Refine defines the fixed canonical loop, research policy, and final synthesis, but the route artifact must carry:

- `dispatch_id` tied to the run id,
- raw operator intent and refinement objective,
- the ten canonical stages as ordered dispatch steps,
- stage owner, mode/configuration, inputs, outputs, runtime surface, and native receipt handles for each runtime-backed stage,
- gates for native capability handles, stage receipts, research confirmation, required artifact existence, owner-boundary preservation, and final synthesis readiness,
- observability trace events grouped by `dispatch_id`,
- a route menu or recorded route decision when more than one technique profile could apply,
- `subagent_strategy` describing whether role-bound sibling agents are none, recommended, required, or blocked,
- role, join-policy, receipt, context, and authorization details when subagents are recommended or required,
- selected technique overlays and why they were selected,
- baseline technique references such as `sequence`, `frame_handoff`, `validation_loop`, `owner_boundary_check`, `observability_grouping`, `minimum_component_catalog`, `conditional_component`, and `data_quality_completeness`,
- optional applied techniques such as `dialectic`, `zig_zag`, `tournament`, `pareto_gate`, `x_ray`, `toy_game`, `memory_loop`, `residue_ledger`, `protected_context_flag`, and `spell_candidate` when the target actually needs them.

If `dispatch-spec` cannot validate the route shape, the run is `block` before stage execution.

</dispatch-spec-contract>

<strategy-preview-and-permission>

Refine is the orchestrating front door. It asks Dispatch Spec for the route and
native runtime/subagent strategy, then shows the operator the strategy before any
runtime-backed stage or delegated subagent execution.

The preview must include:

- selected technique overlays,
- why each selected overlay applies to the target context,
- `subagent_strategy.status`,
- role list and ownership when subagents are recommended or required,
- join policy and receipt requirements,
- what will run next if permission is granted,
- what remains blocked or deferred if permission is denied.

If `subagent_strategy.status` is `recommended` or `required`, Refine must ask for
operator permission before spawning subagents or running runtime-backed stages.
If the operator declines or permission is unavailable, record
`authorization=blocked` or the blocked reason in `RUNTIME-HANDOFF.md` and stop
before execution. Dispatch Spec can recommend the strategy; it does not execute it.

</strategy-preview-and-permission>

<technique-overlay-policy>

Refine preserves the canonical ten-stage loop, but it may adapt the dispatch route with technique overlays. Overlays change stage configuration, validation expectations, gates, evidence requirements, or recommended next routes; they do not remove required stages.

Default overlay:

- `baseline_sequence`: use `sequence`, `frame_handoff`, `handle_handoff`, `validation_loop`, owner-boundary, observability, and POLE-inspired minimum-component/data-quality techniques for ordinary refinement.

Optional overlays:

- `route_menu_for_ambiguity`: use `route_menu`, `one_or_more_option_set`, and `approval_checkpoint` when route, owner, output, or research choice is ambiguous.
- `dialectic_for_tension`: use `dialectic`, `zig_zag`, and `residue_ledger` when the target has competing principles or likely disagreement.
- `tournament_for_alternatives`: use `tournament`, `pareto_gate`, and `recomposition_proof` when several plausible designs, abstractions, or SWU boundaries must be compared.
- `xray_for_hidden_structure`: use `x_ray`, `component_descriptor`, and `entity_component_reference` when hidden architecture, workflow, or relationship structure is the main uncertainty.
- `toy_game_for_low_cost_falsification`: use `toy_game`, `validation_loop`, and `assessment_failure_reference` when a selected abstraction needs a controlled failure test before planning.
- `memory_residue_for_context_recovery`: use `memory_loop`, `residue_ledger`, and `data_quality_deduplication` when prior sessions, rejected candidates, or repository memory are material to the result.
- `protected_context_for_external_or_sensitive_evidence`: use `protected_context_flag`, `system_agnostic_standard`, and `local_nuance_coordination` when external, sensitive, or non-canonical evidence is used.

Validation requirements:

- `dialectic` and `tournament` require roles and convergence criteria.
- `toy_game` and validation-shaped steps require an evidence artifact.
- `x_ray` requires an artifact or handle output.
- technique citations must be reflected in steps, gates, observability, route menu, or validation expectations.

</technique-overlay-policy>

<stage-receipt-contract>

Every executable stage in the validated dispatch must use parent-owned native runtime dispatch. A selected stage is complete only when it records a native receipt or an explicit blocked reason. The receipt may come from the parent coordinator, the owning native skill, an approved subagent, or a deterministic adapter handoff that is clearly outside the execution success gate.

Deprecated command files, slash commands, and command-resolution checks are not active Refine success gates. `tools/arcanum` may remain as explicit legacy compatibility or deterministic handoff preparation, but a missing command interface must not block a stage when the native capability is available through the current host runtime. Explicit legacy adapters such as `codex-exec` and `codex-bypass` remain opt-in only.

Before a stage runs, Refine must identify the owning capability handle and the expected receipt shape. If the capability is unavailable through the current native runtime, the stage is `block` and the blocked reason is recorded. Do not replace a required stage with freeform prose when its owner capability is available through the current native runtime.

For each stage, preserve:

- stage name,
- owning capability,
- capability handle,
- receipt kind,
- runtime surface,
- requested mode/configuration,
- output path,
- status and verdict,
- receipt artifact or structured receipt fields,
- observer status when available,
- blocked reason when no artifact exists.

</stage-receipt-contract>

<stage-configuration>

Default configuration:

- Context Builder: capability `context-builder`; mode `standard`; request includes `--strict --emit both --handoff runtime --persist <run-folder>/context-builder`.
- Invoke Define: capability `invoke`; mode `define`; input is `REFINE-SEED-PROPOSAL.md` plus Context Builder outputs.
- Interrogation 1: capability `interrogation`; mode `refine-review`.
- Research Decision: owner `refine`; mode `no-research`, `bounded-research`, or `research-if-gap-appears`.
- Distill: capability `distill`; mode `standard`.
- Invoke Redefine / Design: capability `invoke`; mode `design`; request explicitly frames the run as redefining/designing from prior artifacts.
- Interrogation 2: capability `interrogation`; mode `refine-design-review`.
- Distill Repair: capability `distill`; mode `validate` or an explicitly repair-focused request.
- Invoke Plan: capability `invoke`; mode `plan`; output is a non-executed plan artifact.
- Final Interrogation and Synthesis: capability `interrogation`; mode `refine-final`, followed by Refine-owned synthesis.

</stage-configuration>

<run-manifest-contract>

Every materialized refinement run must write a target-local evidence folder:

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

Refine owns this folder, the seed proposal, the dispatch request, the runtime handoff, the research decision reference, the final result, and the evidence index. Dispatch Spec owns route-shape validation. Stage capabilities own their own artifacts. The manifest and index reference those artifacts; they do not copy or redefine them.

A selected stage is invalid when it has neither an artifact path nor a blocked reason. A stage marked `pass` is invalid when its artifact path is missing or does not exist.

</run-manifest-contract>

<applicability>
Use this sigil when:

- the user asks to refine a target, idea, folder, design, plan, repository area, or work-pack,
- the target needs discovery, critique, repair, or design before execution,
- the user needs a budget, research mode, loop evidence, or final refined synthesis,
- a future Task Session, Sigil Development, or other route should be recommended only after refinement.
</applicability>

<non-applicability>
Do not use this sigil when:

- the user wants immediate execution of one already-approved task/SWU,
- the request is a trivial direct edit,
- the user wants only Invoke artifacts without the refine loop,
- the user wants lifecycle promotion rather than discovery/design refinement.
</non-applicability>

<inputs>
Expected inputs, if available:

- target folder, artifact, idea, design concern, plan, work-pack, or repository area,
- simple operator sentence such as "refine everything until we have an MVP-ready plan",
- desired preset: compact, standard, full, or deep,
- desired research mode: no, bounded, or if-gap,
- existing source context or constraints,
- preferred output location for seed artifacts.
</inputs>

<simple-operator-sentence-policy>

Refine must support a simple operator sentence as the primary user experience.
When the user says something like:

```text
$refine refine everything until we have an MVP-ready plan
```

Refine should infer:

- target: the current repository, folder, feature, or supplied scope called "everything";
- desired outcome: an MVP-ready non-executed plan;
- preset: `standard` unless the sentence implies compact/deep;
- research mode: `research-if-gap-appears` unless the user says otherwise;
- first action: propose the run strategy, not execute it.

The initial response must be a `Refine Run Strategy Proposal`. It must offer the
strategy that Dispatch Spec selected, explain why it fits the target context, and
ask for confirmation. It must not spawn subagents, execute stages, or start the
canonical loop before confirmation.

After the user confirms, Refine runs the approved refinement session. If the
approved `subagent_strategy.status` is `recommended` or `required`, the confirmed
run should spawn the proposed subagents through the current native runtime when
available and collect their receipts before parent synthesis. If subagents are
not available, record `subagent_execution=blocked` with the exact reason and
continue only if the approved strategy allows a non-subagent fallback.

</simple-operator-sentence-policy>

<ownership-boundary>

- Refine owns seed design, research decision, dispatch request, runtime handoff, manifest/index, final synthesis, and recommended next routes.
- Dispatch Spec owns route-shape validation for the canonical loop, technique references, gates, handoffs, and observability grouping.
- Context Builder owns the evidence baseline and handoff pack outputs.
- Invoke owns Define, Design, and Plan artifacts.
- Interrogation owns critique and readiness verdict artifacts.
- Distill owns coherent-unit selection, optimization, and repair artifacts.
- Runtime adapters own adapter-specific execution status when a runtime run is actually dispatched.
- Task Session and Sigil Development are optional recommended next routes, not refine loop stages.

</ownership-boundary>

<research-policy>
Refine must always record a research decision.

Options:

- `no-research`: use only local repository and supplied context.
- `bounded-research`: one external comparison pass within Refine Loop bounds.
- `research-if-gap-appears`: default; start local-first and ask again only if Interrogation or Distill identifies a named external-context gap.

External research requires explicit confirmation unless the user already selected bounded research for the run. External research cannot override local repository evidence.
</research-policy>

<preset-policy>
Presets tune budget and configuration; they do not remove stages.

- `compact`: shortest stage outputs, lean Context Builder if appropriate, local-first research decision, repair pass may block quickly.
- `standard`: default stage depth with standard Context Builder and Distill.
- `full`: deeper interrogation and distill requests, stronger design/plan output expectations.
- `deep`: full behavior plus checkpointing before expensive or mutation-heavy next-route recommendations.

If no preset is supplied, use `standard`.
</preset-policy>

<process>
1. Resolve the target and decide whether a new seed proposal is needed.
2. Create or update the target-local refinement run folder.
3. Write `REFINE-SEED-PROPOSAL.md` with target, source context, write scope, done criteria, validation surface, preset, research mode, and planned stage configuration.
4. Select dispatch technique overlays from the policy above, recording why each selected overlay applies or why it was not selected.
5. Write `REFINE-DISPATCH.json` as a dispatch-spec document for the canonical ten-stage loop, including route menu/decision, technique overlays, gates, handoffs, and observability.
6. Validate `REFINE-DISPATCH.json` against `formulae/dispatch-spec/dispatch.schema.yml` and the `dispatch-spec` validator/skill contract, or block with exact missing fields.
7. Show the Dispatch Spec strategy preview as `Refine Run Strategy Proposal`: inferred target/outcome, overlays, why they apply, subagent strategy, role ownership, join policy, receipts, runtime implications, and deferred work.
8. Ask permission to run the validated route. When subagents are recommended or required, permission must explicitly cover delegated subagent execution. Stop here until the operator confirms.
9. Write `RUNTIME-HANDOFF.md` with the runtime objective, validated dispatch reference, strategy permission state, adapter/run fields, blocked fields, and runtime status.
10. For each runtime-backed stage in the validated dispatch, identify the native capability handle and required receipt fields before execution.
11. Spawn approved subagents when the confirmed strategy recommends or requires them; collect role receipts before parent synthesis.
12. Dispatch approved stages through the parent native runtime surface. If a durable adapter handoff is needed, record it as compatibility or handoff preparation; do not count command-interface execution as the native stage proof.
13. Record every stage artifact, subagent receipt, or blocked reason in `RUN-MANIFEST.md` and `evidence-index.json`.
14. Run bounded research only when selected or when `research-if-gap-appears` is triggered by a named gap and the user confirms.
15. After final interrogation, synthesize `RESULT.md` from the seed, dispatch validation, subagent receipts, stage artifacts, research decision, distill repair, invoke plan, and final verdict.
16. Recommend next routes only after the final synthesis; do not execute them as part of refine.
</process>

<quality-bar>
A successful Refine run must:

- produce a clear seed proposal before stage execution,
- produce and validate `REFINE-DISPATCH.json` before runtime-backed stage execution,
- preserve the canonical ten-stage loop,
- select technique overlays based on target evidence rather than decorating the route with unused technique names,
- show the Dispatch Spec strategy and ask permission before runtime execution,
- stop after the strategy proposal until the operator confirms the run,
- use native capability handles and native runtime receipts for runtime-backed stages,
- collect subagent receipts when approved subagents are used,
- materialize a target-local run manifest and evidence index,
- record research mode and confirmation status,
- preserve each stage capability's native artifact ownership,
- cite dispatch techniques only when they are expressed by steps, gates, handoffs, or validation notes,
- block unavailable native capabilities or unsafe runtime handoff with exact missing fields,
- produce a final refined synthesis,
- keep Task Session and Sigil Development out of the loop except as optional next-route recommendations.
</quality-bar>

<observability>
For meaningful executions, emit or prepare a post-run signal through the local observability package when available.

Recommended signal fields:

- target,
- selected preset,
- selected research mode,
- research confirmation status,
- runtime handoff status,
- dispatch strategy status,
- subagent strategy status and authorization,
- native capability receipt status,
- run manifest path,
- evidence index path,
- runtime handoff path,
- final result path,
- blocked fields,
- recommended next routes.
</observability>

<promotion-gate>
Refine is promotion-ready only after experiment evidence shows:

- vague targets produce useful seed proposals,
- the ten-stage loop is represented in manifest/index evidence,
- runtime-backed stages produce native capability receipts or blocked reasons,
- blocked native capability or runtime execution records exact missing fields,
- bounded research choices are offered and recorded,
- the dispatch route validates before stage execution,
- the strategy preview and permission gate occur before runtime-backed or subagent execution,
- the simple operator sentence path produces a strategy proposal before execution,
- final synthesis is produced from stage artifacts rather than a route proposal,
- Task Session and Sigil Development are only next-route recommendations.
</promotion-gate>

<anti-patterns>
Avoid:

- treating Task Session or Sigil Development as refine loop stages,
- using a Task Session route artifact as refine's route artifact,
- replacing runtime-backed stages with hand-written prose,
- running external research without the selected mode and confirmation,
- marking refinement complete before final interrogation and synthesis,
- silently falling back from failed dispatch validation, failed runtime handoff, or failed native stage receipt.
- running runtime-backed stages or subagents before showing the Dispatch Spec strategy and receiving permission.
- treating a simple "refine everything" request as permission to run before the strategy proposal is confirmed.
</anti-patterns>

<output-contract>
For the initial strategy proposal, return:

```markdown
## Refine Run Strategy Proposal

- Target: <inferred target>
- Desired outcome: <for example, MVP-ready non-executed plan>
- Preset: compact | standard | full | deep
- Research: no-research | bounded-research | research-if-gap-appears
- Dispatch route: <path>
- Selected overlays: <ids and why each applies>
- Subagent strategy: <none | recommended | required | blocked>
- Proposed subagents: <roles, ownership, affected steps>
- Join policy: <policy>
- Receipt requirements: <fields>
- Runtime plan after confirmation: <summary>
- Deferred work: <items>
- Confirmation prompt: Confirm to run this strategy?
```

After confirmation and execution, return:

```markdown
## Refine Result

- Target: <target>
- Status: pass | flag | block
- Preset: compact | standard | full | deep
- Research: no-research | bounded-research | research-if-gap-appears
- Run manifest: <path>
- Evidence index: <path>
- Seed proposal: <path>
- Dispatch route: <path>
- Dispatch strategy: <selected overlays, why, subagent strategy status, roles, join policy, authorization>
- Runtime handoff: <path>
- Stage evidence:
  - Context Builder evidence baseline: <pass | flag | block>
  - Invoke Define: <pass | flag | block>
  - Interrogation refine-review: <pass | flag | block>
  - Research decision: <pass | flag | block>
  - Distill: <pass | flag | block>
  - Invoke Redefine / Design: <pass | flag | block>
  - Interrogation refine-design-review: <pass | flag | block>
  - Distill Repair: <pass | flag | block>
  - Invoke Plan: <pass | flag | block>
  - Final Interrogation and Synthesis: <pass | flag | block>
- Final synthesis: <summary or blocked reason>
- Recommended next routes: <items or none>
```
</output-contract>
