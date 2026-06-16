# Decision Discipline

Status: active-pattern
Steward: Decision Gate

## Purpose

Govern blocker-level alternatives, trade-offs, selected routes, and decision evidence so consequential mutations do not proceed on unstated assumptions.

## Boundary

This discipline names decision-gating practice. It does not make the decision for the owner, execute the selected route, or mutate downstream artifacts without the owning lifecycle.

## Evidence

- [Decision Gate](../../arcana/decision-gate/README.md) - defines blocker-level alternatives, trade-offs, selected route, and owner decisions.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies decision discipline as a recurring practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `decision-gating` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: decision record review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful decision discipline entry must:

- identify real blocker-level alternatives,
- record trade-offs and selected route,
- name the owner of the decision,
- keep implementation blocked until the selected route is clear,
- route unresolved scope or precedence through Decision Gate.

## Promotion Guardrail

Decision evidence can authorize a route for an owner, but it cannot directly promote registry, ontology, glossary, sigil, spell, or discipline status.
