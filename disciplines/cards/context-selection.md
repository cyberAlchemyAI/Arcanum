# Context-Selection Discipline

Status: active-pattern
Steward: Context Builder

## Purpose

Govern how source-backed evidence is selected, bounded, and handed off so downstream work starts from relevant context without overclaiming authority.

## Boundary

This discipline names context selection practice. It does not make downstream decisions, promote evidence to canonical knowledge, or replace the receiving owner's review.

## Evidence

- [Context Builder](../../transmutations/context-builder/README.md) - defines bounded evidence selection and handoff behavior.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - classifies context selection among active-pattern disciplines.
- [Discipline Catalog](../DISCIPLINES.md) - records `context-selection` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: context pack evidence review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful context-selection discipline entry must:

- cite source-backed evidence rather than broad recall,
- name selection criteria and omissions,
- keep evidence handoffs non-authoritative,
- preserve the receiving owner's decision authority,
- define evidence-pack criteria for hidden-practice scans.

## Promotion Guardrail

Context evidence can recommend routes or candidate disciplines, but it cannot promote inventory, ontology, glossary, sigil, spell, or framework knowledge directly.
