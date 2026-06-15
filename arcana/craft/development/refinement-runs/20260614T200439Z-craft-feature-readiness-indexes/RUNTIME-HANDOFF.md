# Runtime Handoff

## Runtime Boundary

- Runtime: native Arcanum skill runtime
- Adapter: `parent-native-codex`
- Owner: `refine`
- Status: `flag`
- Runtime run folder: `arcana/craft/development/refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/stages/`

## Runtime Objective

Run the canonical Refine loop for the Craft execution-readiness index update and produce a lifecycle-ready design and work-pack.

## Dispatch Route

- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch schema: `formulae/dispatch-spec/dispatch.schema.yml`
- Dispatch validation: `pass`
- Dispatch ID: `20260614T200439Z-craft-feature-readiness-indexes`
- Technique catalog: `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- Technique overlays: `baseline_sequence`, `memory_residue_for_context_recovery`, `protected_context_for_external_or_sensitive_evidence`

## Permission State

- Runtime-backed stages: executed locally through parent-native Codex stage receipts.
- Subagent strategy: recommended by selected overlays.
- Authorization: full subagent spawning blocked because the available subagent tool policy requires an explicit user request for subagents, delegation, or parallel agent work.
- Fallback: parent-local role simulation for memory-residue and protected-context review.

## Handoff Requirements

- Select exactly one SWU before mutation-capable execution.
- Preserve public/private boundary when writing under the public `arcanum` submodule.
- Commit and push `arcanum` before any parent gitlink update if publication is requested.
- Run validation listed in the selected task contract before claiming pass.

## Blocked Fields

- Subagent receipts: no delegated subagents were spawned.
- Canonical source mutation: not performed by this Refine execution.
- Generated runtime surface sync: deferred until canonical source edits pass.

## Stage Receipts

- Context Builder: `stages/S01-CONTEXT-BUILDER.md`
- Invoke Define: `stages/S02-INVOKE-DEFINE.md`
- Interrogation refine-review: `stages/S03-INTERROGATION-REFINE-REVIEW.md`
- Research decision: `stages/S04-RESEARCH-DECISION.md`
- Distill: `stages/S05-DISTILL.md`
- Invoke Design receipt: `stages/S06-INVOKE-DESIGN-RECEIPT.md`
- Interrogation design review: `stages/S07-INTERROGATION-DESIGN-REVIEW.md`
- Distill repair: `stages/S08-DISTILL-REPAIR.md`
- Invoke Plan receipt: `stages/S09-INVOKE-PLAN-RECEIPT.md`
- Final synthesis: `stages/S10-FINAL-INTERROGATION-SYNTHESIS.md`
- Machine receipt: `stages/execution-receipt.json`
