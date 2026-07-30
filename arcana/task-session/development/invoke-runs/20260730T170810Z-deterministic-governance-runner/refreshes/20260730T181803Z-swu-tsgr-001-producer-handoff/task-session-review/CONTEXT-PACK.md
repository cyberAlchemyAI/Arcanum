# Task Session Context Pack: SWU-TSGR-001

## Scope

- Task: `TASK-TSGR-01`
- SWU: `SWU-TSGR-001`
- Mode: standard, strict
- Selected sources: 14
- Strict coverage: pass for review; mutation gate blocked

## Evidence result

The lifecycle dependency is accepted and the exact five implementation files are
staged with a closed Sigil Development producer receipt. Producer validation passes
25/25 golden cases, 5/5 fail-closed cases, 4/4 schema checks, the current 25-case
regression, exact-reference validation, target-absence validation, and a zero
undeclared-output scan.

Staging is not implementation completion. The remaining pre-mutation gate is exact
user approval for applying the five public Arcanum targets. Invoke must then build
and validate the materialized package, and Task Session must bind it into a fresh
mutation-admission receipt.

## Exact material writes

- `arcanum/arcana/task-session/scripts/evaluate-governance.py`
- `arcanum/arcana/task-session/schemas/governance-evaluation-request.schema.json`
- `arcanum/arcana/task-session/schemas/governance-evaluation-receipt.schema.json`
- `arcanum/arcana/task-session/development/fixtures/governance-evaluation-cases.json`
- `arcanum/arcana/task-session/development/validate-governance-evaluator.py`

All five are absent at this review frontier.

## Execution output

The only predeclared Task Session execution output is:

`arcanum/arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/work-pack/results/SWU-TSGR-001-RESULT.json`

It may be written only after admitted material apply and live validation.

## Acceptance-critical validation

From `arcanum/` after apply:

```text
python3 arcana/task-session/development/validate-governance-evaluator.py
python3 arcana/task-session/development/validate-decision-validation-policy.py
```

## Blocker

`TSGR-APPLY-001`: applying the five staged files is consequential and cannot be
auto-selected. It is reversible, bounded, and recommended, but requires an exact
human decision.

## Exclusions

No dirty existing Task Session file, generated mirror, planning record, historical
receipt, publication, promotion, commit, successor SWU, or Experiment Harness state
is in this apply scope.
