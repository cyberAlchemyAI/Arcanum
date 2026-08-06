# Stage 02 — Invoke Define

## Problem definition

The current audit collapses two clocks:

1. **Plan clock** — whether the work pack, graph, commands, writes, receipts, closeout, and immutable source frontier form a valid execution contract.
2. **Execution clock** — whether the exact selected SWU has a current material package and producer receipt immediately before mutation.

Because the global verdict requires both clocks to pass for every unit, a plan whose contract is complete but whose packages are intentionally produced just-in-time is routed to Invoke Refresh and must be audited again.

## Defined target

Add an opt-in, backward-compatible **plan-then-admit** profile to the v2 objective-execution projection. It emits one immutable `PlanSemanticManifest` when plan and terminal-receipt contracts pass. The manifest hashes normalized selector values for the semantic owner, graph, writes, validation, receipt, closeout, runtime, and risk components; whole-file provenance hashes and mutable lifecycle/status receipts remain visible but do not define semantic equivalence. Units without material packages become `runtime-pending`, not plan defects. After explicit selection, Task Session consumes the manifest and performs the existing live material admission for only the selected unit.

## Invariants

1. `PlanSemanticManifest` never selects a unit and always has `authority_effect=none` and `mutation_ready=false`.
2. Missing material is non-blocking only in the opt-in plan-then-admit profile.
3. Any plan, graph, command, schema, write, receipt, closeout, dependency, authority, or snapshot defect still blocks readiness.
4. Task Session must bind the selected SWU to the receipt's ready frontier.
5. Task Session must recompute the selected semantic values from current selector bindings and compare their component digests with the manifest; changing only status/lifecycle receipts must not invalidate semantic readiness.
6. Material package, producer receipt, validation surface, write partitions, ownership, authority, publication, and dependency frontier remain live-admission requirements.
7. Semantic drift blocks before mutation and requires a new readiness audit; material absence, later material creation, or closeout-only status projection changes do not.
8. Existing v1 and strict v2 full-frontier behavior remain unchanged.
9. Invoke Refresh remains the repair owner for actual plan defects and Task Session closeout synchronization, not for expected runtime-pending material.

## Terms

- **plan-ready**: immutable authoring and receipt contract passed; not selected and not mutation-ready.
- **runtime-pending**: the plan is ready, but selected-unit live admission has not occurred.
- **runtime-admitted**: Task Session's current verifier returned `admit` for the explicitly selected SWU.
- **semantic plan drift**: a normalized selected plan value no longer matches its component digest; a whole-file byte change outside the selected plan semantics is provenance drift, not automatically semantic drift.
- **material drift**: the material tuple no longer matches current controls, dependencies, writes, validation, or owner boundaries.

## Non-goals

- Producing material packages during the audit.
- Selecting an SWU automatically.
- Letting a readiness receipt authorize mutation.
- Removing Task Session's material verifier.
- Removing Invoke Refresh from closeout or genuine plan repair.
- Replacing existing v1 or v2 strict full-frontier semantics.

## Define verdict

`pass`. The target, ownership split, compatibility boundary, and falsifiable safety invariants are explicit.
