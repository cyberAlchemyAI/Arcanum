# TASK-TSGR-02: Checkpointed Runner

Layer: L1  
Dependencies: TSGR-001 and TSGR-002 accepted

Shared exact paths:

- `arcana/task-session/scripts/task-session-governance-runner.py`
- `arcana/task-session/development/fixtures/governance-runner-cases.json`
- `arcana/task-session/development/validate-governance-runner.py`

## SWU-TSGR-003 — prepare and status

Objective: compose resolver, production evaluator, admission verifier, preflight,
ticket creation, and read-only status.

Done criteria: repeated inputs yield identical material; tie/missing/stale scope
blocks before state mutation; status never advances; checkpoints are monotonic.

Validation:

```text
python3 arcana/task-session/development/validate-governance-runner.py --family prepare
```

Execution status: completed by
`work-pack/results/SWU-TSGR-003-RESULT.json` with result `pass`. The live prepare
family reported `positive=3/3`, `negative=6/6`, and zero undeclared outputs.
Repeated prepare was byte-stable, status performed no writes, and all missing,
tied, stale, skipped, and predecessor-drift cases blocked.

## SWU-TSGR-004 — structured executor join

Objective: launch or join exactly one executor using structured argv/cwd/timeout and
end at an `execution-received` checkpoint.

Done criteria: no shell interpolation; path and timeout controls pass; executor
receipt identity and write order validate; execution failure remains distinct from
governance failure; no reconciliation or live apply occurs.

Validation:

```text
python3 arcana/task-session/development/validate-governance-runner.py --family executor-join
```

Execution status: completed by
`work-pack/results/SWU-TSGR-004-RESULT.json` with result `pass`. The live
executor-join family reported `positive=6/6`, `negative=13/13`, and zero
undeclared outputs. Structured launch, existing receipt join, and idempotent replay
passed; shell-vector and cwd escapes blocked; timeout and nonzero exit remained
execution failures; identity, nonterminal receipt, and final-write drift remained
governance failures. Reconciliation and live apply were not executed.

## SWU-TSGR-005 — reconcile and classify

Objective: verify received executor evidence, declared writes/outputs/validations,
and three-way target classification without applying live bytes.

Done criteria: every target is exactly `apply`, `already-present-exact-output`, or
`conflict`; undeclared/missing paths and unmet critical validation block;
output-only re-admission is explicit; phase ends at `reconciled`.

Validation:

```text
python3 arcana/task-session/development/validate-governance-runner.py --family reconcile
```

Execution status: completed by
`work-pack/results/SWU-TSGR-005-RESULT.json` with result `pass`. The live reconcile
family reported `positive=10/10`, `negative=20/20`, and zero undeclared outputs.
Apply and exact-present targets classified without live writes; conflict, inventory,
critical-validation, output-only re-admission, cardinality, and evidence-drift cases
blocked. Atomic commit, terminal final-write, and resume were not executed.

## SWU-TSGR-006 — atomic commit, terminal write, and resume

Objective: atomically apply only reconciled staged outputs, then enforce
terminal-final-write and crash-safe phase resume as one commit transaction.

Done criteria: interruption after every boundary resumes or blocks deterministically;
non-idempotent effects never duplicate; exact-present output is a recorded no-op;
partial multi-target commit cannot be accepted; terminal receipt is written last;
repeated idempotency key cannot contradict the first accepted result.

Validation:

```text
python3 arcana/task-session/development/validate-governance-runner.py --family commit-resume
```

All SWUs are sequential because they share the runner paths. Common closeout control
applies. Unique successors: TSGR-004, TSGR-005, TSGR-006, and TSGR-007.
