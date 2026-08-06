# TASK-WPEG-CONTRACT — Execution contract and Plan projection

## Objective

Define the bounded execution contract and make Invoke Plan/readiness output one
truthful entry state before any routing runtime changes.

## SWU-WPEG-001 — Validate the execution contract

### Primary behavior

Validate `ExecutionPolicy`, `AllowedRoutesProjection`,
`ExecutionEntryProjection`, and `ExecutionIntentBinding` as one coherent
plan-to-runtime contract.

### Inputs

- `SPEC.md`
- `architecture-bundle.md`
- existing plan-once manifest and selection schemas
- existing Continuation Router and Task Session receipt contracts

### Write scope

- `arcanum/spells/implementation-readiness/schemas/`
- `arcanum/spells/implementation-readiness/scripts/`
- `arcanum/spells/implementation-readiness/development/fixtures/`

### Ordered rules

1. Bind one exact Work Pack semantic identity and finite frontier.
2. Require declared write scope, validation, automatic decisions, and stop
   decisions.
3. Require exact per-frontier capability, mode, target, write scope, effect
   class, typed inputs, and expected receipt; bind their canonical digest.
4. Reject overlap between automatic and stop decision classes.
5. Require entry state and next owner to agree.
6. Treat the direct execution request as the source of bounded execution
   intent; do not require a second approval artifact.
7. Mark the binding non-promotional and non-expandable.

### Acceptance

- Valid local/reversible policy passes.
- Unknown frontier, escaping path, missing validation, stale Work Pack digest,
  contradictory route, automatic destructive action, and automatic promotion
  each fail with stable diagnostics.
- Undeclared route, target/write expansion, effect/input/receipt mismatch, and
  stale/replayed allowed-route digest each fail.
- Fixture validator is deterministic.

### Verification

```bash
python3 arcanum/spells/implementation-readiness/scripts/validate_execution_contracts.py
```

### Split analysis

Schemas and their validator form one acceptance boundary. They cannot be split
without leaving either semantics or executable proof absent.

## SWU-WPEG-002 — Emit one Plan execution-entry state

### Primary behavior

Make Invoke Plan and Work Pack Readiness outputs state the true next owner and
recommended readiness profile.

### Inputs

- passing SWU-001 contract receipt
- `arcanum/spells/invoke/plan.md`
- `arcanum/spells/invoke/templates/work-pack.md`
- Work Pack Readiness Audit plan-once implementation

### Write scope

- `arcanum/spells/invoke/plan.md`
- `arcanum/spells/invoke/templates/work-pack.md`
- exact Work Pack Readiness Audit schema/script/fixture files required to emit
  the projection

### Ordered rules

1. Recommend `selected-unit-at-task-session` for new plans.
2. Emit exactly one entry state.
3. Emit a closed allowed-routes projection and digest.
4. Use `selection-ready` for expected future material.
5. Use `owner-prerequisite` for real semantic repair/materialization needs.
6. Never emit Task Session as next route while a prerequisite is unresolved.
7. Preserve legacy strict profiles and source compatibility.

### Acceptance

- Positive plan-once fixture emits `selection-ready`.
- Semantic-drift fixture emits exact Invoke Refresh owner route.
- Contradictory next-route fixture blocks.
- Existing Invoke and readiness suites still pass.

### Verification

```bash
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
bash arcanum/spells/work-pack-readiness-audit/development/run-validation-fixtures.sh
python3 arcanum/spells/work-pack-readiness-audit/development/test_plan_once_end_to_end.py
```

### Split analysis

This is one producer behavior across the canonical Plan and readiness
projection. Router consumption belongs to the next task.
