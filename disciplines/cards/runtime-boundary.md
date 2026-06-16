# Runtime Boundary Discipline

Status: active-pattern
Steward: Runtime framework and observed invocation loop

## Purpose

Govern the separation between canonical source, generated install surfaces, and local runtime state so runtime work does not blur public source authority with consuming-repository state.

## Boundary

This discipline names runtime boundary practice. It does not own every runtime adapter, generated package, or local repository state file; those remain with their framework or consuming-repository owner.

## Evidence

- [Runtime framework](../../framework/runtime/README.md) - defines canonical source, generated install surfaces, and local runtime state boundaries.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies runtime boundary as a recurring discipline-like practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `runtime-boundary` as an active-pattern discipline.

## Validation

- Mode: mixed
- Check: runtime boundary review, generated package validation where applicable, and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful runtime boundary discipline entry must:

- keep canonical source, generated install surfaces, and local runtime state separate,
- cite runtime framework authority,
- preserve public/private and source/generated boundaries,
- avoid treating generated packages as source authority,
- name the owner of runtime adapter or install-surface changes.

## Promotion Guardrail

Runtime evidence can recommend boundary or generator work, but it cannot directly promote generated files, local state, registry entries, ontology, glossary, sigils, spells, or discipline status.
