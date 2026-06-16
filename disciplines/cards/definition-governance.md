# Definition Governance Discipline

Status: active-pattern
Steward: Definitions Governance

## Purpose

Govern critical term ownership, drift checks, and definition synchronization so Arcanum uses important terms consistently across capabilities.

## Boundary

This discipline names definition governance as a practice. It does not author or promote canonical definitions from the discipline layer; canonical term work routes to Definitions Governance.

## Evidence

- [Definitions Governance](../../arcana/definitions-governance/README.md) - defines owners, canonical definition maintenance, and drift checks.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies definition discipline as a recurring practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `definition-governance` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: definitions-governance drift review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful definition governance discipline entry must:

- identify which terms need owner-governed definitions,
- distinguish canonical definitions from local explanations,
- cite the definitions-governance owner,
- route term changes through the definition lifecycle,
- avoid using discipline cards as glossary authority.

## Promotion Guardrail

Discipline evidence can recommend a definitions-governance route, but it cannot directly define, rename, promote, or deprecate canonical terms.
