# Architecture Bundle

## View 1: Context

The operator wants to execute a selected unit. Invoke Plan and Work Pack Readiness Audit produce plan evidence. Task Session owns one bounded execution. Invoke Refresh may own genuine plan repair or material preparation. Continuation Router owns one-hop routing. The defect occurs when the entrypoint performs normal execution preparation before resolving a declared upstream prerequisite.

## View 2: High-level structure

```text
Invoke Plan / readiness audit
  -> ExecutionEntry projection
  -> Task Session selector resolution
  -> prerequisite classifier
       -> satisfied -----------------------> Context Builder -> admission -> execute
       -> plan-once-selection-ready -------> select/materialize -> admission -> execute
       -> unmet + unauthorized ------------> fast-block receipt
       -> unmet + exact authorization -----> Continuation Router -> owner receipt
                                                -> recheck -> Context Builder
       -> ambiguous/stale/cycle -----------> block
```

## View 3: Low-level components

| Component | Responsibility | Must not do |
| --- | --- | --- |
| Plan entry projector | Emit a consistent next route, readiness profile, and typed prerequisite record. | Grant execution or apply authority. |
| Prerequisite classifier | Read the bounded entry set and classify satisfaction. | Build broad context or inspect implementation. |
| Fast-block receipt writer | Return exact route, missing evidence, fingerprint, and skipped phases. | Claim Task Session execution started. |
| Continuation Router phase | Match one prerequisite owner, dispatch once, and join its receipt. | Execute owner semantics or recursively resume Task Session. |
| Owner receipt verifier | Validate identity, scope, status, and satisfaction predicate. | Treat authoring success as mutation readiness. |
| Resume guard | Recheck target scope, baselines, fingerprint, and attempt before Context Builder. | Reuse a receipt across attempts. |
| Plan-once adapter | Reuse the existing semantic manifest and selection/admission route. | Require expected pre-execution Refresh merely because material was absent at plan time. |

## View 4: Workflow process

1. Invoke Plan selects a readiness profile and emits a non-contradictory entry projection.
2. Task Session resolves exactly one task/SWU.
3. The classifier evaluates the entry projection under the structural effort bound.
4. Satisfied and plan-once cases advance without an unnecessary Refresh.
5. An unmet legacy/drift prerequisite either fast-blocks or performs one exactly authorized owner hop.
6. Task Session joins and verifies the owner receipt, rechecks live scope, then starts Context Builder.
7. Normal admission, execution, validation, closeout, and continuity contracts remain unchanged.

## View 5: Decision and state flow

```text
resolved
  -> classified:satisfied -> context-ready
  -> classified:plan-once -> selection-ready -> material-ready -> context-ready
  -> classified:unmet
       -> authorization-missing -> fast-blocked
       -> authorization-matched -> owner-dispatched -> owner-joined
            -> satisfaction-pass -> revalidated -> context-ready
            -> satisfaction-fail -> blocked
  -> classified:ambiguous|stale|invalid -> blocked
```

The same prerequisite fingerprint plus attempt may dispatch at most once. A returned owner next route is reported; it is not recursively executed.

## View 6: Dependency and interface

| Producer | Consumer | Interface | Authority |
| --- | --- | --- | --- |
| Invoke Plan / readiness audit | Task Session | readiness profile, semantic manifest, prerequisite record | planning evidence only |
| Task Session classifier | Continuation Router | prerequisite receipt, exact route authorization, bounded target scope | routing request only |
| Continuation Router | Invoke Refresh or other owner | owner-native input contract | owner retains semantics and mutation gates |
| Owner | Task Session | terminal owner receipt | evidence only; Task Session still admits mutation |
| Task Session | lifecycle closeout owner | terminal execution receipt | bounded execution evidence |

## Key decisions

- Reuse plan-once rather than creating another readiness model.
- Add a pre-Context prerequisite phase rather than weakening Context Builder.
- Measure fast behavior by phase/read budget; report wall time only as operational evidence.
- Keep bare, unauthorized Task Session fail-closed but fast.
- Require explicit exact authorization for an apply-capable owner hop; conversational intent must be normalized into durable scope evidence by the caller or outer composition.

## Risks

- A stale prerequisite record could hide changed plan semantics. Mitigation: bind source selectors and revalidate after the owner hop.
- Automatic resume could be mistaken for recursive continuation. Mitigation: resume the same attempt at a named phase; do not start a second Task Session.
- Timing tests can be flaky. Mitigation: assert phase traces and bounded reads; keep five seconds as an SLO only.
- Public examples could leak consuming-project details. Mitigation: synthetic fixtures only.
