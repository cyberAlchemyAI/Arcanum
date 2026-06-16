# Validation Experiment Discipline

Status: canonical
Steward: Experiment Harness

## Purpose

Govern repeatable validation through fixtures, reports, runs, and promotion evidence so executable or high-risk disciplines can be tested before they become authority.

## Boundary

This discipline names validation experiment practice. It does not author each capability's fixtures, guarantee promotion, or replace the owning lifecycle's acceptance criteria.

## Evidence

- [Experiment Harness Standard](../../framework/EXPERIMENT-HARNESS-STANDARD.md) - defines fixture, report, and promotion evidence expectations.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies validation discipline as a canonical pattern.
- [Discipline Catalog](../DISCIPLINES.md) - records `validation-experiment` as canonical.

## Validation

- Mode: fixture
- Check: experiment harness fixtures and reports, plus `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful validation experiment discipline entry must:

- cite fixture and report evidence,
- separate test harness structure from capability-local success criteria,
- require promotion evidence before status changes,
- preserve failed or blocked validation as useful evidence,
- name the smallest validation route needed for the discipline.

## Promotion Guardrail

Validation evidence can support promotion decisions, but it cannot directly promote capabilities, knowledge entries, or discipline status without the named owner and mutation boundary.
