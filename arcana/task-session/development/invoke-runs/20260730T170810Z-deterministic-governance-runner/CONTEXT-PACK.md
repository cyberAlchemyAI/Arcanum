# Context Pack: Deterministic Task Session Governance Runner

Run: `20260730T170810Z-deterministic-governance-runner`

## Objective

Define, design, and plan a Sigil Development work pack that makes Task Session's
governance steps faster and deterministic without turning Task Session into an
implementation daemon or absorbing the authority of Continuation Router, Invoke,
or Signal Observer.

## Selected authority

| Source | Selected contract |
| --- | --- |
| `arcana/task-session/SKILL.md` | current Task Session process, mutation admission, closeout preflight, and continuation boundary |
| `arcana/task-session/decision-validation-policy.json` | machine-readable policy outcomes and allowed closeout delta classes |
| `arcana/task-session/scripts/resolve-nearest-swu.py` | scope resolution only; explicitly not readiness |
| `arcana/task-session/scripts/verify-mutation-readiness.py` | production mutation-admission consumer |
| `arcana/task-session/development/validate-decision-validation-policy.py` | development-only pure evaluators that need a production owner |
| `arcana/task-session/development/fixtures/decision-validation-cases.json` | current policy parity corpus |
| `arcana/continuation-router/SKILL.md` | continuation routing and owner-dispatch boundary |
| `spells/invoke/scripts/material_package_validator.py` | deterministic material-package validation seam |
| `spells/invoke/scripts/refresh_material_handoff.py` | deterministic Refresh handoff seam, not application authority |
| `framework/observability/scripts/observe-invocation.sh` | append-only, deduplicated observation hook |

All paths above are relative to the `arcanum/` repository root.

## Live evidence

- Task Session policy fixtures pass `25/25`.
- nearest-SWU fixtures pass `11/11`.
- mutation-admission fixtures pass `23/23`.
- Continuation Router fixtures pass `6/6`.
- The production gap is orchestration: closeout evaluators are development-only,
  Continuation Router has no production runner, and no checkpointed controller
  joins resolution, policy, admission, execution evidence, closeout, and observation.

These counts are evidence of the current contracts, not evidence that the proposed
runner exists.

## Current-state constraint

The Task Session canonical package is already dirty, including pending
mutation-admission contract changes. This Invoke run does not normalize or overwrite
those changes. Every later mutation-capable SWU must bind the exact live digest at
its own preflight and block on an unexpected delta.

`TASK-SESSION-ARCHITECTURE-DESIGN.md` is stale where it assigns direct work-pack
synchronization to Task Session. The current `SKILL.md` requires the separate
Continuation Router to Invoke owner hop. This run follows the live skill and records
the stale prose as repairable residue.

## Excluded candidates

- Any consuming-project prose, fixtures, paths, and telemetry.
- a long-running daemon, network service, or new authority plane.
- arbitrary shell command execution from an untrusted manifest.
- automatic next-SWU execution.
- direct implementation of Invoke Refresh or Continuation Router semantics.
- generated `.agents/skills` mutation before canonical Arcanum acceptance.
- commit, push, publication, or promotion.

## Handoff

The package stops at a Sigil Development work pack. Sigil Development must accept,
narrow, or reject the work pack before Task Session executes any implementation SWU.
