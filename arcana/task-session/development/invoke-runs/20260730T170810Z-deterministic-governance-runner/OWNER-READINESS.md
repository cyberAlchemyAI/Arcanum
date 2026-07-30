# Owner Readiness Dependency

## TSGR-008 prerequisite

Current evidence shows a canonical Continuation Router skill, schema-shaped fixture
logic, and six passing route fixtures, but no production launcher under
`arcana/continuation-router/scripts/`.

Therefore `SWU-TSGR-008` has an external readiness dependency:

```text
dependency_id: continuation-router-production-launcher
required_receipt: work-pack/dependencies/CONTINUATION-ROUTER-READINESS.json
admitted_result: pass
required_proof:
  - exact executable adapter path and digest
  - accepted input and output schema refs and digests
  - one bounded dispatch and joined-owner negative fixtures
  - no recursive continuation
```

TSGR-007 may register that accepted launcher in Task Session's hook-adapter manifest.
It may not fabricate the launcher or absorb Continuation Router semantics. Until the
dependency receipt exists and passes, TSGR-008 remains blocked while the prototype
through TSGR-007 can proceed.

## Post-pilot integration

Canonical Task Session documentation, stale architecture repair, generated mirror
synchronization, and any recommended-path promotion belong to a new Sigil Development
work pack after `SWU-TSGR-010` emits its pilot verdict. They are not part of this
prototype graph.
