# Refine Seed Proposal: Boundary Evidence Schema

Status: draft seed
Preset: standard
Research mode: no-research
Target: `formulae/dispatch-spec/`

## User Intent

Create a schema for the corrected evolution of `dispatch-spec`, then invoke a
new architecture and plan. The prior Tandem-specific interpretation should be
treated as drift. The target is Arcanum-native dispatch composition integrity:
boundary, evidence, authority, handoff, state, and promotion safety.

## Source Context

- `formulae/dispatch-spec/README.md`
- `formulae/dispatch-spec/dispatch.schema.json`
- `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- `formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- Prior refinement run:
  `formulae/dispatch-spec/development/refinement-runs/20260528T231321Z-expand-dispatch-techniques/`

## Correction

Do not design around Tandem. Remove Tandem as a motivating dependency from the
next architecture. Keep only the generally useful pressure: dispatch routes
need first-class structure for cross-capability boundaries, evidence handoff,
authority ownership, state namespace separation, and promotion safety.

## Candidate Schema Direction

Add a dispatch-owned boundary/evidence schema layer that can validate:

- boundary claims for delegated execution, cross-capability handoff, external
  artifact import, human approval, memory interaction, and observability return;
- authority ownership for lifecycle, execution, evidence, validation, memory,
  and promotion;
- receipt/evidence requirements without making dispatch an execution engine;
- state namespace boundaries between repository source, `.arcanum/` state,
  generated evidence, external artifacts, and runtime/workspace state;
- promotion guardrails that prevent temporary execution evidence from becoming
  canonical Inventory/Ontology knowledge without owner review.

## Write Scope

Refine may create design artifacts in this run folder. It should not mutate
the canonical schema or validator during refinement. Execution belongs to a
later task-session after the architecture and plan are reviewed.

## Done Criteria

- A schema seed is defined for boundary/evidence fields.
- Invoke Define, Design, and Plan artifacts are produced or their command
  blockers are recorded.
- Interrogation and Distill stages critique the schema direction.
- Final synthesis recommends the next execution route without performing it.

## Validation Surface

- Stage command resolution via `tools/arcanum --resolve`.
- Stage artifacts or explicit blocked reasons in `RUN-MANIFEST.md` and
  `evidence-index.json`.
- Non-executed plan only; no canonical schema mutation in this run.
