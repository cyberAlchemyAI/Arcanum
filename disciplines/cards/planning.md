# Planning Discipline

Status: active-pattern
Steward: Invoke, implementation-layering, task-session

## Purpose

Govern the recurring path from intent definition through design, implementation layering, work-pack planning, and bounded execution so Arcanum plans stay traceable and executable.

## Boundary

This discipline names the planning chain. It does not execute tasks, approve implementation, or replace the owning lifecycle for invoke, implementation-layering, task-session, sigil-development, or spellcraft.

## Evidence

- [Lifecycle Work](../../README.md#lifecycle-work) - describes the recurring chain from invoke and implementation-layering into task-session execution.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies planning as a recurring discipline-like practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `planning` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: `python3 disciplines/scripts/validate-discipline-catalog.py` for catalog row shape, plus review that planning artifacts name owner, scope, gates, and execution boundary.
- Latest result: pass

## Quality Bar

A useful planning discipline entry must:

- separate authoring, design, layering, and execution responsibilities,
- cite concrete lifecycle artifacts,
- require plans to name scope, gates, and validation,
- prevent route-shape evidence from being mistaken for executed work,
- name the next hardening move for plan artifact criteria.

## Promotion Guardrail

Discipline evidence can recommend clearer plan criteria, but it cannot promote a plan, work-pack, SWU, sigil, or spell. Enforcement remains with the lifecycle owner named by the route.
