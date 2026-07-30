# Context Pack: SWU-TSGR-001 Producer Handoff

Run: `20260730T181803Z-swu-tsgr-001-producer-handoff`

## Objective

Correct the blocked continuation route for `SWU-TSGR-001`. Invoke Refresh owns the
delta classification and the next-owner handoff. It does not own implementation
material production and, in `proposal-only` mode, cannot authorize mutation.

## Evidence-bound finding

The preflight blocker is real: Task Session cannot admit a reusable material
mutation without a digest-bound material package, its validation receipt, and the
exact producer receipt schema. The originally recorded repair owner was wrong.

The live Invoke contract makes `proposal-only` non-mutating, and its material-package
schema requires a proposal-only package to contain no changes, targets,
dependencies, mirrors, or validation commands. Current research evidence also
rejects generic Refresh as the normal material-production lane. Therefore:

1. Invoke authors this proposal and an exact Sigil Development producer handoff.
2. Sigil Development stages the five `SWU-TSGR-001` outputs outside canonical
   targets and emits a schema-bound producer receipt.
3. Only those staged bytes can be bound into an `apply-approved` material package.
4. Task Session may run mutation admission only after that package validates.

## Exact future material scope

- `arcanum/arcana/task-session/scripts/evaluate-governance.py`
- `arcanum/arcana/task-session/schemas/governance-evaluation-request.schema.json`
- `arcanum/arcana/task-session/schemas/governance-evaluation-receipt.schema.json`
- `arcanum/arcana/task-session/development/fixtures/governance-evaluation-cases.json`
- `arcanum/arcana/task-session/development/validate-governance-evaluator.py`

All five targets are absent at this evidence frontier. Existing dirty canonical
Task Session files are excluded and must remain untouched.

## Required validation after a later admitted apply

From `arcanum/`:

```text
python3 arcana/task-session/development/validate-governance-evaluator.py
python3 arcana/task-session/development/validate-decision-validation-policy.py
```

## Authority ceiling

This pack proves only a complete proposal and owner route. It is not staged
implementation, apply approval, mutation admission, implementation, or work-pack
completion evidence.
