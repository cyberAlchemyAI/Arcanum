# TASK-DCC-INTEGRATE: Lifecycle-Owned Canonical Integration

## Task Objective

Use the proved behavior and experiment receipts to make the smallest justified
Context Builder contract, documentation, and template update.

## Mapping

- Layer: L3
- Slice: S-008
- Wave: W5
- Dependencies: SWU-DCC-007 with reusable-behavior evidence
- Blocker: `G-005`
- Selection: `none`

## SWU-DCC-008

### Primary Behavior

Integrate only evidenced compiler behavior into the canonical public Context
Builder contract and templates under Sigil Development ownership.

### Independent Acceptance Boundary

Canonical docs, skill contract, and runtime handoff templates agree on typed
inputs, deterministic outputs, blocker semantics, one-payload transport,
measurement labels, authority ceilings, and optional/fallback behavior.

### Split Analysis

Skill, README, and paired templates could be edited separately but form one
public contract. Retaining them prevents a partially integrated interface.
Registry release, publication, consumer-specific mirror mutation, and provider
adapters remain separate owner actions.

### Source Anchors

- `SPEC.md`: full acceptance criteria
- `ARCHITECTURE.md`: Integration And Versioning Extension and R-007
- `SIGIL-HANDOFF.md`: proposed modes, inputs, outputs, observability
- passing SWU-DCC-007 comparison and owner receipts

### Related Context

- Canonical files in exact write scope
- [Cross-task traceability](../shared/TRACEABILITY.md)
- Sigil Development lifecycle contract

### Exact Write Scope

1. `transmutations/context-builder/SKILL.md`
2. `transmutations/context-builder/README.md`
3. `transmutations/context-builder/templates/runtime-handoff-pack.md`
4. `transmutations/context-builder/templates/runtime-handoff-index.json`
5. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-008/baseline.json`
6. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-008/task-session-receipt.json`
7. `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-008/owner-receipt.json`

Any generated consumer mirror is outside this public mutation inventory. If a
repository-local admitted mirror exists, its owner must generate and compare it
through a separate projection receipt; this SWU cannot silently add that write.

### Done Criteria

- Canonical contract describes only behavior proved by fixtures and live
  evidence.
- Existing manual Context Builder path remains valid unless evidence explicitly
  supports replacement.
- Templates preserve obligation, provenance, blocker, and output-path semantics.
- Public/private hygiene and all regression fixtures pass.
- Generated-parity status is recorded as pass, not-applicable with evidence, or
  block; it is never assumed.
- Lifecycle receipt separates implementation from registry release and
  promotion.

### Acceptance Evidence And Validation

Run the full deterministic fixture suite, canonical contract checks, public
hygiene scan, link validation, and any admitted generated-parity comparison.
Review the diff against the exact evidence claims.

### Execution Owner And Expected Result

- Lifecycle and execution owner: Sigil Development, optionally delegating the
  selected bounded mutation through Task Session
- Expected result: smallest evidence-backed canonical extension
- Explicit non-result: registry release, publication, deployment, or automatic
  consumer adoption

## Closeout Synchronization

- Shared protocol: [CLOSEOUT-CONTRACT.md](../shared/CLOSEOUT-CONTRACT.md)
- Baseline: exact seven-target inventory above
- Allowed deltas:
  `artifact_changed`, `evidence_added`, `status_changed`, `route_changed`
- Owner validation: full fixture suite, public scan, contract review, scoped
  diff, and generated-parity disposition
- Expected owner receipt:
  `transmutations/context-builder/development/deterministic-context-compiler/session-evidence/SWU-DCC-008/owner-receipt.json`
- Successor: `none`

## Completion Evidence

The task closes only with a Sigil Development receipt. No later lifecycle claim
is implied.
