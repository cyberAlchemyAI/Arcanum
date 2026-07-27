# TASK-DCC-PAYLOAD: Output Parity And One-Payload Handoff

## Task Objective

Render stable human and machine evidence while proving that a runtime adapter
receives exactly one admitted payload representation.

## Mapping

- Layer: L1
- Slice: S-004
- Wave: W3
- Dependencies: SWU-DCC-003
- Blocker: `G-002`
- Selection: `none`

## SWU-DCC-004

### Primary Behavior

Render Markdown, index JSON, compact runtime payload, and a pack receipt from
one selected-set projection, then validate cross-format parity and the
one-payload adapter contract.

### Independent Acceptance Boundary

All formats expose identical obligation, source, selector, blocker, and digest
semantics, and the adapter receipt names exactly one payload hash.

### Split Analysis

Format rendering and adapter proof could be separate implementation functions,
but the acceptance-critical behavior is the boundary between persisted
representations and one injected representation. Keeping them together
prevents parity from passing without transport evidence.

### Source Anchors

- `SPEC.md`: FR-08, FR-09
- `ARCHITECTURE.md`: Pack Renderer And Validator, Runtime Adapter, R-003, R-004
- `WITNESS-CONTRACTS.md`: DCC-FIX-011, DCC-FIX-012

### Related Context

- Current templates:
  `transmutations/context-builder/templates/runtime-handoff-pack.md` and
  `transmutations/context-builder/templates/runtime-handoff-index.json`
- Compiler outputs from SWU-DCC-003
- [Validation strategy](../../VALIDATION-STRATEGY.md)

### Exact Write Scope

1. `transmutations/context-builder/scripts/render_context_pack.py`
2. `transmutations/context-builder/scripts/validate_context_pack.py`
3. `transmutations/context-builder/development/fixtures/expected/parity.pack.md`
4. `transmutations/context-builder/development/fixtures/expected/parity.index.json`
5. `transmutations/context-builder/development/fixtures/expected/parity.payload.md`
6. `transmutations/context-builder/development/fixtures/expected/parity.adapter-receipt.json`
7. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-004/baseline.json`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-004/task-session-receipt.json`
9. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-004/owner-receipt.json`

### Done Criteria

- Stable format ordering and canonical JSON are documented in code.
- Validator recomputes every output digest and exact cross-format projection.
- Adapter receipt has one payload hash and rejects zero or multiple payloads.
- DCC-FIX-011 and DCC-FIX-012 pass, including negative parity mutation.

### Acceptance Evidence

- expected and actual output hashes;
- parity validator result;
- one-payload positive and multi-payload negative adapter receipts;
- public-boundary scan.

### Validation Surface

Run `validate_context_pack.py` on the expected pack receipt, then mutate one
obligation mapping in each persisted format and confirm validation blocks. Run
the adapter fixture with one and two payload refs and confirm pass/block.

### Execution Owner And Expected Result

- Lifecycle owner: Sigil Development
- Execution owner after selection: one Task Session
- Expected result: evidence persistence and runtime injection are no longer
  conflated

## Closeout Synchronization

- Shared protocol: [CLOSEOUT-CONTRACT.md](../shared/CLOSEOUT-CONTRACT.md)
- Baseline: exact nine-target inventory above
- Allowed deltas: `artifact_added`, `evidence_added`
- Owner validation: parity and adapter positive/negative replay plus scoped diff
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-004/owner-receipt.json`
- Successor: `SWU-DCC-005`; selected false

## Completion Evidence

The task closes only with a passing owner receipt.
