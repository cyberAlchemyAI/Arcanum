# Discipline Governance

Discipline Governance is an Arcana sigil for formalizing, routing, validating, promoting, and retiring Arcanum disciplines.

It exists because the [disciplines layer](../../disciplines/README.md) — its catalog, card template, schema, and catalog validator — had no owning lifecycle. Disciplines were added by hand, which makes it easy to catalog a one-off task as a durable practice, to skip the evidence, or to let a discipline quietly claim authority it should not have.

## Problem It Solves

Arcanum repeatedly relies on cross-capability practices: planning, schema form, observability, runtime boundaries, decision gating, and more. These practices are broader than any single sigil or spell, but they are not knowledge entries either.

Without an owner, disciplines drift in three ways:

- a practice gets formalized with no evidence that it actually recurs,
- a discipline claims promotion authority over a sigil, spell, registry, ontology, or glossary it does not own,
- the catalog and cards fall out of sync with the schema and validator.

Discipline Governance keeps a discipline small enough to be evidence-backed, explicit enough to validate, and bounded so it routes enforcement to the right owner instead of absorbing it.

## Core Stance

A discipline names a way of working; it does not execute it.

```text
recurring practice
  -> gather cross-capability evidence
  -> formalize a discipline card + catalog row
  -> choose the smallest sufficient hardening route
  -> hand off enforcement to the owning lifecycle
  -> validate the catalog and card
  -> promote, hold, or retire with named evidence
```

## Use When

- a practice recurs across multiple capabilities and has no formal home,
- scattered rules for one practice are causing drift, rework, or confusion,
- a discipline card or catalog entry must be created or kept schema-valid,
- a discipline needs a hardening decision (constitution, validator, template, spell, or sigil),
- a discipline's status should advance or retire with evidence,
- the catalog must be validated after edits.

## Do Not Use When

- the practice is a one-off task rather than a durable method,
- a capability-local note is enough,
- the request is to mutate a sigil, spell, registry, ontology, or glossary contract,
- the request is to author the constitution itself rather than name it as a route,
- the request is to define a canonical term.

## Core Concepts

- Discipline: a durable cross-capability operating practice with a purpose, boundary, evidence, steward, and status.
- Card: the per-discipline artifact under `disciplines/cards/` that captures the practice.
- Catalog: the `disciplines/DISCIPLINES.md` table that indexes every discipline.
- Hardening route: the smallest sufficient way to give a practice force — catalog-only, template, validator, constitution, spell, or sigil.
- Status ladder: candidate, active-pattern, implemented, canonical, deprecated.
- Growth Rule: promote only when the next route names owner, evidence, validation surface, and mutation boundary.

## Outputs

The sigil can produce:

- a discipline card,
- a catalog row,
- a scan of candidate or hidden disciplines,
- a routing decision with a named owner,
- a catalog and schema validation result,
- a promotion or deprecation record.

## Integration

Use [constitution-governance](../constitution-governance/) when a discipline's hardening route is a constitution.

Use [definitions-governance](../definitions-governance/) when a discipline depends on a canonical term.

Use [context-builder](../../transmutations/context-builder/) and [inventory](../inventory/) to gather source-backed evidence that a practice recurs.

Use [decision-gate](../decision-gate/) when promotion, precedence, or scope needs a human choice.

Use [sigil-development](../sigil-development/) when Discipline Governance itself is revised or promoted.

Run the catalog validator after edits:

```bash
python3 disciplines/scripts/validate-discipline-catalog.py
```

## Why This Is Arcana

Discipline Governance coordinates long-lived method authority across evidence, routing, validation, and promotion. It is not a formatter or a single capability; it governs how recurring practices become disciplines and how they hand enforcement to the right owner.
</content>
