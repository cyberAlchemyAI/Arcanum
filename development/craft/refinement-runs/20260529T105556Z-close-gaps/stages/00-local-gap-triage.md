# Local Gap Triage

Status: preliminary refine-owned synthesis

This artifact does not replace command-backed stages. It preserves local gap state while the canonical refine execution is blocked by missing `dispatch-spec` and `runtime-handoff` command routes.

## Gap Classes

### Closed

| Gap | Evidence |
| --- | --- |
| Recursive-ledger MVP package sync completed | `development/craft/CRAFT-LEDGER-SCHEMA.yml`, `development/craft/LEDGER.md`, `development/craft/LEDGER-VALIDATION.md` |
| Blocker refinement waiver policy validated in fixture | `development/craft/LEDGER-VALIDATION.md`, task session `CRAFT-MVP-004` |

### Pre-Architecture Blocker

| Gap | Why It Blocks | Closure Route |
| --- | --- | --- |
| No Craft glossary | Method architecture will overfit or drift if terms like Craft Space, recursive ledger, blocker, gate, enabler, lane, role, residue, and promotion are not stabilized first. | Create a compact `CRAFT-GLOSSARY.md` using definitions-governance or a local glossary pass. |

### Architecture-Owned Inputs

| Gap | Architecture Responsibility |
| --- | --- |
| No Craft method architecture package yet | Primary next package after glossary stabilization. |
| No route integration contract | Should be designed as part of the architecture package because it binds Craft to refine, invoke, task-session, and validation routes. |
| No validation examples | Architecture should define the example suite shape; example fixtures can follow as implementation work. |

### Deferred Side Threads

| Gap | Deferral Reason |
| --- | --- |
| Type-to-lane-to-role mapping needs more examples before automation | Keep role hints manual until real ledger examples accumulate. |
| Refine runtime strategy is not updated canonically | Belongs to `CRAFT-REFINE-RUNTIME-STRATEGY.md` / refine runtime thread, not Craft method architecture. |
| Arcanum skill runtime interface not defined yet | Belongs to `ARCANUM-SKILL-RUNTIME-HANDOFF.md` thread. |

## Next Smallest Coherent Unit

Create the Craft glossary first, then proceed to the Craft method architecture package. The glossary is the only gap currently classified as a pre-architecture blocker.
