# Define: Deterministic Task Session Governance Runner

Status: proposed for Sigil Development review  
Target: update the existing `task-session` sigil  
Feature code: `TSGR`

## Problem

Task Session has mature governance rules, deterministic point tools, and green
fixture suites, but an agent still has to manually interpret and order many steps.
That increases latency and invites drift between the prose contract, the
machine-readable policy, and the evidence actually handed to closeout owners.

The missing product is not another reasoning authority. It is a deterministic,
checkpointed runner that makes the existing governance path cheap to invoke,
observable, resumable, and fail-closed.

## Desired outcome

An operator invokes one Task Session governance command for one exact SWU. The
runner:

1. resolves or validates the exact work-pack and SWU;
2. evaluates governance policy and mutation admission;
3. emits an immutable execution ticket;
4. accepts a separately produced executor receipt;
5. reconciles declared writes, outputs, and validations;
6. invokes only registered owner hooks for closeout;
7. joins owner receipts and emits a continuity cursor;
8. records an observation event.

The runner never chooses or executes the successor SWU.

## Actors

- **Operator**: starts or resumes one bounded run and reads the terminal summary.
- **Task Session runner**: orders deterministic governance phases and writes its
  own run evidence.
- **Implementation executor**: performs the selected SWU outside the runner's
  governance authority and returns a structured receipt.
- **Continuation Router**: owns continuation routing.
- **Invoke Refresh owner**: owns approved planning-artifact synchronization.
- **Signal Observer**: owns append-only observation ingestion.
- **Sigil Development reviewer**: accepts, narrows, or rejects the lifecycle change.

## Functional requirements

### TSGR-FR-001 — one-SWU scope

The runner must accept exactly one work-pack/SWU pair or resolve one unique nearest
pair through the existing resolver. Resolution never proves readiness.

### TSGR-FR-002 — production policy evaluator

The existing pure decision, validation, closeout-preflight, and closeout-sync
evaluators must be extracted behind a public production CLI with request and receipt
schemas. Its results must remain in golden parity with the development fixture corpus.

### TSGR-FR-003 — checkpointed phases

The controller must use monotonic phases:

```text
resolved -> governed -> admitted -> ticketed
         -> execution-received -> reconciled
         -> closeout-joined -> observed -> terminal
```

Unknown, skipped, stale, or contradictory transitions block. A restart resumes from
the last validated checkpoint.

### TSGR-FR-004 — structured execution boundary

The runner must not execute arbitrary shell text. An execution request uses a
structured argument vector, exact working directory, timeout, declared write/output
inventory, and expected receipt schema. The executor remains a separate role.

### TSGR-FR-005 — target classification

Before any staged output can be applied, every target is classified as exactly one
of:

- `apply`: live bytes equal the ticket baseline;
- `already-present-exact-output`: live bytes equal the staged output;
- `conflict`: neither condition holds.

Any conflict blocks. The second state is the only idempotent adoption path.

### TSGR-FR-006 — reconciliation

After execution, the runner must verify:

- only declared implementation paths changed;
- every declared execution output exists;
- undeclared outputs are absent;
- critical validations passed or an accepted equivalent is explicitly bound;
- the terminal executor receipt is the final executor write;
- output-only re-admission succeeds when later governance output is allowed.

### TSGR-FR-007 — owner hooks

Prepare and closeout side jobs use a generic hook request/receipt protocol. The
runner orders, invokes, and joins the hook but does not reproduce the hook owner's
semantics. An Invoke continuation hook must carry
`mutationMode=apply-approved`; omitted delegated mutation mode is proposal-only.

### TSGR-FR-008 — terminal evidence

Every phase receipt binds the run ID, SWU identity, prior receipt digest, input
digests, result, output refs, and idempotency key. The terminal receipt is written
last using atomic replacement.

### TSGR-FR-009 — observability

The final phase invokes the official observer with bounded refs and digests. A
repeated idempotency key must deduplicate rather than append a contradictory event.

### TSGR-FR-010 — public boundary

Canonical runner code, schemas, documentation, and fixtures must remain
product-neutral. Consumer content stays behind references and digests in
consumer-local evidence.

## Non-functional requirements

- **Determinism**: identical inputs and baselines produce byte-identical decision
  and phase result payloads, excluding explicitly named timestamps.
- **Fail closed**: missing schema, ambiguous successor, stale digest, unjoined owner
  receipt, validation failure, undeclared write, and hook timeout block.
- **Crash safety**: phase evidence is append-only or atomically replaced; partial
  terminal state is never accepted.
- **Bounded output**: captured stdout/stderr has an explicit byte ceiling and
  truncation receipt to reduce private-context leakage.
- **Compatibility**: existing Task Session invocation remains valid while the runner
  is introduced as an optional deterministic path, then becomes the recommended
  governance path only after experiment evidence.
- **Speed claim**: “faster” remains a hypothesis until paired runs measure
  governance latency and agent-intervention count without weaker acceptance.

## Acceptance witnesses

| Witness | Contract |
| --- | --- |
| TSGR-FIX-001 | production evaluator matches all current policy fixtures |
| TSGR-FIX-002 | identical prepare inputs yield identical ticket material |
| TSGR-FIX-003 | ambiguous or missing SWU blocks before any write |
| TSGR-FIX-004 | `apply`, `already-present-exact-output`, and `conflict` classify exactly |
| TSGR-FIX-005 | undeclared write/output and missing declared output block |
| TSGR-FIX-006 | terminal executor receipt must be the executor's final write |
| TSGR-FIX-007 | crash/restart at every phase resumes without duplicate effects |
| TSGR-FIX-008 | closeout pass, no-op, block, and unjoined owner receipt discriminate |
| TSGR-FIX-009 | unique successor yields a cursor; ambiguous successor blocks |
| TSGR-FIX-010 | repeated observer idempotency key deduplicates |
| TSGR-FIX-011 | product-neutral leak scan passes |
| TSGR-EXP-001 | paired manual/runner experiment measures time and interventions |

## Decisions

| Decision | Outcome |
| --- | --- |
| New sigil or update? | update existing `task-session`; the runner is an implementation detail |
| Daemon or bounded CLI? | bounded CLI |
| First trust step? | read-only production policy evaluator with fixture parity |
| Owner logic? | retained by Continuation Router, Invoke, and Signal Observer |
| Next-SWU execution? | forbidden |
| Shell interface? | structured argv only; no shell interpolation |
| First rollout? | opt-in experiment before recommended-path promotion |

## Blockers and residue

- `TSGR-RISK-001`: current Task Session files are dirty. Every implementation SWU
  must bind the live preflight digest and preserve unrelated pending edits.
- `TSGR-RISK-002`: stale architecture prose assigns synchronization directly to
  Task Session. The lifecycle update must repair it after the runtime contract is
  accepted.
- `TSGR-RISK-003`: “faster” is not yet proven. Promotion requires paired experiment
  evidence; no numeric threshold is claimed here.

## Authority ceiling

This Define package may authorize Design and Plan. It does not authorize canonical
implementation, approval, generated-mirror replacement, publication, or promotion.

