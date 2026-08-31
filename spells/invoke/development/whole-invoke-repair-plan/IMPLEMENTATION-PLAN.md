# Whole Invoke Repair — Implementation Plan

## Objective

Repair all findings in `INVOKE-AUDIT-2026-08-27` without weakening lifecycle gates. The implementation must replace asserted readiness with exact producer-owned evidence and prove the final generic workflow through real consumers.

## Source Anchors

| Source | SHA-256 |
| --- | --- |
| `arcanum/spells/invoke/development/audits/2026-08-27-whole-invoke/INVOKE-AUDIT.json` | `dc3e64f881bce6d715ccb1a7bf9985457dc6fc829e3b54a1796507c40171a06f` |
| `arcanum/spells/invoke/development/audits/2026-08-27-whole-invoke/INVOKE-AUDIT.md` | `e70d8fba6c14626449d388e420b17b4cf34145ed311f8fe8f93d48e86ba46679` |
| `.agents/skills/invoke/plan.md` | `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c` |
| `.agents/skills/implementation-layering/SKILL.md` | `a42704c3f526a40193a65849fc50c36d14b224c6da71202c02f20401e1e0ec60` |
| `.agents/skills/orchestrate/SKILL.md` | `6c064b6f5e3a717e48ce7d141d383f35ad25414fe035b8a246ad1b07b3fbf0df` |

## Delivery Slices

1. **Admission trust:** SWU-WIR-001–002 close INV-AUDIT-001, 002, and 007.
2. **Plan-to-owner chain:** SWU-WIR-003–005 close INV-AUDIT-003, 005, and 006.
3. **Mode truth and genericity:** SWU-WIR-006–009, 011–012 close INV-AUDIT-004, 008, 009, and 011.
4. **Compatibility and final proof:** SWU-WIR-010 and 013 close INV-AUDIT-010 and revalidate the whole denominator.

## Implementation Rules

- Each SWU consumes immutable predecessor receipts and writes only its declared scope.
- Producers stage all outputs in a sibling temporary directory, run validation there, and publish the complete family atomically only after PASS.
- Invalid sources and blocked downstream consumers publish no outputs.
- All machine views are schema-first. Human views are deterministic projections and cannot add semantics.
- Runtime-derived and independently reviewed evidence remains separately owned; the Plan source cannot pre-author it.
- Generated mirrors change only through the canonical selective Invoke synchronization command.
- Compatibility tests precede deletion or status removal.

## Compatibility and Rollback

- Prefer additive versioned schemas and readers before changing writer defaults.
- Preserve historical request/response and mode evidence as read-only compatibility fixtures.
- Every canonical change is independently revertible at its SWU boundary; generated mirrors are reverted by canonical resynchronization.
- `full` removal uses a compatibility adapter or explicit unsupported diagnostic for historical inputs; it never silently reroutes them.

## Current Block

The installed Plan producer cannot emit this complete split package, execution-entry projection, WPRA v2 configuration, and readiness receipt from one truthful machine source. Therefore this manually authored planning package is reviewable planning evidence only and is not an execution candidate.
