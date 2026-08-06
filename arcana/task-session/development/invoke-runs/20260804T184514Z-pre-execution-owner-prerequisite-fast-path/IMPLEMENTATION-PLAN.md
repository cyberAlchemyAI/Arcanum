# Implementation Plan

## Objective

Deliver a generic pre-execution prerequisite fast path without removing current mutation safeguards or duplicating the implemented plan-once readiness model.

## Plan slices

### Slice 1: Contract

Define versioned prerequisite and classification schemas, satisfaction semantics, stable fingerprint material, and the exact authorization matrix. Preserve a clear adapter rule for legacy work packs with no typed prerequisite record.

### Slice 2: Fast classifier

Implement a pure classifier that receives already-resolved task/SWU entry inputs. It returns one classification and phase trace. Instrument exact input categories and forbid Context Builder, implementation inspection, target hashing, mutation admission, and full observability work before classification.

### Slice 3: Owner routing

Extend Continuation Router with a `pre-execution-prerequisite` phase. It dispatches no more than one exactly authorized route, joins the owner receipt, applies the declared satisfaction predicate, and returns control to the same attempt.

### Slice 4: Plan and composition adoption

Update Invoke Plan and the work-pack template so immediate next-route claims agree with prerequisite state. Prefer the existing plan-once profile for intentionally just-in-time material. Update Implementation Readiness guidance so direct user execution intent is normalized into an exact, inspectable prerequisite authorization rather than inferred ambiently.

### Slice 5: Integration and packaging

Run synthetic cross-capability canaries, existing Task Session/Continuation/Invoke/readiness regressions, a private-string scan, and selective generated-package sync. Record implementation evidence without claiming registry promotion.

## Algorithm

```text
resolve one task/SWU
load entry projection and prerequisite handle
if plan-once manifest is current:
    route to selection/material production; do not request expected Refresh
classify prerequisite
if satisfied:
    continue at Context Builder
if ambiguous, stale, invalid, or repeated:
    fast block
if unmet and exact authorization absent:
    fast block with exact route and authorization tuple
dispatch one owner hop
join and validate owner receipt
recheck prerequisite fingerprint, target inventory, and baselines
if satisfaction predicate passes:
    resume same attempt at Context Builder
else:
    block with owner receipt and one repair action
```

## Validation strategy

- schema and pure-function unit tests;
- phase/read-budget assertions;
- one-hop route fixtures;
- exact-authorization and path-equality failures;
- plan-once zero-pre-execution-Refresh canary;
- legacy strict-profile regression;
- generated canonical parity;
- scoped whitespace and public-boundary scans.

## Stop conditions

Stop implementation on unresolved authorization semantics, schema incompatibility, a need for more than one owner hop, stale plan semantics, target-scope expansion, failed acceptance-critical validation, generated-source drift, or any public/private boundary leak.
