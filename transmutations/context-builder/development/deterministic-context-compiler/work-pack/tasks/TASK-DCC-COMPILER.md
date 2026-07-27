# TASK-DCC-COMPILER: Exact Compile And Deterministic Selection

## Task Objective

Build the smallest end-to-end compiler, then extend the same contracts to
deterministic multi-candidate deduplication and covering-set selection.

## Mapping

- Layers: L0 and L1
- Slices: S-002 and S-003
- Waves: W2 and W3
- Dependencies: SWU-DCC-001
- Blockers: `G-001` and `G-002`
- Selection: `none`

## SWU-DCC-002: Exact Single-Selector Compile

### Primary Behavior

Compile one admitted Markdown heading selector into one current source snapshot,
one immutable excerpt object, one runtime payload, and one validation receipt.

### Independent Acceptance Boundary

Identical inputs replay byte-identically; selected-source drift invalidates the
old binding; a repository escape never reads bytes.

### Split Analysis

Snapshot, object persistence, minimal rendering, and replay were considered as
children. They remain one L0 unit because removing any one loses the
end-to-end claim that a selected source becomes a reusable and runnable
receipt-bound payload. Multi-candidate selection is split into SWU-DCC-003.

### Source Anchors

- `SPEC.md`: FR-02, FR-03, FR-08
- `ARCHITECTURE.md`: Source Snapshotter, Excerpt Normalizer,
  Content-Addressed Store
- `WITNESS-CONTRACTS.md`: DCC-FIX-001, DCC-FIX-003, DCC-FIX-006

### Related Context

- [Shared context](../shared/CONTEXT.md)
- `transmutations/context-builder/schemas/context-request.schema.json`
- `transmutations/context-builder/schemas/context-pack-receipt.schema.json`

### Exact Write Scope

1. `transmutations/context-builder/scripts/compile_context_pack.py`
2. `transmutations/context-builder/development/fixtures/expected/single-selector.object`
3. `transmutations/context-builder/development/fixtures/expected/single-selector.payload.md`
4. `transmutations/context-builder/development/fixtures/expected/single-selector.receipt.json`
5. `transmutations/context-builder/development/fixtures/expected/single-selector.replay.json`
6. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-002/baseline.json`
7. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-002/task-session-receipt.json`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-002/owner-receipt.json`

### Done Criteria

- Compiler validates before cache access.
- Exact Markdown heading and whole-short-file policies are versioned.
- Object and output creation is atomic.
- Replay hashes match.
- Selected-source drift changes or blocks the pack; escape blocks.

### Acceptance Evidence And Validation

Run the compiler twice against `valid-single-selector.json`, compare all
declared output bytes, then execute selected-source-drift and path-escape
mutants. Record DCC-FIX-001, DCC-FIX-003, and DCC-FIX-006 results.

### Execution Owner And Expected Result

- Lifecycle owner: Sigil Development
- Execution owner after selection: one Task Session
- Expected result: the L0 smallest coherent design unit is executable

### Closeout Synchronization

- Baseline: exact eight-target inventory above
- Allowed deltas: `artifact_added`, `artifact_changed`, `evidence_added`
- Owner validation: replay compile, compare expected bytes, run two negative
  mutants, inspect scoped diff
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-002/owner-receipt.json`
- Successor: `SWU-DCC-003`; selected false

## SWU-DCC-003: Deduplicate And Select A Covering Set

### Primary Behavior

Given pre-mapped candidates, collapse byte-identical excerpts, union obligation
references, and choose a complete set using integer cost comparison and stable
lexical tie-breaking.

### Independent Acceptance Boundary

The selected set, exclusions, coverage, and diagnostics are byte-stable and can
pass without renderer parity, token plugins, or runtime delta behavior.

### Split Analysis

Deduplication and covering-set choice can be described separately, but each
changes the candidate set consumed by the other. Retaining them creates one
reviewable selection boundary; rendering is independently split to
SWU-DCC-004.

### Dependencies

- SWU-DCC-002 passing owner receipt

### Source Anchors

- `SPEC.md`: FR-05, FR-06, FR-07
- `ARCHITECTURE.md`: Covering-Set Selector and Decision Flow
- `WITNESS-CONTRACTS.md`: deterministic selection contract and DCC-VAL-COVERAGE

### Related Context

- [Traceability](../shared/TRACEABILITY.md)
- Existing compile and receipt schemas from SWU-DCC-001 and SWU-DCC-002

### Exact Write Scope

1. `transmutations/context-builder/scripts/compile_context_pack.py`
2. `transmutations/context-builder/development/fixtures/request/valid-duplicate-coverage.json`
3. `transmutations/context-builder/development/fixtures/request/valid-unrelated-drift.json`
4. `transmutations/context-builder/development/fixtures/request/invalid-ambiguous-selector.json`
5. `transmutations/context-builder/development/fixtures/request/invalid-uncovered-obligation.json`
6. `transmutations/context-builder/development/fixtures/request/invalid-budget-overflow.json`
7. `transmutations/context-builder/development/fixtures/expected/covering-set.receipt.json`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-003/baseline.json`
9. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-003/task-session-receipt.json`
10. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-003/owner-receipt.json`

### Done Criteria

- Byte-identical excerpts appear once with all obligation refs.
- Rational comparison avoids floating-point ordering.
- Tie-break order matches the Design contract.
- Uncovered, ambiguous, and over-budget requests block.
- Unrelated source drift leaves selected output unchanged.

### Acceptance Evidence And Validation

Execute DCC-FIX-002, DCC-FIX-004, DCC-FIX-005, DCC-FIX-007, and
DCC-FIX-008; validate exact selection and diagnostic receipts.

### Execution Owner And Expected Result

- Lifecycle owner: Sigil Development
- Execution owner after selection: one Task Session
- Expected result: a deterministic, coverage-preserving selection boundary

### Closeout Synchronization

- Baseline: exact ten-target inventory above
- Allowed deltas: `artifact_added`, `artifact_changed`, `evidence_added`
- Owner validation: replay all five fixtures and compare exact receipt bytes
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-003/owner-receipt.json`
- Successor: `SWU-DCC-004`; selected false

## Synchronization Rules

SWU-DCC-003 cannot begin merely because SWU-DCC-002 is eligible; it requires a
passing owner receipt and a new explicit selection. Shared compiler-file
mutation is therefore serial.

## Completion Evidence

This task closes only after both owner receipts pass.
