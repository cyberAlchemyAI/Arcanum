# Craft Interaction Design

Status: refined-design
Date: 2026-06-07
Owner surface: `development/craft/`

## Purpose

Design how Craft and its local interface interact with Arcanum sigils and spells
without absorbing their authority. Craft owns the recursive making ledger and
route memory. The called capability owns its native lifecycle, artifact contract,
validation, and result evidence.

This design extends `CRAFT-INTERFACE-REFINE.md`; it does not replace the first
interface slice.

## Core Boundary

Craft is a context operating surface:

- it starts and maintains `.craft/ledger.yml`;
- it records intent, state, blockers, enablers, decisions, gaps, definitions,
  next moves, handoffs, receipts, residue, and recomposition;
- it routes work to the right owner capability when Craft itself should not act;
- it receives evidence back and updates the parent or child Craft context.

Craft is not:

- a replacement for `refine`;
- a replacement for `invoke`;
- a replacement for `decision-gate`;
- a replacement for `task-session`;
- a replacement for `dispatch-spec`;
- a command surface or runtime adapter.

## Interaction Model

Every external capability interaction has the same shape:

1. Craft detects a condition in the ledger.
2. Craft classifies the route owner.
3. Craft writes a route handoff row.
4. The owner capability runs or produces its own artifact.
5. Craft receives a receipt.
6. Craft validates whether the receipt satisfies the ledger condition.
7. Craft recomposes the result into the parent context or opens residue.

```text
Craft context state
  -> route classification
  -> handoff contract
  -> owner capability
  -> receipt/evidence
  -> ledger update
  -> recomposition or residue
```

## Interface Additions

The basic Craft interface needs these route methods:

### classify_route

Selects the owner capability for a ledger condition.

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

### prepare_handoff

Creates a durable route handoff before an external capability runs.

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

- route handoff row;
- relation from context to handoff artifact;
- current next move.

### receive_receipt

Records capability-owned output evidence.

Inputs:

- `handoff_id`
- `capability_ref`
- `status`
- `artifacts`
- `validation_result`
- `residue`
- `audit_reference`

Writes:

- receipt row;
- artifact rows;
- relation rows from receipt to affected blockers, decisions, gaps, or child
  contexts.

### apply_receipt

Updates Craft state from a valid receipt.

Inputs:

- `receipt_id`
- `application_policy`

Writes:

- blocker, enabler, decision, gap, definition, or next-move updates;
- recomposition evidence when a child context is satisfied.

Invariant:

- Craft may record that a capability passed, flagged, or blocked. It may not
  rewrite the capability's native verdict.

### open_residue

Turns incomplete or failed capability results into explicit Craft residue.

Inputs:

- `receipt_id`
- `residue_type`
- `summary`
- `route_recommendation`

Writes:

- gap or blocker row;
- optional child context;
- next move.

## Capability Contracts

### refine

Use when:

- the Craft context is vague, brittle, recursive, or not execution-ready;
- route ownership is unclear;
- a design concern needs critique, repair, and a non-executed plan.

Craft sends:

- target context;
- current ledger state;
- source artifacts;
- unresolved blockers, gaps, decisions, definitions;
- desired outcome;
- research mode;
- stop conditions.

Refine returns:

- run manifest;
- evidence index;
- seed proposal;
- validated dispatch route;
- stage artifacts or blocked reasons;
- final synthesis;
- recommended next routes.

Craft records:

- child context for the refinement run when the run is substantial;
- receipt linked to the original context;
- refined blockers/gaps/definitions;
- next route from the final synthesis.

Craft must not:

- skip Refine's strategy preview;
- treat a Refine plan as executed work;
- absorb Refine's ten-stage lifecycle into Craft.

### decision-gate

Use when:

- a blocker-level multi-option decision affects scope, implementation, rollout,
  policy, cost, risk, validation, or promotion.

Craft sends:

- decision question;
- options;
- trade-offs;
- source evidence;
- downstream impact;
- current blocked condition.

Decision Gate returns:

- `PASS` or `BLOCK`;
- selected option or unresolved blocker;
- rationale;
- decision artifact path;
- deferred decisions and assumptions.

Craft records:

- decision row status;
- selected option and rationale;
- blocker resolution or continued block;
- updated next move.

Craft must not:

- auto-select consequential decisions;
- hide an unresolved decision as a normal gap;
- proceed after a `BLOCK` result unless the user explicitly overrides.

### invoke

Use when:

- Craft needs authored define, design, plan, handoff, or refresh artifacts;
- raw intent needs a governed artifact baseline before execution;
- an approved design needs a work-pack.

Craft sends:

- target artifact owner;
- mode: `define`, `design`, `plan`, `handoff`, or `refresh`;
- source contracts;
- vocabulary boundaries;
- unresolved gaps;
- expected handoff path;
- next-route expectation.

Invoke returns:

- authored artifact paths;
- mode status;
- unresolved gaps;
- implementation layering when applicable;
- work-pack when in plan mode;
- recommended next route.

Craft records:

- authored artifacts as ledger artifacts;
- source contract relations;
- gaps that belong to the target artifact;
- next move, usually `task-session` for an approved work-pack.

Craft must not:

- treat Invoke authoring as lifecycle completion;
- execute work-pack tasks during Invoke planning;
- mutate upstream canonical surfaces without approval.

### task-session

Use when:

- exactly one work-pack task or SWU is ready to execute;
- inputs, outputs, write scope, validation, and recomposition path are explicit.

Craft sends:

- selected task or SWU;
- context pack obligations;
- write scope;
- blockers and decisions already resolved;
- acceptance criteria;
- validation commands;
- expected receipt fields.

Task Session returns:

- task result: `PASS`, `FLAG`, or `BLOCK`;
- context pack summary;
- decisions;
- files updated;
- validation result;
- residue;
- synchronized records.

Craft records:

- execution receipt;
- artifact rows for changed files;
- validation evidence;
- residue as gaps/blockers/child contexts;
- recomposition into the parent context when evidence supports closure.

Craft must not:

- send multiple unrelated tasks as one task-session;
- mark Craft context closed just because files changed;
- ignore Task Session `BLOCK` or `FLAG` residue.

### dispatch-spec

Use when:

- a Craft route needs a validator-backed composition over capabilities;
- handoffs, gates, technique overlays, subagents, receipts, or boundary evidence
  must be explicit before execution.

Craft sends:

- route intent;
- steps;
- capability references;
- gates;
- handoffs;
- observability events;
- boundary evidence;
- subagent strategy when relevant.

Dispatch Spec returns:

- route validation: `pass`, `flag`, or `block`;
- missing or invalid fields;
- subagent strategy status;
- promotion guardrail status.

Craft records:

- dispatch artifact as route evidence;
- validation verdict;
- blocked fields as gaps or blockers;
- next move to repair route or proceed to owner execution.

Craft must not:

- use Dispatch Spec to decide domain content;
- execute a route just because the route shape validates;
- claim promotion authority from dispatch validation.

## Route Classification Table

| Craft Condition | Route | Handoff Artifact | Receipt Expected | Ledger Effect |
| --- | --- | --- | --- | --- |
| vague intent | `invoke define` or `refine` | define/refine request | authored define artifact or refine synthesis | description, definitions, gaps, next move |
| brittle design | `refine` | refine seed and dispatch | refine result, stage evidence | refined context, child context, route recommendation |
| missing architecture or plan | `invoke design` or `invoke plan` | mode request | design/plan/work-pack artifacts | artifact rows, source contracts, next route |
| unresolved consequential decision | `decision-gate` | decision options | decision record | decision closed or context blocked |
| route shape uncertainty | `dispatch-spec` | dispatch JSON | validation result | route pass/flag/block, repair gaps |
| one executable task | `task-session` | task reference/context pack | task-session report | artifacts, validation, residue, recomposition |
| failed or partial execution | `refine`, `decision-gate`, or child context | residue handoff | repair plan or decision | new gap/blocker/child next move |

## Ledger Row Additions

The interaction layer needs three candidate row families in addition to the base
interface rows.

### route_handoffs

Required fields:

- `handoff_id`
- `context_id`
- `capability_ref`
- `mode`
- `objective`
- `source_artifacts`
- `ledger_conditions`
- `expected_outputs`
- `expected_receipt_fields`
- `status`

### receipts

Required fields:

- `receipt_id`
- `handoff_id`
- `producer`
- `status`
- `artifacts`
- `validation_result`
- `audit_reference`
- `residue`

### route_events

Required fields:

- `event_id`
- `context_id`
- `event_type`
- `capability_ref`
- `summary`
- `evidence`

Recommended event types:

- `route_classified`
- `handoff_created`
- `receipt_received`
- `receipt_applied`
- `residue_opened`
- `recomposition_completed`

## Decision Gate Result

Target scope: Craft interaction design.

Result: PASS.

Decisions resolved:

- Craft remains ledger/router, not owner of the called sigil or spell lifecycle.
- Capability receipts are recorded in Craft but native verdicts remain owned by
  the producing capability.
- The interaction layer adds `route_handoffs`, `receipts`, and `route_events`.

Blockers remaining: none for local design.

Deferred decisions:

- whether route handoffs become a helper library, CLI, or skill-native helper;
- whether receipt validation becomes executable;
- whether Craft can later run selected routes directly through a runtime owner.

## Validation Rules

- A handoff must name one owner capability.
- A receipt must reference one handoff.
- A blocked receipt cannot close a context.
- A `dispatch-spec` pass validates route shape only, not content completion.
- An `invoke plan` work-pack is not execution evidence.
- A `task-session` pass can close an execution child context only after Craft
  recomposition evidence is recorded.
- A `decision-gate` block keeps the linked Craft context blocked.
- Candidate definitions remain local unless an owning governance route promotes
  them.

## Next Build Slice

After `CRAFT-INTERFACE-001`, add a second bounded task:

`CRAFT-INTERACTION-001`: implement the interaction contract artifacts and a
fixture showing Craft routing one context through `invoke plan`,
`dispatch-spec`, `task-session`, and `decision-gate` without claiming their
authority.
