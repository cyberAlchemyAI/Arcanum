# TASK-TSGR-04: Observation and Pilot Evidence

Layer: L3  
Dependencies: TSGR-008 accepted

## SWU-TSGR-009 — observe and deduplicate

Exact write scope:

- `arcana/task-session/scripts/task-session-governance-runner.py`
- `arcana/task-session/development/fixtures/governance-runner-cases.json`
- `arcana/task-session/development/validate-governance-runner.py`

Done criteria: official observer is invoked by ref/digest; duplicate key is a no-op;
private payload is not projected; append, failure, and dedupe evidence remain
distinct; observer failure does not rewrite the implementation result.

Validation:

```text
python3 arcana/task-session/development/validate-governance-runner.py --family observe
```

## SWU-TSGR-010 — paired experiment and pilot verdict

Exact write scope:

- `arcana/task-session/development/experiments/governance-runner/EXPERIMENT.md`
- `arcana/task-session/development/experiments/governance-runner/run-experiment.py`
- `arcana/task-session/development/experiments/governance-runner/fixtures.json`
- `arcana/task-session/development/experiments/governance-runner/PILOT-VERDICT.md`

Done criteria: paired manual/runner scenario reports latency, interventions, reads,
acceptance coverage, and verdict; product-neutral leak scan passes; verdict is
`opt-in-pilot`, `revise`, or `reject`; no speed, recommended-path, production,
canonical integration, mirror, or promotion claim exceeds evidence.

Validation:

```text
python3 arcana/task-session/development/experiments/governance-runner/run-experiment.py --fixture
```

Common closeout control applies. TSGR-009 successor is TSGR-010; TSGR-010 returns a
terminal continuity cursor. If the verdict is `opt-in-pilot`, a new Sigil Development
work pack may plan canonical docs, stale architecture repair, generated mirrors, and
promotion. This work pack does not perform them.
