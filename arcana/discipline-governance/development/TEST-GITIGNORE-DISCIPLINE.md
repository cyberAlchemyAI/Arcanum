# Discipline Governance - Test Run: Gitignore Discipline

This is the first live validation example for the `discipline-governance` sigil. It exercises the `formalize` and `route` modes end to end by formalizing a real recurring practice and routing it to a constitution.

## Input

- Practice: deciding what belongs in `.gitignore` versus the tracked tree across Arcanum and consuming repositories.
- Maintenance signals met: appears across multiple capabilities (runtime boundary, observability, generated install surfaces); already had scattered rules; had caused tracked-vs-ignored confusion.

## Actions

| Mode | Output | Path |
| --- | --- | --- |
| formalize | Discipline card | [disciplines/cards/gitignore.md](../../../disciplines/cards/gitignore.md) |
| formalize | Catalog row (`gitignore`, candidate) | [disciplines/DISCIPLINES.md](../../../disciplines/DISCIPLINES.md) |
| route | Hardening route = constitution; handed off to constitution-governance | [framework/GITIGNORE-CONSTITUTION.md](../../../framework/GITIGNORE-CONSTITUTION.md) |
| validate | Catalog validator | `disciplines/scripts/validate-discipline-catalog.py` |

## Validation Result

```text
VALIDATION=pass
CATALOG=disciplines/DISCIPLINES.md
DISCIPLINE_COUNT=21
```

- All discipline card evidence links resolve locally.
- The constitution declares honest validation modes (`review`, no validator yet) and names its next hardening move.
- Boundary preserved: the discipline recommends a constitution route and does not promote any sigil, spell, registry, ontology, or glossary entry.

## Outcome

- Result: pass.
- Route chosen: constitution (smallest sufficient enforcement for a structure/form practice).
- Next route: constitution-governance to add an ignore-policy validator, then `promote` the discipline beyond `candidate`.

## Promotion Note

This single example is the sigil's first validation evidence, not full promotion proof. A complete `experiment-harness` loop (low, medium, and complex discipline cases plus a validation report) is the named follow-up before this sigil is promoted beyond version 0.1.0.
</content>
