# TASK-WPEG-ROUTER — Automatic owner routing and outer loop

## Objective

Consume the Work-Pack execution binding so internal owner hops happen without
per-route authorization, then coordinate those hops through the correct outer
owner.

## SWU-WPEG-003 — Admit Work-Pack-bound owner hops

### Primary behavior

Continuation Router accepts a matching active Work-Pack binding as sufficient
for one declared internal owner hop.

### Write scope

- exact contract, schema, validator, and fixture files under
  `arcanum/arcana/continuation-router/`

### Ordered rules

1. Preserve ad hoc exact-route authorization outside a Work-Pack binding.
2. Match Work Pack ID/digest, frontier unit, owner capability/mode, target
   scope, write scope, effect class, required inputs, expected receipt, and
   allowed-routes digest.
3. Require no `--authorize-route` when the match passes.
4. Reject scope expansion, stop-class effects, ambiguous owner, stale binding,
   missing inputs, or unknown route.
5. Invoke at most one owner and join one terminal receipt.
6. Return, but never execute, the owner's next route.

### Acceptance

- Bound declared route dispatches without an authorization flag.
- Same route in ad hoc mode retains existing authorization behavior.
- Undeclared route and wrong target, owner, frontier, write scope, effect
  class, required input, receipt contract, or digest block.
- Owner failure, missing join, repeated fingerprint, and cycle block.
- Existing route fixtures continue to pass.

### Verification

```bash
bash arcanum/arcana/continuation-router/development/run-validation-fixtures.sh
python3 arcanum/arcana/continuation-router/development/validate-route-fixtures.py
```

### Split analysis

One behavior: change the Router's authorization source for a bound route. The
outer loop that supplies and consumes the binding remains separate.

## SWU-WPEG-004 — Implement the outer loop

### Primary behavior

Implementation Readiness binds direct execution intent, chooses automatic
routes, joins owners, and starts Task Sessions until the captured mode stops.

### Write scope

- `arcanum/spells/implementation-readiness/README.md`
- exact new schemas/scripts/fixtures under
  `arcanum/spells/implementation-readiness/`

### Ordered rules

1. Resolve one exact Work Pack and direct execution mode.
2. Build the binding automatically.
3. Classify entry and decision type.
4. Invoke one owner through Continuation Router and join it.
5. Reclassify; invoke one fresh Task Session only when task-ready.
6. Continue within the captured frontier/budget.
7. Stop on completion or a stop-class decision.
8. Record automatic decisions without asking the user.

### Acceptance

- Mechanical owner/tool routes do not prompt.
- Product/scope/destructive/external/authority/failed-critical cases stop.
- Owner and Task Session receipts remain separate.
- Loop cannot absorb a new frontier unit or recursively resume a session.

### Verification

```bash
python3 arcanum/spells/implementation-readiness/development/validate-outer-loop.py
```

### Split analysis

One controller/reducer behavior. Task Session's entry guard is separate so its
owner can validate that lifecycle change independently.
