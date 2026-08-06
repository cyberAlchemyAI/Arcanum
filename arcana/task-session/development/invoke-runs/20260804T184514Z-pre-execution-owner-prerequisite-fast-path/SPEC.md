# Specification: Pre-Execution Owner Prerequisite Fast Path

## Status and ownership

- Status: candidate development specification
- Primary lifecycle owner: `sigil-development` for Task Session
- Contributing owners: `sigil-development` for Continuation Router; `spellcraft` for Invoke Plan and Implementation Readiness
- Execution owner after planning: the owner selected by the validated dispatch
- Authority effect: none

## Problem

A selected SWU can declare an owner prerequisite such as Invoke Refresh, yet Task Session may discover it only after ordinary context construction and gate work. The resulting block is correct but late. The operator experiences a long audit where a bounded route decision should have happened first.

A second problem is contradictory handoff language: a plan may name `task-session` as its next route while also saying another owner must run before mutation. The next route and the prerequisite state are then inconsistent.

## Objective

Make plan-to-execution entry deterministic and cheap:

- new plans prefer the already implemented plan-once semantic manifest route;
- genuine owner prerequisites are machine-readable;
- Task Session classifies them before Context Builder;
- exact authorization can admit one owner hop and resume the same bounded attempt;
- missing authorization, ambiguity, or stale evidence returns immediately with one exact repair action.

## Non-goals

- Removing digests, target baselines, material-package validation, or live mutation admission.
- Letting Task Session implement Invoke Refresh semantics.
- Treating a work-pack route declaration as mutation authorization.
- Recursively executing arbitrary next routes or prerequisite DAGs.
- Changing promotion, publication, deployment, destructive-action, policy, or cost authority.
- Making a wall-clock threshold the only correctness test.

## Core types

### `PreExecutionOwnerPrerequisite`

A plan-owned, non-authoritative record with:

- `prerequisite_id`, `task_id`, and `swu_id`;
- exact `owner_route` including mutation mode when consequential;
- typed trigger and source selectors;
- exact target inventory and complete structured validation contracts;
- expected owner receipt type and satisfaction predicate;
- authorization requirement and evidence selector;
- `resume_point=task-session:context-build`;
- `max_owner_hops=1`.

### `PrerequisiteClassification`

One of `satisfied`, `unmet`, `ambiguous`, `stale`, or `invalid`. It records the exact inputs read, a stable prerequisite fingerprint, the permitted next action, and a phase trace.

### `ExecutionEntryState`

One of:

- `plan-once-selection-ready`: semantic plan manifest is current; expected material absence is not a plan defect;
- `owner-prerequisite`: one prerequisite is unmet and has one exact owner;
- `context-ready`: all pre-execution prerequisites are satisfied;
- `blocked`: ambiguity, stale scope, missing contract, cycle, or owner failure prevents safe entry.

## Required behavior

### Plan authoring

1. Invoke Plan must not advertise `task-session` as the immediate next route when a declared prerequisite is unmet.
2. New mutation-capable plans should select `selected-unit-at-task-session` when the semantic plan can be audited once and material is intentionally produced after selection.
3. A plan that genuinely requires a pre-execution owner must emit `PreExecutionOwnerPrerequisite` and route first to Implementation Readiness or the exact owner-preparation route.
4. Legacy full-frontier behavior remains valid and fail-closed.

### Task Session entry

1. After exact task/SWU resolution and before Context Builder, inspect only the selected work pack, selected unit contract, prerequisite record, and referenced satisfaction receipt.
2. If satisfied, continue to normal context construction.
3. If unmet and exact authorization is absent, emit a fast-block receipt with the exact route and missing evidence. Do not build a context pack, hash implementation targets, run mutation admission, inspect implementation code, or emit full run telemetry first.
4. If unmet and exact authorization is present, call Continuation Router for one prerequisite-phase owner hop, join the owner receipt, recheck scope and baselines, and resume at Context Builder once.
5. If ambiguous, stale, invalid, repeated, or cyclic, block before mutation.

### Continuation routing

1. Add a `pre-execution-prerequisite` source phase distinct from terminal optional continuation.
2. Preserve one-hop behavior and owner isolation.
3. Return control to the same bounded Task Session attempt; do not recursively invoke Task Session.
4. A proposal-only or no-op owner receipt satisfies the prerequisite only when the declared satisfaction predicate explicitly accepts it.

## Authority rules

- The plan owns the prerequisite declaration, not its execution.
- Continuation Router owns route matching and receipt joining, not owner work.
- Invoke owns Refresh authoring and material production.
- Task Session owns final live mutation admission and execution.
- Exact authorization must bind route, task, SWU, target inventory, validation contracts, attempt, and allowed effect.
- Approval scope, package targets, target inventory, and validated paths must remain equal after normalization.

## Fast-path budget

Correctness is measured structurally:

- at most four input categories are read before classification;
- no Context Builder phase, mutation-admission phase, implementation inspection, or target mutation occurs before the decision;
- the phase trace proves which phases were skipped;
- a local five-second result is an operational SLO, not the normative acceptance condition.

## Acceptance

1. An unmet unique prerequisite returns before Context Builder when authorization is missing.
2. An exact authorization performs one owner hop, joins a valid receipt, rechecks baselines, and enters Context Builder once.
3. A satisfied prerequisite suppresses duplicate owner work.
4. Stale or expanded scope blocks before mutation.
5. Ambiguous owners never resolve from confidence alone.
6. A repeated fingerprint or attempt cannot dispatch twice.
7. Plan-once fixtures prove zero expected pre-execution Refresh calls.
8. Legacy and strict readiness profiles retain their current safety behavior.
9. Generated surfaces derive from validated canonical changes.
10. Public artifacts contain no consuming-project identifiers or private evidence.
