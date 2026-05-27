# CyberAlchemy Ontology Lifecycle Development Package

Status: started
Date: 2026-05-27
Observed authoring capability: invoke
Target lifecycle owner: Ontology Vault / Sigil Development
Source package: `development/cyberalchemy-ontology-lifecycle/`

## Purpose

Start an Ontology Vault development package that consumes the completed CyberAlchemy Ontology Lifecycle architecture package as candidate evidence.

This package exists to decide what should move into Ontology Vault development next: branch-aware schema validation, PromotionRecord schema normalization, bridge-validation templates, owner/gate rules, and operational ontology acceptance boundaries.

## Boundary

In scope:

- use all artifacts under `development/cyberalchemy-ontology-lifecycle/` as source evidence,
- preserve the CAOL package verdict as reviewed candidate evidence,
- map CAOL concepts into the current Ontology Vault branch-aware model,
- prepare Ontology Vault tasks and validation surfaces.

Out of scope:

- mutating `development/cyberalchemy-ontology-lifecycle/`,
- mutating `../cyberAlchemy/ontology/`,
- mutating Inventory,
- mutating structured-action-schema,
- promoting CAOL definitions into canonical ontology,
- changing `arcana/ontology-vault/README.md`, `SKILL.md`, or templates before validation.

## Source Package Verdict

The source package reports `final-audit-pass`.

That pass means the CAOL package is complete as a reviewed candidate architecture package. It does not mean canonical ontology promotion.

Core caveat preserved from the source package:

```text
candidate knowledge may guide review
promoted knowledge may guide operation
signals are review inputs, not truth
```

## Package Files

| File | Purpose |
| --- | --- |
| [SOURCE-PACK.md](SOURCE-PACK.md) | Manifest and selected evidence from the CAOL package. |
| [ONTOLOGY-VAULT-BRIEF.md](ONTOLOGY-VAULT-BRIEF.md) | How CAOL maps into Ontology Vault branch-aware development. |
| [WORK-PACK.md](WORK-PACK.md) | Bounded next tasks for Ontology Vault development. |
| [index.json](index.json) | Machine-readable package index. |

## Current Synthesis

CAOL's strongest reusable contribution is the `PromotionRecord` boundary object:

```text
ReviewableSignal / InventoryEvidence / LifecycleEvidenceEnvelope / UserDecision / SourceSelector
  -> PromotionRecord
  -> Candidate / Premise / PromotedEntry / Policy / Constitution / Axiom / Contradiction / Retirement
```

For current Ontology Vault branch-aware work, this should be treated as a candidate governance object that can harden:

- promotion boundaries,
- confidence separation,
- bridge validation,
- operational-use gates,
- contradiction and retirement paths,
- self-application/circular-authority checks.

## Next Route

Recommended next route:

```text
ontology-vault validate
```

Validate the current branch-aware ontology schema candidate against CAOL's PromotionRecord model and first-slice scenario before mutating canonical Ontology Vault contracts.

## Layer Split

General ontology lifecycle material has been copied to:

```text
arcana/ontology-vault/development/general-ontology-lifecycle/
```

DomainSpec/AEO-specific lifecycle material is now routed through:

```text
arcana/ontology-vault/development/handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md
```

Keep this package as source evidence for the split. Do not continue adding DomainSpec-specific implementation detail here.
