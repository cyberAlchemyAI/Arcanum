# Ontology Discipline

Status: active-pattern
Steward: Ontology Vault

## Purpose

Govern branch-aware meaning, premises, confidence, convention changes, and ontology boundaries so meaning work stays separate from evidence capture and local implementation.

## Boundary

This discipline names ontology governance as a practice. It does not promote ontology claims, define terms, or treat discipline evidence as ontology authority without Ontology Vault review.

## Evidence

- [Ontology Vault](../../arcana/ontology-vault/README.md) - defines meaning, premise, branch, confidence, and convention governance.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies ontology discipline as a recurring practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `ontology` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: ontology-owner review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful ontology discipline entry must:

- preserve branch-aware meaning boundaries,
- cite the ontology owner,
- distinguish source evidence from ontology authority,
- name confidence and convention implications when relevant,
- route ontology mutation to Ontology Vault.

## Promotion Guardrail

Discipline evidence can recommend ontology review, but it cannot directly promote, contradict, merge, or retire ontology claims.
