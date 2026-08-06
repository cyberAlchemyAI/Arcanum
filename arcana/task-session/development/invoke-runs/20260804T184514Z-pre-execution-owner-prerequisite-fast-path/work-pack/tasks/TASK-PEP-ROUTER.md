# TASK-PEP-ROUTER: Owner hop and same-attempt resume

## SWU-PEP-003

Primary behavior: route one pre-execution owner hop.

### Ordered rules

1. Add `pre-execution-prerequisite` as a typed Continuation Router source phase.
2. Consume the classifier receipt, exact authorization, and owner-native inputs.
3. Select only one unambiguous owner route.
4. Dispatch once, join once, and preserve owner authority.
5. Return the owner receipt and control handle to Task Session.

### Independent acceptance

Authorized, unauthorized, ambiguous, unknown-owner, and repeated-fingerprint fixtures pass without owner mutation inside the router.

## SWU-PEP-004

Primary behavior: verify the joined owner receipt and resume the same Task Session attempt once.

### Ordered rules

1. Match the owner receipt to route, task, SWU, attempt, target inventory, validation contracts, package identity, and satisfaction predicate.
2. Rehash declared live target baselines after the owner hop.
3. Atomically mark the prerequisite fingerprint consumed for this attempt.
4. Resume at `task-session:context-build`, not selector resolution and not a new Task Session.
5. Preserve normal Context Builder, mutation admission, validation, closeout, and continuity gates.

### Failure modes

- owner receipt authored successfully but not mutation-ready;
- stale receipt or source selector;
- expanded package target;
- changed baseline;
- reused attempt/fingerprint;
- returned next route tries to recurse;
- owner helper is unjoined or open.

### Validation

```bash
bash arcanum/arcana/continuation-router/development/run-validation-fixtures.sh
python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/test_owner_resume.py
```
