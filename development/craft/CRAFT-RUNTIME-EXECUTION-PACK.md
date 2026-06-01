# Craft Runtime Command Surface Execution Pack

## Purpose

Coordinate execution for `CRAFT-RUNTIME-WORK-PACK.md`.

## Wave Plan

| Wave | Layer | Goal | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-packs/craft-runtime/waves/W0.md) | L0 | Expose `dispatch-spec`. | CRAFT-RUNTIME-001 | Work-pack exists. | `tools/arcanum --resolve dispatch-spec` passes. |
| [W1](work-packs/craft-runtime/waves/W1.md) | L1 | Expose `runtime-handoff`. | CRAFT-RUNTIME-002 | W0 passed. | `tools/arcanum --resolve runtime-handoff` passes. |
| [W2](work-packs/craft-runtime/waves/W2.md) | L2 | Run command smoke. | CRAFT-RUNTIME-003 | W1 passed. | Both resolves pass and dispatch validation passes. |
| [W3](work-packs/craft-runtime/waves/W3.md) | L3 | Sync Craft state. | CRAFT-RUNTIME-004 | W2 passed. | README/session ledger agree on next Refine validation route. |

## Parallelization

Not recommended. Each task depends on the previous route proof.
