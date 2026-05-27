# Refine Result

## Verdict

`pass`

## Summary

The selected `Candidate Role Semantics` section was too small: it named only `axiom`, `constitution`, `policy`, and `premise`, so it skipped earlier and negative roles such as `hypothesis`, `observation`, `evidence`, `candidate`, `contradiction`, and `retirement`.

The refinement expands the section into a candidate role catalog while preserving the non-canonical boundary.

## Selected Unit

Candidate role catalog for ontology lifecycle claims.

## Decision

Use roles as claim semantics, not as canonical lifecycle statuses. A role can inform status and promotion gates, but it should not silently promote a claim.

## Validation

- Added `hypothesis`.
- Added early evidence roles, governance roles, and negative/closeout roles.
- Preserved candidate-only language.
- Did not mutate templates, Inventory, structured-action-schema, or canonical Ontology Vault contracts.
