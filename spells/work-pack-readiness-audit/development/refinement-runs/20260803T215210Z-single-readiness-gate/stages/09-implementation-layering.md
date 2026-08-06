# Single-readiness-gate implementation layering

## Target

One semantic plan audit, followed by explicit selection and selected-unit live material admission, without a pre-execution Invoke Refresh/re-audit loop.

## L0 — Contract proof

- Decision question: after this layer, do we have a closed, schema-valid distinction between immutable plan semantics, mutable lifecycle state, selection, and mutation admission?
- Minimum unit: versioned Plan Semantic Manifest schema.
- Included: admission-timing profile, manifest constants, component/unit digests, runtime-pending state, selection request/receipt contracts.
- Deferred: runner and Task Session code.
- Exit evidence: schemas pass Draft 2020-12 validation; negative examples reject mutation authority and ambiguous identity.
- Promotion: only if legacy strict shapes remain valid.

## L1 — Repeatable plan producer

- Decision question: after this layer, can the audit deterministically produce the same semantic epoch across status-only byte changes and invalidate it for real plan changes?
- Minimum unit: selected-value normalizer plus opt-in v2 audit projection.
- Included: canonical JSON normalization, component digests, per-unit digest, pending-selection report, selection handoff, defect-only Refresh signals.
- Deferred: Task Session consumption.
- Exit evidence: repeated projection fixtures; status-only equivalence; command/write/graph mutation invalidation.
- Non-regression: v1 and strict v2 missing-material blocks remain byte-compatible.

## L2 — Safe selected-unit consumer

- Decision question: after this layer, can exactly one selected unit cross from semantic readiness to a single-use live admission without a second audit?
- Minimum unit: audit-owned plan-epoch verifier and Task Session receipt bridge.
- Included: current selector recomputation, lifecycle/dependency eligibility, explicit selection receipt, package identity, live target baselines, full validation contract, attempt binding, mutating-adapter receipt requirement.
- Deferred: broad rollout.
- Exit evidence: wrong-unit, stale-plan, stale-material, target-TOCTOU, dependency, replay, and adapter-bypass fixtures block.
- Non-regression: absence of material remains a mutation blocker.

## L3 — Integration and packaging

- Decision question: after this layer, is the cross-capability route reproducible, documented, and installable without private leakage?
- Minimum unit: end-to-end synthetic fixture from plan-once audit to terminal Task Session receipt.
- Included: fixture matrix, documentation, generated Codex/Claude package sync, Anime.js migration guidance.
- Deferred: default-profile change, v1 deprecation, multi-unit autonomous epochs.
- Exit evidence: canonical and generated fixture suites pass; public/private boundary review passes.

## Boundary heuristic

Each layer unlocks a distinct decision: contract validity → deterministic producer → safe consumer → reusable packaging. Combining L0–L2 would hide which side caused a safety failure; splitting their selected minimum units further would create schemas without a coherent identity or verifiers without an owned digest algorithm.

## Recommended next layer

L0 only. It is the narrowest reversible trust-building proof and introduces no runtime behavior.
