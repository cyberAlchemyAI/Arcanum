# Refine

Refine is an Arcana sigil for discovery and design refinement.

It is the front door for requests such as "refine this design," "use refinement on this folder," or "turn this vague target into a refined seed." It designs an initial seed, records research mode, emits a dispatch-spec route for the canonical refinement loop, runs or hands off that validated route through native runtime stage receipts, indexes stage evidence, and returns a final refined synthesis.

## Problem It Solves

Users often have a target, concern, folder, repository area, or rough idea, but not a refined model of what should be built, designed, planned, or deferred. Refine provides a governed discovery/design loop before any implementation or lifecycle promotion route is chosen.

## Use When

- a refinement target is vague or only points to a folder, idea, design, plan, or repository area,
- the user wants a budget and loop count before deeper design work,
- research should be offered and recorded before refinement,
- the result should include auditable stage evidence,
- possible next routes should be recommended after a final synthesis.

## Do Not Use When

- the user wants immediate execution of one approved task/SWU,
- the work only needs a direct edit,
- the user wants only Invoke design/plan without the refine loop,
- the user wants lifecycle promotion rather than discovery/design refinement.

## Ownership Model

| Capability | Owns |
| --- | --- |
| Refine | Seed design, research decision, dispatch request, runtime handoff, manifest/index, final synthesis, recommended next routes. |
| Dispatch Spec | Route-shape validation, technique references, gates, handoffs, and observability grouping. |
| Context Builder | Evidence baseline and runtime handoff context. |
| Invoke | Define, Design, and Plan artifacts. |
| Interrogation | Critique and readiness verdict artifacts. |
| Distill | Coherent-unit selection, optimization, and repair artifacts. |
| Runtime adapters | Adapter-specific execution status when a durable runtime run is dispatched. |

Task Session and Sigil Development may be recommended after refinement, but they are not stages in the refine loop.

## Refinement Loop

The canonical loop is defined in [Refinement Loop](REFINEMENT-LOOP.md):

```text
Context Builder evidence baseline
  -> Invoke Define
  -> Interrogation
  -> Research decision / bounded research when selected or triggered
  -> Distill
  -> Invoke Redefine / Design
  -> Interrogation
  -> Distill Repair
  -> Invoke Plan
  -> Final Interrogation and Synthesis
```

Every materialized run first writes `REFINE-DISPATCH.json`, validated by [Dispatch Spec](../../formulae/dispatch-spec/README.md). The dispatch route carries the canonical stage order, command owners, modes, handoffs, gates, trace events, route-menu decisions, and technique references.

Refine can select Dispatch Spec technique overlays while preserving the canonical ten-stage loop:

- baseline sequence for ordinary refinement,
- route menu for ambiguous route or owner choices,
- dialectic for competing principles,
- tournament and Pareto gates for alternative designs or abstractions,
- x-ray for hidden structure,
- toy-game validation for low-cost falsification,
- memory/residue recovery for prior context,
- protected-context handling for external or sensitive evidence.

Technique overlays must change evidence, gates, stage configuration, or recommended next routes. Unused technique labels are validation drift.

Every runtime-backed stage in the validated dispatch must use parent-owned runtime dispatch. Refine first resolves deterministic capability handles locally:

```bash
tools/arcanum --resolve <capability-id>
```

When a handoff artifact is useful, Refine can ask the deterministic tool surface for a native runtime receipt contract. The stage still runs through the parent native skill/subagent surface:

```bash
tools/arcanum --exec --adapter native-skill --output <stage-output> <capability-id> <stage-request>
```

For native adapters, `tools/arcanum --exec` prepares the handoff and receipt contract; it does not spawn nested model-backed CLIs. `codex-exec` and `codex-bypass` remain explicit legacy opt-in adapters.

The manifest records the owning capability, resolved capability handle, runtime adapter, requested mode/config, stage output path, observer status, verdict, and blocked reason.

## Research Decision

Refine always records a research decision:

- `no-research`: local repository and supplied context only.
- `bounded-research`: one external comparison pass within the loop's research bounds.
- `research-if-gap-appears`: default; start local-first and ask again only if a named gap appears.

External research never overrides local repository evidence.

## Output

When a refinement run is materialized, Refine writes a target-local run folder:

```text
<target>/development/refinement-runs/<run-id>/
```

That folder contains:

- `RUN-MANIFEST.md`
- `evidence-index.json`
- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `RUNTIME-HANDOFF.md`
- `RESULT.md`
- `stages/`

The manifest references artifacts produced by Context Builder, Invoke, Interrogation, and Distill. It does not duplicate those artifacts.

## Lifecycle Evidence

`refine` is a pilot sigil. Its Experiment Harness lives under [development/](development/):

```text
development/run-example-with-codex.sh next
development/run-validation-fixtures.sh
development/write-experiment-report.sh
```

Promotion requires realistic live outputs for seed proposal, research decision, valid dispatch route, runtime handoff, valid manifest/index evidence, deterministic `tools/arcanum` stage dispatch evidence, and final synthesis. Proposal-only output is preflight evidence, not completed refinement evidence.
