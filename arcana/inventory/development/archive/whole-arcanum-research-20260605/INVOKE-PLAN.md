---
module: inventory-whole-arcanum
version: 0.1.0
status: planned
updatedAt: 2026-05-29
docType: invoke-plan
invokeMode: plan
---

# Invoke Plan: Whole Arcanum Inventory

## Intent

Create an execution-ready plan for inventorying the whole Arcanum repository as
agent-fast evidence cards and candidate EvidenceSets.

The plan does not execute ingestion. It defines the staged route, boundaries,
validation gates, and Smallest Working Units needed for `task-session` to run
the rollout safely.

## Planning Inputs

- Inventory package state: `arcana/inventory/development/WORK-PACK.md`
- Inventory production templates: `arcana/inventory/templates/`
- Artifact governance: `framework/ARTIFACT-CONSTITUTION.md`
- Schema governance: `framework/SCHEMA-CONSTITUTION.md`
- Repository surfaces observed on 2026-05-29:
  - source-like: `arcana/`, `spells/`, `transmutations/`, `formulae/`,
    `framework/`, `registry/`, `tools/`, and native runtime package surfaces
  - candidate durable evidence: curated fixtures, readiness reports, validation
    reports, and selected task-session results named by work-packs
  - excluded by default: local runtime state, generated observability ledgers,
    benchmark logs/artifacts, temporary output folders, and unpromoted run output

## Delivery Boundary

Inventory owns fast agent retrieval and evidence packaging. It does not become
the authority for canonical definitions, ontology roles, or constitution rules.

| Boundary | Decision |
| --- | --- |
| Runtime surface | Shell plus `jq` first; no human UI in this rollout. |
| Scope strategy | Whole repository through staged source slices, not one bulk ingest. |
| EvidenceSet status | Use candidate EvidenceSets to test retrieval value; do not promote canonical status yet. |
| Source authority | Inventory records evidence and selectors; upstream skills, spells, and framework docs remain the source of truth. |
| Generated state | Exclude by default unless a work-pack explicitly promotes an artifact as durable evidence. |

## Core Decision

The whole-Arcanum inventory should start with a source manifest and exclusion
policy, then create cards for a high-value pilot slice before expanding by
capability family. This gives us measurable selector quality and retrieval value
before spending effort on broad coverage.

## Produced Plan Artifacts

- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `work-pack/tasks/TASK-WAI-001-source-manifest.md`
- `work-pack/tasks/TASK-WAI-002-inventory-self-slice.md`
- `work-pack/tasks/TASK-WAI-003-governance-lifecycle-slices.md`
- `work-pack/tasks/TASK-WAI-004-expanded-capability-waves.md`
- `work-pack/tasks/TASK-WAI-005-operational-readiness.md`
- `work-pack/waves/W0-source-boundary.md`
- `work-pack/waves/W1-proof-slice.md`
- `work-pack/waves/W2-capability-expansion.md`
- `work-pack/waves/W3-operational-readiness.md`

## Next Route

Run `task-session` on `SWU-WAI-001`.

Expected first output:

- a source manifest draft,
- an exclusion policy,
- a source-family classification table,
- validation notes proving the manifest does not treat generated or local
  runtime state as source.
