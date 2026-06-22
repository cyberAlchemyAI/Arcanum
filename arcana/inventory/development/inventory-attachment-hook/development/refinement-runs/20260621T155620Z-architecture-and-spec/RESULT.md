---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
status: pass
updatedAt: 2026-06-21
docType: refine-result
---

# Refine Result: Inventory Attachment Hook Architecture And Spec

## Result

| Field | Value |
| --- | --- |
| Target | `arcanum/arcana/inventory/development/inventory-attachment-hook/` |
| Status | pass |
| Preset | standard |
| Research | research-if-gap-appears, no external research needed |
| Dispatch route | `REFINE-DISPATCH.json` |
| Runtime handoff | `RUNTIME-HANDOFF.md` |
| Run manifest | `RUN-MANIFEST.md` |
| Evidence index | `evidence-index.json` |

## Outputs

- `arcanum/arcana/inventory/development/inventory-attachment-hook/ARCHITECTURE.md`
- `arcanum/arcana/inventory/development/inventory-attachment-hook/SPEC.md`

## Stage Evidence

| Stage | Verdict |
| --- | --- |
| Context Builder evidence baseline | pass |
| Invoke Define | pass |
| Interrogation refine-review | pass |
| Research decision | pass |
| Distill coherent unit | pass |
| Invoke Design architecture/spec | pass |
| Interrogation design review | flag-repaired |
| Distill Repair | pass |
| Invoke Plan refresh | pass |
| Final Interrogation and Synthesis | pass |

## Final Synthesis

The hook should be implemented as `AttachedInventoryHandoff`: an explicit,
opt-in post-run handoff from an observed sigil/spell invocation to Inventory
candidate evidence.

The refined architecture/spec now fixes the main risks found by review:

- idempotency is per selected output;
- disabled/absent policy is a skip, not an invalid handoff;
- attachment operations cannot recursively attach themselves;
- public-boundary inheritance must resolve before public writes;
- selected outputs become evidence-cards first, and EvidenceSets only group card
  IDs;
- validation requires schema/fixture checks beyond grep anchors;
- generated Observed Invocation Loop mirrors are in scope whenever OIL canonical
  docs change.

## Residue

This packet is pre-implementation guidance. It is not canonical authority until
the listed canonical sources are patched and generated mirrors are refreshed.

## Recommended Next Route

Run `task-session` on `SWU-IAH-001`.
