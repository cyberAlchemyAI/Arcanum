# TASK-TSGR-03: Owner Side Jobs and Continuation

Layer: L2
Dependencies: TSGR-006 accepted

## SWU-TSGR-007 — generic owner hook protocol

Exact write scope:

- `arcana/task-session/schemas/owner-hook-request.schema.json`
- `arcana/task-session/schemas/owner-hook-receipt.schema.json`
- `arcana/task-session/hook-adapters.json`
- `arcana/task-session/scripts/run-owner-hook.py`
- `arcana/task-session/development/fixtures/owner-hook-cases.json`
- `arcana/task-session/development/validate-owner-hook.py`

Done criteria: the versioned adapter manifest binds adapter ID, owner, executable,
input/output schema, and its own digest; structured argv only; exact
owner/schema/path/timeout/idempotency binding; bounded stdout/stderr; malformed,
missing, timed-out, stale-manifest, or owner-mismatched receipts block.

Validation:

```text
python3 arcana/task-session/development/validate-owner-hook.py
```

Execution status: completed by
`work-pack/results/SWU-TSGR-007-RESULT.json` with result `pass`. Both the
canonical no-argument and explicit-root modes reported `positive=4/4`,
`negative=30/30`, `schema=4/4`, and zero undeclared outputs. The first
live no-argument run blocked on root resolution; a one-file admitted recovery passed
while the other five product digests remained unchanged.

## SWU-TSGR-008 — continuation and cursor join

External entry gate: schema-valid
`work-pack/dependencies/CONTINUATION-ROUTER-READINESS.json` satisfying
`OWNER-READINESS.md`.

Exact write scope:

- `arcana/task-session/schemas/continuity-cursor.schema.json`
- `arcana/task-session/scripts/task-session-governance-runner.py`
- `arcana/task-session/scripts/run-owner-hook.py`
- `arcana/task-session/development/fixtures/governance-runner-cases.json`
- `arcana/task-session/development/validate-governance-runner.py`

Done criteria: Task Session invokes only the accepted Continuation Router adapter;
the Continuation Router receipt validates against the exact planning schema and
contains a digest-bound, schema-valid separate Invoke owner receipt for
`invoke:refresh:apply-approved`; owner `pass`/`no-op` joins;
block/timeout/unjoined blocks; unique successor emits one cursor; ambiguous successor
blocks; no successor records terminal completion; no successor executes.

Validation:

```text
python3 arcana/task-session/development/validate-governance-runner.py --family closeout
python3 arcana/continuation-router/development/validate-route-fixtures.py
```

Execution status: blocked before Task Session admission. The required external
`work-pack/dependencies/CONTINUATION-ROUTER-READINESS.json` receipt is absent;
Continuation Router owns that dependency. No SWU-TSGR-008 product mutation or owner
dispatch occurred.

Common closeout control applies. Unique successors: TSGR-008 then TSGR-009.
