# Task Session Until Blocker

`task-session-until-blocker` is a reusable Arcanum spell for executing a
captured, ordered work-pack frontier as a series of distinct Task Sessions. It
continues only across uniquely declared, dependency-ready successors and stops
at the first genuine blocker or when the captured frontier is complete.

The spell does not widen Task Session. Each Task Session still owns exactly one
task or SWU, one validation result, one lifecycle-owner closeout join, one
continuity cursor, and one terminal receipt.

## Status

- type: reusable spell
- canonical id: `task-session-until-blocker`
- aliases: `task-session-chain`, `all-swus-until-blocker`
- lifecycle owner: Spellcraft
- execution unit owner: Task Session
- loop style: bounded serial orchestration

## Use When

- the user explicitly asks for all ready SWUs, one go, or execution until a
  blocker;
- the target is one ordered work pack with declared dependencies;
- every candidate unit can be executed through a fresh Task Session;
- stopping at the first failed gate is more important than speculative
  throughput.

## Do Not Use When

- the work spans unrelated work packs or independent branches;
- the frontier is not ordered or successor selection is ambiguous;
- the request is for planning, discovery, promotion, publication, deployment,
  or destructive cleanup;
- one Task Session is sufficient;
- continuation would require expanding the captured frontier.

## Required Capabilities

- `task-session`
- `continuation-router`
- `signal-observer`

Task Session remains responsible for its required
`invoke:refresh:apply-approved` closeout hop. The spell observes and joins the
result; it does not impersonate Invoke or mutate owner artifacts directly.

## Optional Capabilities

- `experiment-harness` for repeatable chain validation
- `decision-gate` for a blocker that exposes a real user choice
- `workflow-reflect` when accumulated observations justify maintenance

## Inputs

- one exact work-pack path or stable selector;
- optional first task or SWU selector;
- explicit stop condition, defaulting to `first-blocker-or-frontier-complete`;
- optional maximum session count, bounded by the captured frontier length;
- runtime selection accepted by Task Session;
- any approval boundary required by the work-pack or runtime.

## Preconditions

Before the first implementation mutation, the spell must prove:

1. one exact work-pack scope is bound;
2. the initial incomplete frontier is finite, ordered, and dependency-aware;
3. each candidate has declared write scope and validation obligations;
4. each candidate has a Task Session closeout contract with terminal receipt
   shape, target inventory, baselines, allowed delta classes, owner validation,
   expected owner receipt, and successor policy;
5. the first candidate is uniquely ready;
6. the maximum session count is no greater than the captured frontier length.

Missing or contradictory evidence returns `BLOCK` before code mutation.

## Shared Chain State

Persist one chain record containing:

- chain id and work-pack identity;
- captured frontier with stable task or SWU ids;
- current expected selector;
- visited selectors;
- joined Task Session receipt paths;
- joined closeout owner receipt paths or validated no-op evidence;
- continuity cursor fingerprints;
- stop reason and final next route.

This state coordinates the series. It does not collapse the inner receipts into
one synthetic Task Session receipt.

### Approved-epoch candidate runtime

The additive candidate runner at
[`scripts/run_chain.py`](scripts/run_chain.py) consumes:

- [`chain-config.schema.json`](schemas/chain-config.schema.json), binding the
  exact WPRA manifest, human/Decision Gate approval receipt, epoch digests,
  finite frontier, risk ceiling, request budget, flag allowlist, persistence,
  and compensation policy;
- [`chain-transition.schema.json`](schemas/chain-transition.schema.json), one
  hash-linked transition for one fresh Task Session;
- [`closeout-no-op-proof.schema.json`](schemas/closeout-no-op-proof.schema.json),
  an exact before/after inventory proof with validator identity and
  Continuation Router verification.

The runtime stores one immutable `chain.json` and exclusively creates numbered
transition records. It replays the hash chain on every invocation. A
preflight or transition receipt exposes either one exact next selector or none;
it never launches Task Session itself. Repeated cursors, epoch/frontier drift,
out-of-order or ambiguous successors, risk or budget overflow, missing joins,
and invalid `NO_OP` proofs stop fail-closed.

`NO_OP` is semantic, not a boolean: before and after inventories must match,
the observed delta must be empty, the closeout contract must be the approved
one, and validator identity plus Router verification must be bound.
Compensation is never automatic. A `none` policy requires rationale; an
`owner-routed` policy stops and returns the named owner.

This candidate proves finite-frontier control only. Task Session continues to
own each implementation, Invoke Refresh owns closeout mutation, and the
approved manifest remains authority-none evidence.

### Work-Pack prerequisite resumption

The additive fresh-session admission at
[`scripts/fresh_session_resume.py`](scripts/fresh_session_resume.py) handles the
one detour that is intentionally not a terminal Task Session transition. It
joins one exact Work-Pack-bound Router admission and one byte-current passing
prerequisite-owner receipt, then validates a new fast-entry classification.
Only `task-ready` evidence may produce a durable admission for a new Task
Session using the original selected unit and captured frontier.

The prerequisite detour does not consume the unit's one terminal Task Session
receipt slot or the logical finite-frontier request budget. The emitted fresh
admission is stored by exclusive create in a separate evidence ledger. A
replayed owner fingerprint, unchanged prerequisite, repeated session cursor,
changed frontier or budget, stale or mismatched receipt, or reused terminal
receipt slot blocks without launching Task Session. The controller consumes
the returned `task-session:execute` admission; this spell never launches a
process itself and never recursively resumes the guarding session.

## Phases

### 1. Bind And Capture

Resolve the exact work pack, capture its current ordered incomplete frontier,
record its identity and baselines, and set the session budget to the smaller of
the requested maximum and captured frontier length.

### 2. Preflight The Frontier

Validate each candidate’s declared dependencies, write scope, validation
surface, and closeout contract. Do not assume later Invoke refresh can infer
missing inventory, baselines, or receipt destinations.

### 3. Run One Fresh Task Session

Invoke Task Session for the current expected selector. Never ask Task Session
to execute more than one unit. Preserve its execution result, validation
evidence, closeout result, owner receipt or no-op proof, and continuity cursor.

### 4. Admit Or Stop

Continue only when all of the following are true:

- execution result is `PASS` or `FLAG`;
- required closeout is `PASS` or validated `NO_OP`;
- the lifecycle-owner receipt is joined when synchronization occurred;
- the continuity cursor is present and has not appeared earlier in the chain;
- Task Session returned one unique, declared, dependency-ready successor;
- the successor is the next unvisited member of the captured frontier;
- the successor remains in the same work-pack scope.

Any failed condition returns `BLOCK` with the preserved inner receipts.

### 5. Advance

Set the returned successor as the next selector and invoke a new Task Session.
Do not recursively resume the previous Task Session and do not use conversational
context as the only continuation state.

### 6. Close The Chain

Return `COMPLETE` when every captured unit is visited and the final Task Session
returns no successor. Otherwise return `BLOCK` with the first failed gate, the
last completed selector, the unvisited captured frontier, and the smallest
unblock action.

## Stop Conditions

Stop immediately on:

- any Task Session `BLOCK`;
- failed or unavailable acceptance-critical validation;
- closeout failure, missing owner join, or invalid no-op proof;
- ambiguous, missing, repeated, out-of-order, or cross-scope successor;
- repeated selector or continuity cursor;
- successor outside the captured frontier;
- live frontier expansion that would widen the session budget;
- approval, authority, policy, cost/risk, destructive, publication, deployment,
  or promotion boundary;
- exhausted session budget.

Newly discovered work remains for a later spell invocation. It never joins the
active frontier automatically.

## Authority Boundaries

- Work-pack authority remains with the work-pack lifecycle owner.
- Implementation authority remains with each selected Task Session.
- Closeout mutation authority remains with Invoke Refresh.
- Continuation Router owns normalized owner dispatch and receipt joining.
- This spell owns only bounded sequence state and stop decisions.
- A returned route is not authorization to execute outside the captured
  frontier.

## Observability

Emit one invocation envelope for the spell and preserve links to every inner
Task Session envelope. Record:

- trigger and target selector;
- captured frontier and budget;
- ordered selectors actually invoked;
- execution and closeout outcome for each selector;
- owner receipt or no-op evidence for each selector;
- cursor fingerprints;
- final stop reason and next route.

Use Signal Observer after the chain terminates. Observability is evidence, not
authority.

## Experiment Harness

The repository-local development harness must cover at least:

- a linear frontier completing in order;
- a blocker in a later Task Session;
- a closeout failure after passing implementation;
- a repeated cursor;
- a cross-scope successor;
- a successor outside the captured frontier;
- an ambiguous successor;
- a validated no-op closeout.

Harness results prove deterministic control-flow behavior only. They do not
prove a consuming project’s implementation is correct.

## Output Contract

Return:

- result: `COMPLETE | BLOCK`;
- chain id and exact work-pack scope;
- captured frontier and session budget;
- ordered selectors invoked;
- per-selector Task Session receipt;
- per-selector closeout owner receipt or no-op evidence;
- final continuity cursor;
- stop reason;
- remaining captured frontier;
- next route, if any;
- observability receipt.

## Quality Bar

- one fresh Task Session per unit;
- no recursive Task Session continuation;
- no mutation before closeout preflight passes;
- no continuation without joined inner receipts;
- no fresh-session admission without exact Router, owner, and reclassification evidence;
- one exclusive fresh-session admission per prerequisite fingerprint;
- no cross-scope or frontier-expanding continuation;
- deterministic stop at the first failed gate;
- public, project-agnostic contract and fixtures.

## Anti-Patterns

- changing Task Session’s execution limit from one;
- treating a chain receipt as proof that every inner validation passed;
- continuing after implementation passes but closeout blocks;
- selecting a successor from conversation alone;
- recomputing the frontier to absorb new work;
- routing around Invoke Refresh because the target is not yet released;
- describing `FLAG` as equivalent to `PASS`;
- hiding the first blocker to maximize the number of executed units.
