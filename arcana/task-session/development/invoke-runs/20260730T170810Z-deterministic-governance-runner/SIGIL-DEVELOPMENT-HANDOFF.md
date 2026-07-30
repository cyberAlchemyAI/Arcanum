# Sigil Development Handoff

## Request

Update the existing `task-session` sigil with the proposed deterministic governance
runner. Start with `SWU-TSGR-000`: accept, narrow, or reject the lifecycle design.

## Selected package

- definition: `SPEC.md`
- architecture: `ARCHITECTURE.md`
- selection receipt: `DESIGN-SELECTION-RESULT.json`
- layer governance: `IMPLEMENTATION-LAYERING.md`
- canonical executable plan: `WORK-PACK.md`
- choreography: `EXECUTION-PACK.md`
- closeout control: `work-pack/shared/EXECUTION-CONTROL.md`

## Exact first decision

Decide whether Task Session may add a bounded, local, checkpointed CLI that owns
phase ordering and receipt joins while retaining separate implementation,
Continuation Router, Invoke, Signal Observer, and lifecycle owners.

## Required lifecycle constraints

- Update existing sigil; do not create a competing sigil.
- Preserve one-SWU execution ceiling.
- No recursive successor execution.
- No arbitrary shell interpolation.
- No consuming-project content in public fixtures or docs.
- Preserve current dirty Task Session work; bind exact live digests per SWU.
- First implementation SWU is the read-only production evaluator.
- This prototype work pack ends at an experiment-backed pilot verdict; canonical
  documentation and generated mirrors require a later lifecycle package.

## Return shape

```yaml
swu_id: SWU-TSGR-000
decision: accept | narrow | reject
accepted_boundaries: []
narrowing: []
affected_swus: []
implementation_gate: pass | block
next_route: invoke-refresh | task-session | none
```
