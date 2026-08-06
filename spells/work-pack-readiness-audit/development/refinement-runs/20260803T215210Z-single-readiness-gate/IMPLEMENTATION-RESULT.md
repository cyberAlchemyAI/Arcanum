# Single Readiness Gate — Implementation Result

Result: `pass`.

The opt-in `selected-unit-at-task-session` route is implemented across Work
Pack Readiness Audit, Invoke material production, and Task Session. Planning
now emits a selector-value semantic epoch and a non-authoritative selection
route. Later material production does not require a pre-execution Invoke
Refresh or a second readiness audit. Task Session instead verifies the current
selected unit, material identity, complete validation contract, and live target
baselines, then atomically consumes one attempt-bound admission at executor
launch.

Legacy v1 and strict v2 behavior remain supported and passed their existing
fixtures. The new adversarial fixtures prove status-only epoch stability,
semantic drift invalidation, wrong-attempt rejection, target-TOCTOU rejection,
terminal admission recording, and cross-run replay rejection.

Canonical packages and their repository Codex/Claude mirrors were validated
for exact selective-sync parity. The package-complete Task Session sync also
materialized previously canonical owner-hook runtime files in both mirrors.

This is implementation and local validation evidence only. It is not registry
promotion, release, deployment, or production-readiness evidence.
