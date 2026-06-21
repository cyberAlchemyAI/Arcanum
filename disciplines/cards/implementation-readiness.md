# Implementation Readiness Discipline

Status: deprecated
Steward: Implementation Layering and implementation-readiness spell
Superseded by: `planning` (merged 2026-06-21 — the planning chain absorbs the smallest-responsible-layer readiness rule)

## Purpose

DEPRECATED — merged into the [planning discipline](planning.md). Govern readiness to implement by selecting the smallest responsible layer, naming prerequisites, validation, boundaries, and stop conditions before mutation. This rule now lives as a planning sub-rule; this card is retained for provenance only.

## Boundary

This discipline names implementation readiness practice. It does not execute implementation, override task-session, or widen scope beyond the selected layer.

## Evidence

- [Implementation Layering](../../transmutations/implementation-layering/README.md) - defines small evidence-based implementation layers and promotion criteria.
- [Discipline Catalog](../DISCIPLINES.md) - records `implementation-readiness` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: implementation layering/readiness review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful implementation readiness discipline entry must:

- name the smallest responsible implementation layer,
- identify prerequisites, blockers, and validation surface,
- preserve task-session execution boundaries,
- avoid broad implementation mutation before readiness is proven,
- route unresolved choices through Decision Gate or the owning lifecycle.

## Promotion Guardrail

Implementation readiness evidence can authorize a bounded implementation route, but it cannot directly execute or promote the result.
