# Quality-Bar Discipline

Status: canonical
Steward: Framework

## Purpose

Govern observable completion criteria so Arcanum work is judged by evidence, validation, and named residual risk rather than plausible narration.

## Boundary

This discipline names the cross-capability quality practice. It does not define every capability's local done criteria or substitute for running the validation owned by that capability.

## Evidence

- [Quality Bar](../../framework/QUALITY-BAR.md) - defines observable success and failure criteria for Arcanum execution.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies quality discipline as canonical framework practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `quality-bar` as canonical.

## Validation

- Mode: mixed
- Check: quality-bar review against observable evidence + `python3 disciplines/scripts/validate-discipline-catalog.py`. Canonical status rests on the [Quality Bar constitution](../../framework/QUALITY-BAR.md), not a deterministic card-validator (curation 2026-06-21).
- Latest result: pass
- Next hardening: add a deterministic card-quality validator (every discipline card exposes observable success/failure), then canonical status becomes validator-backed.

## Quality Bar

A useful quality-bar discipline entry must:

- name observable evidence and failure criteria,
- avoid substituting confidence for validation,
- preserve local capability ownership of done criteria,
- cite the framework quality bar,
- require discipline cards to expose success and failure expectations.

## Promotion Guardrail

Quality evidence can recommend further validation, but it cannot promote registry, ontology, glossary, sigil, spell, or task-session results by itself.
