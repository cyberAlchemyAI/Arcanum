# Discipline Governance - Test Run: Receipt Id Legend Discipline

Second live validation example for the `discipline-governance` sigil. It exercises `formalize` and `route` end to end on a real recurring practice and routes it to a constitution — the **medium** regime (formalize + route + constitution authored), one step beyond the gitignore example (low).

## Input

- Practice: every sigil/spell receipt that cites a tracked id (`BLK-`, `GAP-`, `DEC-`, `SWU-`, `R-*`, `dispatch_id`, ...) must gloss it inline so the receipt is self-contained.
- Maintenance signals met: appears across multiple capabilities (craft, task-session, refine, dispatch-spec output contracts all emit id-bearing receipts); rules were scattered/implicit; opaque-id receipts caused "what is BLK-X?" friction.

## Actions

| Mode | Output | Path |
| --- | --- | --- |
| formalize | Discipline card | [disciplines/cards/receipt-id-legend.md](../../../disciplines/cards/receipt-id-legend.md) |
| formalize | Catalog row (`receipt-id-legend`, candidate) | [disciplines/DISCIPLINES.md](../../../disciplines/DISCIPLINES.md) |
| route | Hardening route = constitution; handed off to constitution-governance | [framework/RECEIPT-ID-LEGEND-CONSTITUTION.md](../../../framework/RECEIPT-ID-LEGEND-CONSTITUTION.md) |
| validate | Catalog validator | `disciplines/scripts/validate-discipline-catalog.py` |

## Validation Result

```text
VALIDATION=pass
CATALOG=disciplines/DISCIPLINES.md
DISCIPLINE_COUNT=22
```

- All discipline card evidence links resolve locally (public arcanum only; no private cross-submodule paths).
- The constitution declares honest validation modes (`review`, no validator yet) and names its next hardening move (receipt-legend check under `tools/`).
- Boundary preserved: the discipline recommends a constitution route and does not promote any sigil, spell, registry, ontology, or glossary entry; glossing restates ids, it does not own their schemes.

## Outcome

- Result: pass.
- Route chosen: constitution (smallest sufficient enforcement for a receipt-form/structure practice across all sigils and spells).
- Next route: constitution-governance to add a receipt-legend validator, then `promote` the discipline beyond `candidate`.

## Promotion Note

This is the sigil's **second** validation example (low=gitignore, medium=receipt-id-legend). The **complex** regime (a `scan` that surfaces a hidden cross-capability practice, or a `promote`/`deprecate` with a `decision-gate`) is still unrun. See [EXPERIMENT-HARNESS-REPORT.md](EXPERIMENT-HARNESS-REPORT.md) for the full regime status before this sigil promotes beyond version 0.1.0.
