# Session Handoff: DomainSpec Ontology Lifecycle Particulars

## Identity

- Source session reference: current ontology development thread, 2026-05-27
- Destination label: DomainSpec ontology lifecycle migration
- Handoff type: new-lifecycle-thread
- Target project or lifecycle: DomainSpec / Agent Execution Orchestrator ontology lifecycle evidence
- Created for: moving DomainSpec/AEO-specific material out of general Ontology Vault development

## New Session Prompt

```text
Use the DomainSpec/AEO-specific material currently referenced by Arcanum Ontology Vault development to start a DomainSpec-owned ontology lifecycle package. Move only the particular software lifecycle and AEO route/evidence-envelope concerns into the DomainSpec layer. Keep the general ontology lifecycle concepts in Arcanum Ontology Vault. Do not mutate Arcanum Ontology Vault contracts, Inventory, or structured-action-schema. Produce a DomainSpec-local development package with source map, lifecycle evidence model, fixture plan, and open decisions.
```

## Route Rationale

- Recommended next route: `invoke define` or `invoke design`
- Rationale: the migration needs a DomainSpec-owned lifecycle baseline, not immediate implementation.
- Lifecycle owner: external-project / DomainSpec

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| Separate general from particular | covered | `arcana/ontology-vault/development/general-ontology-lifecycle/CONTEXT-PACK.md#Particular Material For DomainSpec Handoff` | Names what should leave the general Ontology Vault layer. |
| Preserve reusable general model | covered | `arcana/ontology-vault/development/general-ontology-lifecycle/GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md#Deferred Particulars` | Prevents re-importing DomainSpec-specific details into the general model. |
| Preserve CAOL source context | covered | `development/cyberalchemy-ontology-lifecycle/CONTEXT-HANDOFF.md#DomainSpec And AEO Sources` | Identifies original DomainSpec/AEO evidence sources. |
| Preserve AEO/lifecycle evidence concept | covered | `development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md#Low-Level Component View` | Defines `LifecycleEvidenceEnvelope` and DomainSpec/AEO role as candidate evidence input. |
| Preserve promotion gates | covered | `development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md#Bridge Validation` | DomainSpec-specific package should still respect bridge outcomes and confidence split. |

Strict coverage: pass

## Selected Session Context

- The current thread identified a concern mix: CAOL was useful as candidate evidence, but DomainSpec/AEO route-stage details should not become the general Ontology Vault layer.
- General material was copied to:
  - `arcana/ontology-vault/development/general-ontology-lifecycle/`
- DomainSpec-specific material to move:
  - DomainSpec/AEO route-stage execution semantics,
  - AEO telemetry envelope implementation details,
  - DomainSpec authority map and constitution-specific governance,
  - `LifecycleEvidenceEnvelope` details tied to AEO route/stage/terminal outcomes,
  - software-development-specific fixture scenarios.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Full CAOL package transcript | Too broad; use selected source files and selectors. |
| General PromotionRecord model | Already copied to Ontology Vault general package; DomainSpec should consume, not redefine. |
| Ontology Vault template mutation | Out of scope for DomainSpec migration. |
| Inventory evidence-card implementation | Separate Inventory lifecycle. |

## Target Boundary

In scope for the new thread:

- DomainSpec-local development package,
- DomainSpec/AEO source map,
- lifecycle evidence envelope model,
- AEO route/stage/evidence fixture plan,
- bridge validation from DomainSpec intent to system/runtime evidence,
- open decisions about how DomainSpec consumes general PromotionRecord semantics.

Out of scope for the new thread:

- general Ontology Vault schema ownership,
- Arcanum Inventory mutation,
- structured-action-schema mutation,
- canonical DomainSpec mutation without explicit acceptance,
- CyberAlchemy-specific ontology promotion.

Prior decisions to preserve:

- general ontology lifecycle concepts remain in Ontology Vault development,
- DomainSpec/AEO particulars move to DomainSpec-owned development,
- signals are review inputs, not truth,
- evidence confidence and commitment confidence remain separate,
- bridge validation blocks false alignment.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| DomainSpec target path not selected | DomainSpec thread | open | Choose target folder before writing. |
| DomainSpec acceptance route unknown | DomainSpec/user | open | Decide define vs design start. |
| AEO fixture scope not selected | DomainSpec thread | open | Pick one route/stage/evidence-envelope scenario. |

## Next-Session Start Prompt

```text
Start a DomainSpec-owned ontology lifecycle migration from the Arcanum Ontology Vault split.

Use these source artifacts:
- arcana/ontology-vault/development/handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md
- arcana/ontology-vault/development/general-ontology-lifecycle/CONTEXT-PACK.md
- arcana/ontology-vault/development/general-ontology-lifecycle/GENERAL-ONTOLOGY-LIFECYCLE-MODEL.md
- development/cyberalchemy-ontology-lifecycle/CONTEXT-HANDOFF.md
- development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md
- development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md

Create a DomainSpec-local development package for the particular software lifecycle/AEO evidence-envelope material. Keep general ontology lifecycle concepts in Arcanum Ontology Vault. Do not mutate Arcanum Ontology Vault contracts, Inventory, structured-action-schema, or canonical DomainSpec files without explicit approval.
```

## Provenance

- Source refs:
  - `development/cyberalchemy-ontology-lifecycle/`
  - `arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle/`
  - `arcana/ontology-vault/development/general-ontology-lifecycle/`
- Context Builder mode: standard
- Evidence date: 2026-05-27
- Output path: `arcana/ontology-vault/development/handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md`

## Gate Result

- Status: pass
- Reason: Context selected enough material to start a DomainSpec-owned lifecycle thread while preserving the general/specific layer boundary.
