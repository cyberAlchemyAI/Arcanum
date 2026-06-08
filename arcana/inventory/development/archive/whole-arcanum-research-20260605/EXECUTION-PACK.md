---
module: inventory-whole-arcanum
version: 0.1.0
status: planned
updatedAt: 2026-05-29
docType: execution-pack
---

# Execution Pack: Whole Arcanum Inventory

## Execution Strategy

Execute one SWU at a time until L0 passes. After L0, parallelization is allowed
only when write scopes are disjoint and the source manifest is already stable.

## Waves

| Wave | Layer | Goal | Tasks | Parallelization |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0-source-boundary.md) | L0 | Establish source boundary and manifest. | TASK-WAI-001 | none |
| [W1](work-pack/waves/W1-proof-slice.md) | L1 | Prove value on Inventory plus governance/lifecycle sources. | TASK-WAI-002, TASK-WAI-003 | after manifest, task-local parallelism only |
| [W2](work-pack/waves/W2-capability-expansion.md) | L2 | Expand by source family. | TASK-WAI-004 | family slices may parallelize after W1 |
| [W3](work-pack/waves/W3-operational-readiness.md) | L3 | Harden validation, refresh, and readiness. | TASK-WAI-005 | closure wave, sequential |

## First Task-Session Handoff

Start with `SWU-WAI-001` from `TASK-WAI-001`.

Task-session should stop at the first blocker if:

- source classification cannot distinguish source from generated state,
- a path needs durable-evidence promotion but no nearby artifact explains why,
- schema files violate `.schema.yml` governance,
- the planned manifest would require broad ingestion before source boundaries are
  reviewed.

## Validation Spine

Run after each wave:

```bash
tools/validate-artifact-constitution.sh --self-test
tools/validate-artifact-constitution.sh
bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card
```

Additional wave-local checks are documented in each task contract.
