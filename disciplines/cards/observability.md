# Observability Discipline

Status: implemented
Steward: Signal Observer and observability setup

## Purpose

Govern run evidence, telemetry, reflection, and maintenance signals so Arcanum usage can inform future repair without turning every run into canonical knowledge.

## Boundary

This discipline names observability practice. It does not execute the observed work, own capability-local results, or promote telemetry into framework authority without review.

## Evidence

- [Observability layer](../../README.md#observability-layer) - describes how runs become evidence for reflection and maintenance.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies observability as an implemented discipline-like practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `observability` as implemented.

## Validation

- Mode: observability
- Check: observability package behavior and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful observability discipline entry must:

- distinguish telemetry from canonical source,
- cite the observability layer,
- name when discipline changes should emit reflection signals,
- keep execution evidence attached to the run that produced it,
- route maintenance changes to the owning capability.

## Promotion Guardrail

Observability evidence can flag maintenance needs, but it cannot directly promote a sigil, spell, registry row, ontology claim, glossary term, or discipline status.
