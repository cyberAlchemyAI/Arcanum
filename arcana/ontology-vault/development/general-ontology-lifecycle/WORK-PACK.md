# General Ontology Lifecycle Work-Pack

Status: draft
Date: 2026-05-27

## Objective

Validate and harden the general ontology lifecycle model extracted from CAOL without carrying DomainSpec/AEO-specific concerns into Ontology Vault's general layer.

## Tasks

### GOV-LIFE-001: Validate General Fixture

Status: pending

Create a branch-neutral PromotionRecord fixture that does not use CyberAlchemy, CAOL, DomainSpec, or AEO as the scenario.

Acceptance:

- uses one primary claim,
- uses generic evidence pointers,
- preserves confidence split,
- includes owner/gate,
- includes bridge validation outcome,
- avoids canonical mutation.

### GOV-LIFE-002: Reconcile With Branch Schema

Status: pending

Compare [GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md](GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md) with [../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md](../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md).

Acceptance:

- decides whether `PromotionRecord` is a standalone companion record, entry subtype, or separate template family,
- identifies missing fields,
- preserves Inventory and structured-action-schema boundaries.

### GOV-LIFE-003: Draft General Templates

Status: pending

Draft candidate templates under development first, not under `templates/`.

Candidate outputs:

- `templates-candidate/promotion-record.md`
- `templates-candidate/bridge-validation.md`
- `templates-candidate/reviewable-signal.md`

Acceptance:

- no canonical template mutation,
- examples use generic subjects,
- DomainSpec/AEO examples are deferred to the DomainSpec handoff.

### GOV-LIFE-004: Decision Packet

Status: pending

Prepare decision-gate input for:

- `meaning` branch label,
- operational branch acceptance,
- PromotionRecord record kind,
- bridge-validation outcomes,
- axiom/constitution role semantics.

## Validation

Run:

```bash
tools/validate-artifact-constitution.sh
```

Review:

```bash
rg -n "DomainSpec|AEO|CyberAlchemy|CAOL" arcana/ontology-vault/development/general-ontology-lifecycle
```

Expected result:

- references to source package are okay in package metadata,
- general model should not depend on DomainSpec/AEO as its scenario.
