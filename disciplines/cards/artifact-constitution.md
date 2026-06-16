# Artifact Constitution Discipline

Status: canonical
Steward: Constitution Governance

## Purpose

Govern artifact authority classes such as source, durable evidence, generated output, and local runtime state so new artifacts enter the repository with explicit ownership and promotion boundaries.

## Boundary

This discipline names artifact authority rules. It does not decide the content of a capability artifact, promote generated surfaces to source authority, or override repository-specific ownership.

## Evidence

- [Artifact Constitution](../../framework/ARTIFACT-CONSTITUTION.md) - defines the source, durable evidence, generated, and local runtime artifact classes.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies artifact discipline as a canonical framework practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `artifact-constitution` as canonical.

## Validation

- Mode: mixed
- Check: artifact constitution review, available artifact validators, and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful artifact constitution discipline entry must:

- preserve source versus generated versus runtime authority,
- cite the canonical artifact constitution,
- require explicit owner and promotion boundaries,
- avoid treating evidence as downstream authority,
- name the next metadata or validation hardening move.

## Promotion Guardrail

Discipline evidence can recommend artifact classification and validation work, but it cannot directly promote artifacts or mutate capability-local artifact contracts.
