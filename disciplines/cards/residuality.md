# Residuality Discipline

Status: active-pattern
Steward: Residuality Spec

## Purpose

Govern stressor analysis, desired residue, degradation behavior, attractors, and resilience decisions so specifications remain useful under partial failure or pressure.

## Boundary

This discipline names residuality practice. It does not own every specification, decide implementation behavior alone, or replace validation for the system being specified.

## Evidence

- [Residuality Spec](../../arcana/residuality-spec/README.md) - defines stressors, residue, degradation behavior, and resilience decisions.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies residuality as a recurring discipline-like practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `residuality` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: residuality-spec review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful residuality discipline entry must:

- name stressors and desired residue,
- describe degradation behavior rather than only success behavior,
- identify resilience decisions and attractors,
- cite Residuality Spec evidence,
- keep implementation and validation owned by the target system lifecycle.

## Promotion Guardrail

Residuality evidence can harden a specification route, but it cannot directly promote implementation, registry, ontology, glossary, sigil, spell, or discipline authority.
