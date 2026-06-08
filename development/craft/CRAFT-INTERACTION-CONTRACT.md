# Craft Interaction Contract

Status: candidate-local
Date: 2026-06-08
Task: `CRAFT-INTERACTION-001`

## Purpose

Define how Craft routes work to owner capabilities, records handoffs, receives
receipts, applies evidence, and opens residue without replacing the called sigil
or spell lifecycle.

Craft owns route memory and recursive ledger state. The called capability owns
its native artifact contract, validation, and verdict.

## Interaction Methods

### classify_route

Inputs:

- `context_id`
- `condition_id` or `next_move`
- `candidate_routes`
- `evidence`

Returns:

- selected `capability_ref`;
- route reason;
- required handoff fields;
- expected receipt fields;
- blocking status.

Writes:

- route event with `event_type: route_classified`.

Invariant:

- route classification does not execute work or decide domain content.

### prepare_handoff

Inputs:

- `context_id`
- `capability_ref`
- `mode`
- `objective`
- `source_artifacts`
- `ledger_conditions`
- `expected_outputs`
- `expected_receipt_fields`

Writes:

- `route_handoffs` row;
- route event with `event_type: handoff_created`;
- relation from context to handoff artifact when applicable.

Returns:

- handoff id.

Invariant:

- each handoff names exactly one owner capability.

### receive_receipt

Inputs:

- `handoff_id`
- `capability_ref`
- `status`
- `artifacts`
- `validation_result`
- `residue`
- `audit_reference`

Writes:

- `receipts` row;
- route event with `event_type: receipt_received`;
- artifact rows or relations for produced evidence.

Returns:

- receipt id.

Invariant:

- Craft records the native verdict but does not rewrite it.

### apply_receipt

Inputs:

- `receipt_id`
- `application_policy`

Writes:

- route event with `event_type: receipt_applied`;
- condition, decision, gap, or next-move updates when allowed;
- recomposition evidence when receipt closes child work.

Returns:

- application result: `pass`, `flag`, or `block`.

Invariants:

- blocked receipts cannot close contexts;
- task-session pass closes execution work only after Craft recomposition
  evidence is recorded;
- dispatch-spec pass is route-shape evidence only.

### open_residue

Inputs:

- `receipt_id`
- `residue_type`
- `summary`
- `route_recommendation`

Writes:

- gap or blocker row;
- optional child context;
- route event with `event_type: residue_opened`;
- next move.

Returns:

- residue id or opened condition id.

Invariant:

- residue stays visible until closed, waived, deferred, or routed.

## Capability Contracts

### refine

Craft sends:

- target context;
- ledger state;
- source artifacts;
- unresolved blockers, gaps, decisions, and definitions;
- desired outcome;
- research mode;
- stop conditions.

Craft expects:

- run manifest;
- evidence index;
- seed proposal;
- validated dispatch route;
- stage evidence or blocked reasons;
- final synthesis;
- recommended next routes.

Craft records:

- refine receipt;
- child context when substantial;
- refined blockers or gaps;
- next route.

Boundary:

- Craft must not skip Refine strategy preview or treat a Refine plan as executed
  work.

### decision-gate

Craft sends:

- blocker-level question;
- concrete options;
- trade-offs;
- source evidence;
- downstream impact;
- linked blocked condition.

Craft expects:

- `PASS` or `BLOCK`;
- selected option or unresolved blocker;
- rationale;
- decision artifact path;
- deferred decisions and assumptions.

Craft records:

- decision row update;
- blocker resolution or continued block;
- next move.

Boundary:

- Craft must not auto-select consequential decisions.

### invoke

Craft sends:

- target artifact owner;
- mode: `define`, `design`, `plan`, `handoff`, or `refresh`;
- source contracts;
- vocabulary boundaries;
- unresolved gaps;
- expected handoff path;
- next-route expectation.

Craft expects:

- authored artifact paths;
- mode status;
- unresolved gaps;
- implementation layering when applicable;
- work-pack when in plan mode;
- recommended next route.

Craft records:

- authored artifacts;
- source contract relations;
- target-artifact gaps;
- next route.

Boundary:

- Invoke authoring is not execution evidence.

### task-session

Craft sends:

- one selected task or SWU;
- context pack obligations;
- write scope;
- resolved blockers and decisions;
- acceptance criteria;
- validation commands;
- expected receipt fields.

Craft expects:

- task result: `PASS`, `FLAG`, or `BLOCK`;
- context pack summary;
- decisions;
- files updated;
- validation result;
- residue;
- synchronized records.

Craft records:

- execution receipt;
- artifact rows;
- validation evidence;
- residue;
- recomposition evidence.

Boundary:

- changed files alone do not close a Craft context.

### dispatch-spec

Craft sends:

- route intent;
- steps;
- capability references;
- gates;
- handoffs;
- observability events;
- boundary evidence;
- subagent strategy when relevant.

Craft expects:

- route validation: `pass`, `flag`, or `block`;
- missing or invalid fields;
- subagent strategy status;
- promotion guardrail status.

Craft records:

- dispatch artifact;
- validation verdict;
- blocked fields as gaps or blockers;
- next move to repair or proceed.

Boundary:

- dispatch validation proves route shape, not execution.

## Closure Rule

An external capability result can affect Craft state only through a receipt.
A Craft context can close only when:

- the receipt status allows closure;
- required validation evidence exists;
- residue is classified;
- recomposition evidence connects child work to parent context.
