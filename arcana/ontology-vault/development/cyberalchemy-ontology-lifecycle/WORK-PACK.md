# Ontology Vault CAOL Development Work-Pack

Status: draft
Date: 2026-05-27
Owner: Ontology Vault / Sigil Development

## Objective

Use the completed CyberAlchemy Ontology Lifecycle package to harden Ontology Vault's branch-aware ontology development.

This work-pack starts the target-local development package. It does not execute all tasks.

## Completion Criteria

The package is ready for implementation or convention-update planning when:

1. CAOL source evidence is mapped into Ontology Vault development terms.
2. The branch-aware schema candidate is validated against one CAOL PromotionRecord scenario.
3. PromotionRecord boundaries are reconciled with ontology entry boundaries.
4. Bridge-validation outcomes are tested against at least one example.
5. Operational Ontology remains candidate or receives an explicit decision route.
6. No Inventory, structured-action-schema, canonical CyberAlchemy ontology, or Ontology Vault contract mutation occurs without approval.

## Tasks

### OVC-CAOL-001: Source Pack

Status: complete

Goal:

Preserve the CAOL package as selected source evidence for Ontology Vault development.

Outputs:

- `README.md`
- `SOURCE-PACK.md`
- `index.json`

Acceptance:

- all CAOL package files are represented,
- source package authority caveat is preserved,
- residual review items are listed.

### OVC-CAOL-002: Development Brief

Status: complete

Goal:

Map CAOL concepts into the current branch-aware Ontology Vault model.

Outputs:

- `ONTOLOGY-VAULT-BRIEF.md`

Acceptance:

- CAOL Business/System/Operational/Bridge terms map to current branch candidate language,
- PromotionRecord boundary is summarized,
- first validation scenario is selected.

### OVC-CAOL-003: PromotionRecord Fixture

Status: pending

Goal:

Create one review-only PromotionRecord fixture using CAOL's first working slice scenario.

Write scope:

```text
arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle/fixtures/
```

Expected outputs:

```text
fixtures/CAOL-PROMOTION-RECORD-001.md
fixtures/CAOL-PROMOTION-RECORD-001.validation.md
```

Acceptance:

- one primary claim only,
- candidate status visible,
- source inputs are pointers,
- evidence confidence and commitment confidence are separate,
- review owner class is present,
- bridge validation outcome is present,
- signal truth guard is explicit,
- operational use is gated,
- no canonical mutation.

### OVC-CAOL-004: Schema Reconciliation

Status: pending

Goal:

Compare the fixture against `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`.

Expected output:

```text
SCHEMA-RECONCILIATION.md
```

Acceptance:

- identifies whether `PromotionRecord` should be a standalone record, ontology entry subtype, or companion template,
- names missing fields in the current schema,
- preserves Inventory and structured-action-schema boundaries.

### OVC-CAOL-005: Bridge Validation Template Candidate

Status: pending

Goal:

Draft a candidate bridge-validation template using CAOL outcomes: `aligned`, `partial`, `drift`, `insufficient`, `contradicted`.

Expected output:

```text
BRIDGE-VALIDATION-TEMPLATE-CANDIDATE.md
```

Acceptance:

- supports two-sided evidence,
- preserves expected claim and observed behavior for drift,
- distinguishes evidence confidence from commitment confidence,
- blocks one-sided alignment from promotion.

### OVC-CAOL-006: Decision Packet

Status: pending

Goal:

Prepare decision-gate input for unresolved model decisions.

Expected output:

```text
DECISION-PACKET.md
```

Decisions:

- `meaning` versus `business` versus another first-branch label,
- operational as top-level branch with context binding versus extension,
- PromotionRecord standalone versus embedded,
- default bridge-validation outcomes,
- axiom/constitution role semantics.

## Validation Commands

Artifact constitution:

```bash
tools/validate-artifact-constitution.sh
```

Manual review:

```bash
rg -n "Inventory|structured-action-schema|canonical|candidate|PromotionRecord|ReviewableSignal" arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle
```

## Next Route

Next executable route:

```text
task-session or ontology-vault validate for OVC-CAOL-003
```

Recommended prompt:

```text
Run OVC-CAOL-003. Create one review-only PromotionRecord fixture and validation result under arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle/fixtures/. Use the CAOL first working slice scenario and current branch-aware schema candidate. Do not mutate Inventory, structured-action-schema, canonical CyberAlchemy ontology, or Ontology Vault contracts.
```
