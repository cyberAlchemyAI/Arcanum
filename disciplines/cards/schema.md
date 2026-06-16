# Schema Discipline

Status: canonical
Steward: Constitution Governance

## Purpose

Govern schema form, validator backing, and schema migration so machine-checkable contracts stay consistent across Arcanum artifacts.

## Boundary

This discipline names schema governance. It does not own the domain semantics inside individual schemas, nor does it mutate capability-local contracts without the owning lifecycle route.

## Evidence

- [Schema Constitution](../../framework/SCHEMA-CONSTITUTION.md) - defines the canonical schema rules and validator-backed practice.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - classifies schema as a canonical discipline.
- [Discipline Catalog](../DISCIPLINES.md) - records `schema` as canonical with legacy schema migration as a hardening move.

## Validation

- Mode: validator
- Check: schema-specific validators and `python3 disciplines/scripts/validate-discipline-catalog.py` for the catalog row.
- Latest result: pass

## Quality Bar

A useful schema discipline entry must:

- cite the canonical schema constitution,
- distinguish schema form from capability-local semantics,
- require validator-backed claims when status is canonical,
- keep migrations scoped and reviewable,
- name the owner for any schema contract mutation.

## Promotion Guardrail

Schema discipline evidence can route schema work to Constitution Governance, but it cannot directly alter a sigil, spell, registry, ontology, glossary, or generated runtime contract.
