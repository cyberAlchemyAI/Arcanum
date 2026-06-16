# Dispatch Discipline

Status: active-pattern
Steward: Dispatch Spec

## Purpose

Govern route-shaped work where Arcanum chains, fans out, validates, or hands off multiple capability steps with explicit gates, observability, and boundary evidence.

## Boundary

This discipline names dispatch route practice. It does not execute route steps, prove content completion, or promote the capabilities named in a dispatch document.

## Evidence

- [Dispatch Spec](../../formulae/dispatch-spec/README.md) - defines schema-backed route validation, gates, and boundary evidence.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies dispatch as a recurring discipline-like practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `dispatch` as an active-pattern discipline.

## Validation

- Mode: validator
- Check: `python3 formulae/dispatch-spec/scripts/validate-dispatch.py <dispatch.json>` for route artifacts, plus `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful dispatch discipline entry must:

- separate route-shape validation from execution evidence,
- cite the dispatch-spec validator and route contract,
- require gates, handoffs, and boundary evidence for multi-step work,
- preserve owner authority for each step,
- name the next hardening route for multi-phase formalization.

## Promotion Guardrail

Dispatch evidence can validate a proposed route, but it cannot directly execute, approve, or promote any sigil, spell, registry, ontology, glossary, or discipline.
