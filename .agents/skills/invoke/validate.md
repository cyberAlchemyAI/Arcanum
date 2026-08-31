# Invoke Validate Mode

## Identity

- Spell: `invoke`
- Mode: `validate`
- Status: deferred

## Deferral Reason

Validate mode is intentionally out of L0 scope. It is introduced once lifecycle stages beyond define are implemented and need explicit pass or fail governance.

## Planned Activation Gate

- at least one non-define mode is implemented,
- validation checks are stable and auditable,
- lifecycle owner confirms L3 promotion readiness.

## Planned Scope (Draft)

- verify mode contracts against gates and output obligations,
- detect unresolved blocker leakage across lifecycle boundaries,
- emit validation verdict with remediation routes.

## Output Contract (Deferred)

When implemented, this mode will return a standard Invoke Result with mode `validate` and validation evidence outputs.
