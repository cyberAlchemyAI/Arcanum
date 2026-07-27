# TASK-DCC-METRICS: Honest Measurement And Safe Reuse

## Task Objective

Separate byte, tokenizer, and runtime usage claims, then prove cache
invalidation and base/delta reuse fail closed.

## Mapping

- Layer: L2
- Slices: S-005 and S-006
- Wave: W4
- Dependencies: SWU-DCC-004
- Blockers: `G-003`; `G-004` and `G-006` remain deferred
- Selection: `none`

## SWU-DCC-005: Evidence-Separated Payload Measurement

### Primary Behavior

Always record payload bytes, optionally record exact counts from one named
tokenizer, and accept actual prompt usage only through a runtime receipt.

### Independent Acceptance Boundary

Unavailable tokenizer or runtime usage stays `not_available` or `unknown`;
neither is inferred from bytes.

### Split Analysis

Tokenizer plugins and runtime adapters are separate future surfaces. This SWU
owns only the shared measurement schema and one optional tokenizer adapter,
which is the smallest unit that prevents false precision.

### Source Anchors

- `SPEC.md`: FR-11 and Failure Contract
- `ARCHITECTURE.md`: Usage receipt interface, R-005
- `WITNESS-CONTRACTS.md`: DCC-FIX-009, DCC-VAL-USAGE

### Exact Write Scope

1. `transmutations/context-builder/schemas/runtime-usage-receipt.schema.json`
2. `transmutations/context-builder/scripts/measure_context_payload.py`
3. `transmutations/context-builder/development/fixtures/usage/bytes-only.json`
4. `transmutations/context-builder/development/fixtures/usage/missing-tokenizer.json`
5. `transmutations/context-builder/development/fixtures/usage/runtime-receipt.json`
6. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-005/baseline.json`
7. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-005/task-session-receipt.json`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-005/owner-receipt.json`

### Done Criteria And Evidence

- bytes are deterministic and always present;
- tokenizer ID and version accompany exact tokenizer counts;
- unavailable tokenizer passes only with an unavailable status;
- actual runtime tokens require a bound runtime receipt;
- DCC-FIX-009 passes.

Validation replays all three usage fixtures and validates receipt schema and
field provenance.

### Execution Owner And Expected Result

- Lifecycle owner: Sigil Development
- Execution owner after selection: one Task Session
- Expected result: measurement fields support claims no stronger than evidence

### Closeout Synchronization

- Baseline: exact eight-target inventory above
- Allowed deltas: `artifact_added`, `evidence_added`
- Owner validation: replay usage fixtures and inspect exact receipt fields
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-005/owner-receipt.json`
- Successor: `SWU-DCC-006`; selected false

## SWU-DCC-006: Cache Invalidation And Proved Base/Delta

### Primary Behavior

Reject corrupt or stale cached objects and emit a delta only when an exact
runtime base-pack receipt proves the base; otherwise emit the full payload.

### Independent Acceptance Boundary

Cache and base-proof decisions pass through explicit receipts and can be tested
without a live model or canonical sigil change.

### Split Analysis

Cache invalidation and base/delta proof both govern reuse but have different
stores. They remain one SWU because the acceptance boundary is singular:
no reused bytes enter a runtime payload without current proof. Cleanup and
provider-specific caching remain deferred.

### Dependencies

- SWU-DCC-005 passing owner receipt

### Source Anchors

- `SPEC.md`: FR-04, FR-10
- `ARCHITECTURE.md`: Content-Addressed Store, Data Lifecycle Extension, R-001, R-006
- `WITNESS-CONTRACTS.md`: DCC-FIX-010, DCC-VAL-CACHE

### Exact Write Scope

1. `transmutations/context-builder/scripts/compile_context_pack.py`
2. `transmutations/context-builder/scripts/validate_context_pack.py`
3. `transmutations/context-builder/development/fixtures/cache/corrupt-object.json`
4. `transmutations/context-builder/development/fixtures/cache/stale-source.json`
5. `transmutations/context-builder/development/fixtures/cache/proved-base.json`
6. `transmutations/context-builder/development/fixtures/cache/unproved-base.json`
7. `transmutations/context-builder/development/fixtures/expected/base-delta.receipt.json`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-006/baseline.json`
9. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-006/task-session-receipt.json`
10. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-006/owner-receipt.json`

### Done Criteria And Evidence

- stale and corrupt objects never count as hits;
- safe rebuild from current source is observable;
- strict failure is used when rebuild cannot validate;
- proved base emits a bound delta;
- unproved base emits full payload or strict block according to declared policy;
- DCC-FIX-010 and cache mutants pass.

### Execution Owner And Expected Result

- Lifecycle owner: Sigil Development
- Execution owner after selection: one Task Session
- Expected result: reuse improves cost without weakening freshness

### Closeout Synchronization

- Baseline: exact ten-target inventory above
- Allowed deltas: `artifact_added`, `artifact_changed`, `evidence_added`
- Owner validation: stale, corrupt, proved-base, and unproved-base replay
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-006/owner-receipt.json`
- Successor: `SWU-DCC-007`; selected false

## Synchronization Rules

The two SWUs are serial because they share the evidence vocabulary consumed by
base/delta receipts. Each requires an independent selection.

## Completion Evidence

This task closes only after both owner receipts pass.
