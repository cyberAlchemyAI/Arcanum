# UX Evidence Discipline

Status: candidate
Steward: UX Evidence Validator

## Purpose

Govern user-interface evidence through browser checks, accessibility criteria, market or research references, and validator-safe fixtures for durable UX work.

## Boundary

This discipline names UX evidence practice. It does not own product design decisions, replace user research, or mutate interface implementations outside their owning lifecycle.

## Evidence

- [UX Evidence Validator](../../arcana/ux-evidence-validator/README.md) - defines browser evidence, accessibility checks, fixture plans, and evidence reports.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - classifies UX evidence as a candidate discipline.
- [Discipline Catalog](../DISCIPLINES.md) - records `ux-evidence` as a candidate discipline.

## Validation

- Mode: mixed
- Check: browser/accessibility evidence review, UX validator fixtures where applicable, and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful UX evidence discipline entry must:

- cite browser or accessibility evidence for durable UI claims,
- separate evidence from product design authority,
- name the fixture or report surface when available,
- preserve owner review for product-facing decisions,
- avoid using generic taste as validation.

## Promotion Guardrail

UX evidence can support product or validator decisions, but it cannot directly promote interface changes, registry entries, ontology, glossary, sigils, spells, or discipline status.
