# Invoke Refresh Direct-User Default Reflection

## Trigger

The operator corrected the Refresh interaction policy on 2026-07-23: a direct
user invocation should default to `apply-approved`, not `proposal-only`.

## Superseded Decision

Earlier Refresh design and interrogation artifacts selected `proposal-only` as a
universal default to prevent silent mutation. Those artifacts remain historical
evidence, but their universal-default conclusion is superseded by this
reflection and the current `refresh.md` contract.

## Revised Contract

1. An explicit mutation mode always wins.
2. A direct user invocation with no explicit mode resolves to `apply-approved`.
3. A delegated or continuation activation with no explicit mode resolves to
   `proposal-only`.
4. A direct request supplies approval evidence only for the exact declared
   scope.
5. Material-package, dependency, owner, publication, path, and validation gates
   remain fail-closed and cannot be bypassed by approval.
6. Refresh records activation source and mutation-mode source so default
   resolution is auditable.

## Preservation Boundary

This change does not authorize target-task execution, discovered paths, broad
upstream mutation, or lifecycle promotion. It changes the default mutation mode
for direct user activation while retaining deterministic material admission.

## Validation

- `arcanum/spells/invoke/development/run-material-package-fixtures.sh`
- `arcanum/spells/invoke/development/run-capability-status-fixtures.sh`
- `arcanum/spells/invoke/development/run-validation-fixtures.sh`
