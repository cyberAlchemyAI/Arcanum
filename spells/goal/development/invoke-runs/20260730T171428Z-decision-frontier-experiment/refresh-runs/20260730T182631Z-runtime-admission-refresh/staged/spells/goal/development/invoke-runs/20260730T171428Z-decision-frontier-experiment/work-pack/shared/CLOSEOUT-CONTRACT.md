# Task Session Closeout Contract

## Current Owner Route

Task Session execution and lifecycle ownership remain distinct:

- Task Session owns one selected SWU and its terminal source receipt.
- `invoke:refresh:apply-approved` is the only automatic closeout owner route.
- Spellcraft remains the experiment lifecycle owner and owns admission plus the
  final lifecycle decision.

The closeout hop is bookkeeping only. It cannot implement another unit,
select a successor, change authority, promote, publish, or deploy.

## Baseline Binding

Before mutation, the selected Task Session writes:

```text
spells/goal/development/decision-frontier-experiment/session-evidence/<SWU-ID>/baseline.json
```

It contains `swu_id`, `session_id`, exact task-local target inventory,
per-target existence/kind/SHA-256, scoped porcelain state, and a canonical
baseline digest. Missing future files are `exists: false`; globs are forbidden.

## Terminal Source Receipt

The executor writes:

```text
spells/goal/development/decision-frontier-experiment/session-evidence/<SWU-ID>/task-session-receipt.json
```

It must validate against `TASK-SESSION-RECEIPT.schema.json` and the semantic
validator in `work-pack/shared/validate-task-session-receipt.py`. A pass binds
the exact work-pack digest, unit/step identity, baseline, material/output
partition, artifacts, validation, empty blockers, empty undeclared writes,
authority effect `none`, and one eligible but unselected successor.

## Closeout Owner Receipt

The exact closeout route writes:

```text
spells/goal/development/decision-frontier-experiment/session-evidence/<SWU-ID>/owner-receipt.json
```

It validates against `CLOSEOUT-RECEIPT.schema.json` and records
`owner: invoke:refresh:apply-approved`, `lifecycle_owner: spellcraft`, the
source-receipt digest, re-run validation evidence, exact validated targets,
admitted delta classes, empty blockers, and one eligible but unselected
successor.

## Allowed Closeout Delta Classes

- `evidence_added`
- `blocker_opened`
- `blocker_resolved`
- `status_changed`
- `route_changed`

Implementation, deletion, canonical authority change, tracker mutation,
private export, successor selection, promotion, publication, and deployment
are forbidden.

## Successor Rule

A successor becomes eligible only when all predecessor closeout receipts pass
and no blocker affects its boundary. Eligibility never implies selection.
The outer `task-session-until-blocker` controller may select the unique
successor only under the user's explicit series authorization.
