# UX Plan: Task Session Governance Runner

## Operator promise

One command advances one exact SWU governance run as far as admitted evidence allows.
Normal output is short; diagnostic evidence remains in the run directory.

## Commands

```text
task-session-governance-runner.py prepare <request.json>
task-session-governance-runner.py reconcile <run-dir>
task-session-governance-runner.py closeout <run-dir>
task-session-governance-runner.py observe <run-dir>
task-session-governance-runner.py status <run-dir>
```

A later wrapper may compose admitted phases, but the phase commands remain available
for diagnosis and safe resume.

## Summary contract

Every command prints:

```text
RESULT=<pass|flag|block|no-op>
RUN_ID=<id>
SWU_ID=<id>
PHASE=<phase>
EVIDENCE=<path>
NEXT=<exact command, owner route, or none>
```

On block it also prints:

```text
CODE=<stable diagnostic code>
OWNER=<repair owner>
REPAIR=<one bounded repair>
```

No summary claims the SWU is complete until the terminal executor receipt,
acceptance validation, owner receipt join, and terminal runner receipt all pass.

## Recovery

`status` is read-only. It identifies the last accepted phase, verifies the digest
chain, and prints the exact admissible next phase. It never repairs or advances state.

## Accessibility

The terminal surface does not rely on color, animation, or cursor position. Stable
keys are machine-readable, explanatory text is plain language, and evidence paths
are copyable.

## UX acceptance

- the same blocker always yields the same code and phase;
- a user can distinguish “implementation succeeded but closeout blocked” from
  “implementation failed”;
- no success line hides a missing owner receipt;
- normal pass output fits within one terminal screen;
- private stdout/stderr is not echoed beyond its bounded policy.

