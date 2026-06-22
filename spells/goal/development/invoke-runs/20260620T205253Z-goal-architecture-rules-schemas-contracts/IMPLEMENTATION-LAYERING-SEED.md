# Goal Implementation Layering Seed

Status: seed only

This is a design-stage seed for a later Invoke plan or Task Session route. It
does not create work-pack tasks and does not authorize runtime mutation.

## Layer L0 - Source Contract And Design Baseline

Purpose: keep the public spell contract, definitions, architecture, rules,
schemas, and contracts coherent.

Evidence now present:

- `arcanum/spells/goal/README.md`
- `arcanum/spells/goal/decision-profile.schema`
- `20260620T202601Z-goal-spec-definitions/`
- `20260620T205253Z-goal-architecture-rules-schemas-contracts/`

Promotion gate:

- Spellcraft validates source contract and design bundle.

## Layer L1 - Runtime Skeleton

Purpose: implement the smallest runtime substrate for binding scope, reading
frontier, classifying risk, and producing a non-mutating result.

Expected future SWUs:

- bind goal scope,
- read frontier,
- classify risk,
- emit goal loop result.

Gate:

- Protected work stops before routing or mutation.

## Layer L2 - Delegation And Staging

Purpose: validate dispatch routes, collect execution receipts, audit progress,
and stage deltas without applying source mutation.

Expected future SWUs:

- dispatch route adapter,
- receipt closeout validation,
- audit gate,
- staged delta creation.

Gate:

- No active ledger mutation without staged delta and approval token.

## Layer L3 - Approval, Promotion, And Reusable Validation

Purpose: apply approved staged batches through Craft and prove reusable
behavior through Experiment Harness.

Expected future SWUs:

- approval token handling,
- decision record linkage,
- approved Craft apply,
- low/medium/protected-mutation validation fixtures,
- telemetry and promotion-readiness report.

Gate:

- Spell remains draft until Experiment Harness proves fail-closed behavior, gap
  discovery termination, and durable approval records.

## Layering Gaps

| Gap | Route |
| --- | --- |
| No runtime skeleton exists yet. | Invoke plan or Task Session after Spellcraft validation. |
| No reusable behavior fixtures exist yet. | Experiment Harness after runtime skeleton and staging exist. |
| Schema promotion location is undecided. | Spellcraft validation decides whether schemas stay in development or move to `spells/goal/schemas/`. |
