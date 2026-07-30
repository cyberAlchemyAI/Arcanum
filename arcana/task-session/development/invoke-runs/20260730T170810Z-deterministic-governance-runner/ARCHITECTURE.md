# Design: Deterministic Task Session Governance Runner

Status: proposed  
Design owner: Invoke  
Lifecycle owner: Sigil Development for `task-session`

## Design stance

The runner is a deterministic local control shell around existing authorities. It
owns phase ordering, checkpoint validation, and its own evidence. It does not own
implementation semantics, successor selection semantics, planning synchronization,
or observability interpretation.

## System context

```text
Operator
  -> Task Session Governance Runner
       -> Scope Resolver
       -> Governance Evaluator
       -> Mutation Admission Verifier
       -> Execution Ticket
  -> separate Implementation Executor
       -> Executor Receipt
  -> Task Session Governance Runner
       -> Reconciler / Target Classifier
       -> Continuation Router owner hook
            -> Invoke Refresh owner hook
       -> Continuity Cursor
       -> Signal Observer hook
```

Every arrow is an artifact or registered process boundary. It is not implicit
authority transfer.

## 1. Container and component view

### `evaluate-governance.py`

A pure production CLI extracted from the development evaluator. It consumes a
versioned request plus `decision-validation-policy.json` and emits one receipt. It
owns no filesystem mutation beyond its explicitly named output receipt.

### `task-session-governance-runner.py`

A bounded phase controller. Subcommands:

- `prepare`: resolve, evaluate, admit, and emit the execution ticket;
- `reconcile`: join the executor receipt and validate writes/outputs;
- `closeout`: run registered owner hooks and join their receipts;
- `observe`: invoke the official observer and finalize the run;
- `status`: validate and render the current checkpoint without advancing it.

The controller never receives arbitrary shell text. Hook and executor launches use
structured argv arrays from an allowlisted adapter registry or explicit trusted CLI
arguments.

### Reconciler

Compares exact baseline, staged, and live digests; validates declared writes and
outputs; enforces terminal-write ordering; and requests output-only re-admission
when applicable.

### Hook adapter

Projects a common request envelope to an owner-specific process, applies a timeout,
captures bounded output, validates the returned receipt, and joins it. It does not
translate or reimplement owner decisions.

## 2. Runtime flow view

```text
prepare
  resolve unique SWU
  -> evaluate policy
  -> mutation admission
  -> closeout prerequisite preflight
  -> execution ticket

external execution
  ticket -> executor -> terminal executor receipt

reconcile
  verify ticket chain
  -> classify targets
  -> validate declared write/output set
  -> validate acceptance commands
  -> reconciled receipt

closeout
  reconciled receipt
  -> Continuation Router hook
  -> if authorized: Invoke Refresh hook with apply-approved
  -> join owner receipt
  -> continuity cursor

observe
  bounded refs/digests -> Signal Observer
  -> terminal runner receipt
```

The controller may stop after any phase. Resume first validates the entire receipt
chain and current target digests. A skipped or repeated non-idempotent phase blocks.

## 3. Data and state view

### Run directory

Consumer-local run evidence is the only state store:

```text
run/
  request.json
  checkpoints/
    01-resolved.json
    02-governed.json
    03-admitted.json
    04-ticketed.json
    05-execution-received.json
    06-reconciled.json
    07-closeout-joined.json
    08-observed.json
  hooks/
    <hook-id>.request.json
    <hook-id>.receipt.json
  terminal-receipt.json
```

Checkpoints form a digest chain. A phase writes to a temporary sibling, validates
the bytes, then atomically replaces its final path. The terminal receipt is last.

### Authority

The run directory is generated evidence, not canonical policy authority. Canonical
rules remain in Task Session policy, schemas, and skill prose. Consumer-private
payloads do not enter public fixtures or public observability.

### Concurrency

One lock is scoped to one run ID. The runner rejects a second writer, stale lock
identity, or conflicting idempotency key. Different run IDs may proceed concurrently
only when their declared write sets are disjoint; otherwise the admission layer
blocks.

## 4. Interface and integration view

### Governance evaluator request

Required fields: schema version, evaluation kind, policy digest, exact input,
request ID, and output path. Result: `PROCEED`, `PASS`, `NO_OP`, `FLAG`, or `BLOCK`
as allowed by the selected policy kind.

### Execution ticket

Required fields: run/SWU/work-pack identity, source and control digests, baseline
inventory, allowed writes, declared outputs, validation contracts, executor receipt
schema, timeout, idempotency key, and closeout contract.

### Executor interface

The runner may launch or join an executor using structured `argv`, `cwd`, `timeout`,
and environment-name allowlist. No string is evaluated by a shell. The executor
receipt names touched files, output digests, validation results, terminal sequence,
and residue.

### Owner hook interface

Required fields: hook ID, owner capability, phase, request/receipt schema refs,
input refs and digests, structured argv, cwd, timeout, idempotency key, allowed
output paths, and expected receipt path. The joined result records the child exit
status, receipt digest, owner result, and bounded-output metadata.

Invoke continuation hooks must carry the exact route tuple
`invoke:refresh:apply-approved`.

### Compatibility

The current agent-led Task Session path remains supported during the opt-in pilot.
The runner initially productionizes existing policy without changing policy meaning.
Only Sigil Development acceptance plus experiment evidence can make the runner the
recommended path.

## 5. Security and trust view

Trust boundaries:

- consumer input to canonical evaluator;
- runner to implementation executor;
- runner to owner hook;
- private run evidence to public observability;
- staged bytes to live target.

Controls:

- JSON Schema validation at every boundary;
- exact path containment and symlink rejection for writable targets;
- structured argv without shell interpolation;
- digests for policy, baselines, staged output, receipts, and predecessors;
- allowlisted hook owner and receipt schema;
- bounded stdout/stderr capture with truncation evidence;
- no secret or raw private-payload projection to public telemetry;
- fail-closed timeout and non-zero exit handling;
- three-way target classification before application.

Abuse cases include path traversal, receipt forgery, digest replay, owner
impersonation, undeclared write, shell injection, oversized log exfiltration, and
ambiguous successor selection. Each must have a negative fixture before pilot.

## 6. Operations and evolution view

### Release sequence

1. production evaluator, schemas, and golden parity;
2. read-only/dry-run checkpointed controller;
3. reconcile and idempotent target classification;
4. bounded application/executor join and crash-safe terminal receipt;
5. generic side-job hook protocol;
6. continuation/cursor join;
7. observation;
8. paired experiment and bounded opt-in pilot verdict.

Canonical documentation repair and generated mirror synchronization require a new
Sigil Development work pack after the pilot verdict.

### Failure and recovery

- A failed phase leaves the last accepted checkpoint authoritative.
- Resume revalidates policy and source digests; drift blocks instead of silently
  upgrading a live run.
- A missing owner receipt is a blocker, never a successful timeout.
- `already-present-exact-output` is recorded as idempotent adoption, not another
  write.
- An observer failure flags terminal observability residue but cannot rewrite the
  completed implementation result; promotion remains blocked until residue closes.

### Rollback

The pilot is additive. Removing the optional runner entry point returns Task Session
to the agent-led path. Canonical policy changes are out of scope for the runner
itself.

## Selected concern extensions

### Authority and trust

The execution ticket authorizes one bounded implementation attempt. It does not
approve lifecycle changes or planning synchronization. Owner receipt joins prove a
separate authority acted.

### Persistence and concurrency

Digest-chained atomic checkpoints plus a run-scoped lock provide crash safety.
Cross-run write-set overlap is rejected at admission.

### Failure and compensation

The only automatic “compensation” is safe resume or no-op adoption of exact staged
bytes. Divergent live state blocks for human or owner resolution.

### Integration and versioning

All request, ticket, phase, hook, executor, cursor, and terminal receipts are
versioned. Unsupported versions block. Owner-specific semantics stay behind adapters.

### Data lifecycle

Public surfaces store schemas and synthetic fixtures only. Consumer-local evidence
may contain paths and bounded output. Public observations receive refs and digests,
not payloads.

### UX

Normal operation is one command plus a concise phase summary. Detailed artifacts are
links/paths for diagnosis. A blocker names the failed phase, exact evidence path,
owner, and repair; it never emits “governance failed” without a discriminating code.

### Validation contracts

Design witnesses `TSGR-FIX-001` through `TSGR-FIX-011` and `TSGR-EXP-001` are
planned, not executed evidence. Pilot readiness requires all fixture witnesses;
recommended-path promotion additionally requires the paired experiment.

## Rejected alternatives

- **One monolithic script containing all semantics**: rejects owner boundaries and
  duplicates policy.
- **Automatic recursive next-SWU loop**: violates Task Session's one-SWU ceiling.
- **Free-text hook commands**: introduces shell and authority ambiguity.
- **Direct Task Session work-pack mutation**: bypasses Continuation Router and Invoke.
- **New daemon or service**: creates lifecycle, security, and state surface with no
  demonstrated need.
