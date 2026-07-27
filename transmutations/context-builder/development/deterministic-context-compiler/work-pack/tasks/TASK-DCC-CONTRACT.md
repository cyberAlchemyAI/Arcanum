# TASK-DCC-CONTRACT: Freeze Structural Contracts

## Task Objective

Define the minimum request and receipt schemas and prove that malformed,
duplicate-ID, and escaping-path requests fail before compilation.

## Mapping

- Layer: L0
- Slice: S-001
- Wave: W1
- Source contracts:
  [SPEC.md](../../SPEC.md),
  [ARCHITECTURE.md](../../ARCHITECTURE.md),
  [WITNESS-CONTRACTS.md](../../WITNESS-CONTRACTS.md)
- Dependencies: W0 baseline only
- Blockers: none known; `G-001` remains open until validation passes
- Selection: `none`

## SWU-DCC-001

### Objective And Primary Behavior

Introduce versioned structural contracts that accept a valid typed
single-selector request and reject invalid shape, duplicate stable IDs, and
repository escape before cache or compiler work.

### Independent Acceptance Boundary

This unit passes when the schemas and request validator accept the valid
fixture, reject every declared negative fixture with stable diagnostics, and
perform no cache or payload writes.

### Split Analysis

Candidate children were schema authoring and negative-fixture validation.
Retain them together because an unexercised schema and a validator without a
fixed contract do not establish an executable trust boundary. Compiler,
snapshot, cache, and rendering behavior remain separate SWUs.

### Dependencies

- W0 baseline receipt
- Python and repository-local JSON Schema validation dependency already used by
  Arcanum validators

### Source Anchors

- `SPEC.md`: FR-01, FR-07, Failure Contract
- `ARCHITECTURE.md`: Request Validator, R-002
- `WITNESS-CONTRACTS.md`: DCC-VAL-REQUEST, DCC-FIX-006

### Related Context

- [Shared context](../shared/CONTEXT.md)
- [Cross-task decisions](../shared/DECISIONS.md)
- Canonical target contract: `transmutations/context-builder/SKILL.md`

### Exact Write Scope

1. `transmutations/context-builder/schemas/context-request.schema.json`
2. `transmutations/context-builder/schemas/context-pack-receipt.schema.json`
3. `transmutations/context-builder/scripts/validate_context_request.py`
4. `transmutations/context-builder/development/fixtures/request/valid-single-selector.json`
5. `transmutations/context-builder/development/fixtures/request/invalid-duplicate-obligation.json`
6. `transmutations/context-builder/development/fixtures/request/invalid-path-escape.json`
7. `transmutations/context-builder/development/fixtures/source/single.md`
8. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-001/baseline.json`
9. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-001/task-session-receipt.json`
10. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-001/owner-receipt.json`

### Done Criteria

- Schemas have explicit version, required fields, stable-ID constraints, and
  evidence-separated count fields.
- Validator resolves paths against an explicit repository root and rejects
  escape before reading.
- Valid fixture passes; duplicate-ID and escape fixtures fail.
- Public fixture scan passes.

### Acceptance Evidence

- validator command and exit code for every fixture;
- diagnostic code for each negative fixture;
- schema and fixture SHA-256 values;
- scoped public-boundary scan.

### Validation Surface

```bash
python3 transmutations/context-builder/scripts/validate_context_request.py \
  transmutations/context-builder/development/fixtures/request/valid-single-selector.json
python3 transmutations/context-builder/scripts/validate_context_request.py \
  transmutations/context-builder/development/fixtures/request/invalid-duplicate-obligation.json
python3 transmutations/context-builder/scripts/validate_context_request.py \
  transmutations/context-builder/development/fixtures/request/invalid-path-escape.json
```

The first command must pass; the final two must fail with their expected
diagnostic codes.

### Execution Owner And Handoff

- Lifecycle owner: Sigil Development
- Execution owner after explicit selection: one Task Session
- First-candidate status: yes
- Selected status: no
- Expected result: a narrow, reversible structural trust boundary

## Closeout Synchronization

- Shared protocol: [CLOSEOUT-CONTRACT.md](../shared/CLOSEOUT-CONTRACT.md)
- Baseline binding: exact ten-target inventory above
- Allowed delta classes: `artifact_added`, `evidence_added`
- Owner validation: replay all three fixture commands, validate both schemas,
  and inspect the scoped diff
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-001/owner-receipt.json`
- Deterministic successor: `SWU-DCC-002`
- Successor selection: false

## Completion Evidence

Task completion requires the passing owner receipt. Source bytes alone do not
close the task.
