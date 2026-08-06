# TASK-WPEG-TASK-SESSION — Fast entry and fresh-session resumption

## Objective

Prevent expensive wrong-owner Task Session work and safely resume execution
after an automatic prerequisite hop.

## SWU-WPEG-005 — Fast prerequisite guard

### Primary behavior

Task Session classifies the execution entry before Context Builder, deep
material checks, or mutation admission.

### Write scope

- exact contract, schema, script, and fixture files under
  `arcanum/arcana/task-session/`

### Ordered rules

1. Resolve exact Work Pack, selected unit, binding, and entry projection.
2. Verify their identities and entry state.
3. Return `proceed` only for Task-ready input.
4. Return `route-owner` with an exact owner packet for a prerequisite.
5. Return `block` for stale, contradictory, unsafe, or ambiguous input.
6. Do not build a full context pack when returning `route-owner` or `block`.

### Acceptance

- Declared prerequisite returns before Context Builder is invoked.
- Read-set/phase counter proves the fast path touches only declared entry
  evidence.
- Task-ready route still performs full existing context/admission behavior.
- No mutation occurs on route-owner/block paths.

### Verification

```bash
bash arcanum/arcana/task-session/development/run-validation-fixtures.sh
python3 arcanum/arcana/task-session/development/test_plan_once_admission.py
python3 arcanum/arcana/task-session/development/test_plan_once_governance.py
```

### Split analysis

One early classification behavior. It does not change the outer loop or
single-use mutation admission.

## SWU-WPEG-006 — Resume through a fresh Task Session

### Primary behavior

The series controller consumes one joined prerequisite owner receipt and starts
a fresh Task Session for the same selected unit.

### Write scope

- exact canonical contract, schema, runtime, and fixture files under
  `arcanum/spells/task-session-until-blocker/`

### Ordered rules

1. Preserve the original selected unit and frontier.
2. Join one prerequisite owner receipt.
3. Reject unchanged blocker fingerprints and cycles.
4. Reclassify entry from current evidence.
5. Start a new Task Session; never recursively resume the blocked one.
6. Retain one Task Session receipt per unit.

### Acceptance

- Passing owner receipt produces one fresh Task Session start.
- Blocking/missing/stale/mismatched receipt stops.
- Same fingerprint or repeated session cursor stops.
- Frontier and session budget cannot expand.
- Existing chain fixtures remain green.

### Verification

```bash
bash arcanum/spells/task-session-until-blocker/development/run-validation-fixtures.sh
python3 arcanum/spells/task-session-until-blocker/development/validate-chain-v2.py
```

### Split analysis

One continuation behavior at the existing series owner; cross-capability proof
belongs to integration.

