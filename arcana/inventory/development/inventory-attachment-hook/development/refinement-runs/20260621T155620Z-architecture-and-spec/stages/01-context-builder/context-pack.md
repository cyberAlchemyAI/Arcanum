---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
stage: s1-context-builder
status: pass
updatedAt: 2026-06-21
docType: context-pack
---

# Context Pack: Inventory Attachment Hook Architecture And Spec

## Task

Create architecture and specification artifacts for the Inventory Attachment Hook
without mutating canonical skill docs or generated mirrors.

## Obligation Matrix

| Obligation | Coverage | Evidence |
| --- | --- | --- |
| Define opt-in attachment, not global execution. | covered | `INVOKE-PLAN.md:25`, `IMPLEMENTATION-LAYERING.md:28`, `WORK-PACK.md:104` |
| Keep Inventory output candidate/read-model only. | covered | `INVOKE-PLAN.md:28-30`, `INVOKE-PLAN.md:80-97`, `inventory/SKILL.md:223-227` |
| Split owners across Inventory, Sigil Development, Spellcraft, Observability, Observed Invocation Loop, and generator. | covered | `INVOKE-PLAN.md:69-75`, `WORK-PACK.md:71-77` |
| Define policy and handoff envelopes. | covered | `INVOKE-PLAN.md:44-64`, `REFINE-SEED-PROPOSAL.md:107-111` |
| Define idempotency, failure, privacy, public-boundary, and validation rules. | covered | `WORK-PACK.md:83-86`, `REFINE-SEED-PROPOSAL.md:53-58`, `observed-invocation-loop/README.md:65-70` |
| Preserve generated mirror discipline. | covered | `WORK-PACK.md:76`, `observed-invocation-loop/README.md:115` |
| Keep state namespaces separate. | covered | `REPOSITORY-PACKAGE.md:12-19`, `SIGIL-OBSERVABILITY-HOOK.md:70-93`, `dispatch-spec/TECHNIQUE-CATALOG.md:116-117` |

## Selected Evidence

| Source | Selector | Why Included |
| --- | --- | --- |
| `arcanum/arcana/inventory/development/inventory-attachment-hook/INVOKE-PLAN.md` | lines 25-30, 44-75, 80-110 | Defines the hook intent, policy sketch, ownership split, and no-promotion boundary. |
| `arcanum/arcana/inventory/development/inventory-attachment-hook/WORK-PACK.md` | lines 25-32, 44-77, 83-86, 104-106 | Defines implementation slices, SWUs, and open decisions for failure, mode, idempotency, and pilot. |
| `arcanum/arcana/inventory/SKILL.md` | lines 82-105, 150-175, 223-227 | Defines Inventory ingest, evidence-card/EvidenceSet, and authority rules. |
| `arcanum/arcana/inventory/README.md` | lines 15-35, 91-107 | Defines evidence-card and EvidenceSet behavior and non-authority handoffs. |
| `arcanum/arcana/sigil-development/SKILL.md` | lines 146-153, 207-216 | Defines where sigil observability/post-run hook guidance belongs. |
| `arcanum/arcana/spellcraft/SKILL.md` | lines 119-136, 181-193 | Defines where reusable spell observability and handoff guidance belongs. |
| `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md` | lines 27-70, 85-93, 166-191 | Defines invocation envelope, telemetry ledger, hook operations, implementation options, and failure behavior. |
| `arcanum/spells/observed-invocation-loop/README.md` | lines 14-18, 45-70, 85-115 | Defines hook-first observed runtime flow and generated package attachment discipline. |
| `arcanum/formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | lines 84, 100-117 | Defines authority split, receipt handoff, state namespace, and memory/promotion split techniques. |

## Constraints

- Canonical sources are designed first; generated runtime packages are refreshed
  later from canonical source.
- Inventory Attachment may only create candidate evidence, indexes, and lookup
  projections.
- Runtime automation must be downstream of contract and template definition.
- Hook failure defaults to warning unless a capability declares attachment as a
  required output.
- No private material may be inventorized into public Arcanum surfaces.

## Gaps

No external research gap was found. The local repository already has enough
authority material for architecture/spec authoring.

## Context Builder Result

- Mode: standard
- Handoff pack: runtime
- Strict coverage: pass
- Verdict: pass
