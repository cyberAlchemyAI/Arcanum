# Stage 5 — Distill (coherent unit selection)

- **Capability:** distill · **Mode:** standard · **Status:** pass

## Selected coherent unit
**A thin `ux-lessons` sigil that owns exactly two typed artifacts (`lesson`, `ux-pattern`) and two consumer adapters, and composes five existing owners for everything else.**

This is the smallest unit that still recomposes into the full `session → lesson → ux-pattern → consumers` system.

## Composition map (build-from-owned)
| Concern | Owner (composed, not rebuilt) |
| ------- | ----------------------------- |
| session signal capture | signal-observer / observed-invocation-loop |
| session → analysis shape | workflow-reflect (borrowed shape) |
| lesson → pattern reduction | distill |
| reusable pattern store mechanics | architecture-pattern-inventory (card shape + store) |
| residue ledger | residuality-spec |
| **lesson + ux-pattern schemas (NEW)** | **ux-lessons** |
| **validator adapter + studio adapter (NEW)** | **ux-lessons** |

## Rejected alternatives
- **Net-new sigil owning the whole pipeline** — rejected: duplicates 5 owners (Role A). Violates build-from-owned.
- **Schema-less spell** — rejected: cannot own the `lesson`/`ux-pattern` typed contract the two consumers require (Role B). A spell composes but owns no schema.
- **Fold into workflow-reflect** — rejected: workflow-reflect emits workflow *proposals*, not reusable UX *patterns* with consumer intakes; different output type and consumers.

## Carried constraints (from Stage 3 flags)
- Borrow, never fork, the architecture-pattern-inventory store (F1).
- Schema enforces anecdote→no-hard-gate honesty (F2).
- MVP = validator adapter + studio annotation adapter; studio variant/fitness intake deferred behind OQ-5 (F3).
