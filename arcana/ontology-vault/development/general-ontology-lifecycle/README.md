# General Ontology Lifecycle Development Package

Status: started
Date: 2026-05-27
Created with: context-builder selection + invoke handoff split
Source package: `development/cyberalchemy-ontology-lifecycle/`

## Purpose

Hold the general ontology-governance material extracted from the CyberAlchemy Ontology Lifecycle package.

This package is intentionally branch-neutral and system-neutral. It keeps reusable Ontology Vault ideas here, while DomainSpec/AEO-specific software lifecycle details can move to DomainSpec-owned development.

## General Material Copied Here

- PromotionRecord as a bounded governance/change record.
- ReviewableSignal as review input, not truth.
- Evidence confidence versus commitment confidence.
- Candidate versus promoted knowledge.
- Bridge validation outcomes.
- Operational ontology as candidate/context-bound until accepted.
- Owner/gate and contradiction/retirement requirements.
- Axiom and constitution semantics as candidate governance roles, not settled definitions.

## Not Owned Here

- DomainSpec/AEO route-stage implementation details.
- DomainSpec canonical authority maps or constitution.
- CyberAlchemy-specific ontology package claims.
- Runtime adapter implementation.
- Inventory evidence-card implementation.
- structured-action-schema fields.

## Files

| File | Purpose |
| --- | --- |
| [CONTEXT-PACK.md](CONTEXT-PACK.md) | Context Builder selection of general evidence from CAOL. |
| [GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md](GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md) | Reusable model copied from CAOL into Ontology Vault terms. |
| [WORK-PACK.md](WORK-PACK.md) | General follow-up tasks for Ontology Vault validation and schema hardening. |
| [index.json](index.json) | Machine-readable package index. |

## Layer Boundary

This package may inform future Ontology Vault templates or schemas, but it is not canonical. Template or contract changes still require validation and an explicit convention-update route.

## Next Route

Use this package as the source for Ontology Vault validation of:

```text
PromotionRecord
ReviewableSignal
bridge validation outcomes
candidate/promoted boundaries
```

Use [../handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md](../handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md) for the DomainSpec-specific migration thread.
