---
metadata:
  surface_kind: generated-native-runtime-package
  runtime: codex
  canonical_source: runtime/orchestrate/SKILL.md
  alias_of: null
  generated_by: tools/bootstrap_arcanum.sh --profile
  mutation_policy: regenerate-from-canonical-source
name: orchestrate
description: Route repository work through installed Arcanum capabilities and execute validated capability-bound dispatches through host-native operations.
argument_hint: execute <dispatch.json>
execute_contract:
  grammar: orchestrate execute <dispatch.json>
  verb: execute
  argument_count: 1
  argument_kind: dispatch-json-path
  validation_owner: dispatch-spec
  required_validation_result: pass
  authorization_satisfied:
  - approved
  - not_needed
  host_profile: hosts/codex-native.md
  ready_state: wave_ready
  preflight_spawn_attempt_count: 0
  strategy_registration_required: true
  strategy_registration_schema: arcanum.subagent-strategy-registration.v0.3
  strategy_ledger: .arcanum/observability/subagents-strategy/subagents-dispatch.yaml
  missing_host_behavior: block
  nested_model_cli_fallback: forbidden
native_spawn_contract:
  input_schema: schemas/action.schema.json
  action: spawn
  persisted_action_required: true
  operation_from_host_profile: spawn
  pre_event: action_attempted
  success_event: host_spawn_returned
  failure_event: host_spawn_failed
  calls_per_action: 1
  unknown_action_policy: block
  replay_policy: block
  returned_binding:
  - action_id
  - agent_id
  driver: scripts/native_dispatch_driver.py
native_join_contract:
  input_receipt_schema: schemas/receipt.schema.json
  join_policy: all
  wait_operation_from_host_profile: wait
  inventory_operation_from_host_profile: inventory
  recovery_operation_from_host_profile: interrupt
  registration_event: agent_wait_registered
  wait_event: wait_attempted
  terminal_event: agent_terminal
  close_event: agent_closed
  timeout_event: wait_timed_out
  interrupt_event: agent_interrupted
  registration_per_agent: 1
  close_per_agent: 1
  missing_result_status: timed_out
  identity_mismatch_status: block
  reducer: scripts/native_dispatch_coordinator.py
  driver: scripts/native_dispatch_driver.py
  receipt_admission_schema: schemas/receipt-admission.schema.yml
  receipt_join_event: receipt_joined
  gate_event: gate_decided
native_evidence_contract:
  causal_schema: schemas/run-event.schema.json
  residue_schema: schemas/run-residue.schema.yml
  append_owner: scripts/native_dispatch_driver.py
  source_time_append_required: true
  prefix_validation_required: true
  complete_validation_before_resolved_close: true
  pure_reduce_live_evidence: false
---

# Skill: Arcanum Orchestrate

<objective>
Route work through installed Arcanum capabilities and provide the parent-owned native execution surface for already-valid capability-bound dispatches.
</objective>

<authority>
- Dispatch Spec validates dispatch structure, route rules, and techniques.
- Orchestrate owns execution preflight, native action scheduling, joins, gates, and run closeout.
- A delegated capability owns only its bounded work and returned receipt.
- Humans and capability owners retain lifecycle and promotion authority.
</authority>

<commands>

## `orchestrate execute <dispatch.json>`

Accept exactly one repository-local dispatch JSON path. Extra positional arguments, a missing path, or another verb return a blocked preflight receipt and perform no host action.

Native execution after preflight uses
`scripts/native_dispatch_driver.py`. Its `prepare-spawn` and `prepare-wait`
commands append the required pre-call events before making a host request
artifact available. `record-spawn` and `append-event` record host-owned results.
`advance-wave` admits the exact current-wave receipt set, appends receipt joins
and the reducer-owned gate decision, validates the causal stream, and only then
persists dependent actions. `prepare-next-wave-plan` binds those exact actions
to an exclusively created current-wave plan without changing the causal stream.
</commands>

<execute-preflight>
Run these checks in order:

1. Parse the exact execute grammar.
2. Run the canonical Dispatch Spec validator. Continue only when the result is `pass`; `flag` and `block` emit a blocked receipt.
3. Read `subagent_strategy.authorization`. Continue only for `approved` or `not_needed`. Use `authorization_pending` for `requires_user_permission`; use `blocked` for `blocked` or missing authorization.
4. Load the selected host profile and compare every `required_execute_operation` with the active host tool catalog. The active host catalog is runtime evidence; a shell executable or prose claim is not a substitute.
5. If any required operation is missing, emit `state=blocked`, name the missing operations, set `spawn_attempt_count=0`, and stop.
6. Ask the deterministic coordinator to verify `subagent_strategy.registration` against the canonical append-only strategy ledger. It must find exactly one dispatch row with the same `dispatch_id`, `sheet_schema_version`, `sheet_sha256`, and executable projection digest; recompute that projection from the current Dispatch Spec; compare registered agent names, exact initial prompts, group cardinality, and blocking dependencies to executable waves; and prove that the declared temporary sheet no longer exists. Missing, stale, mismatched, duplicate, or unconsumed registration blocks before actions are emitted.
7. Ask the deterministic coordinator to compile the first eligible wave. A passing preflight persists `strategy-registration.json` beside the state and run plan and ends at `state=wave_ready` with action documents and `spawn_attempt_count=0`.

Preflight never invokes `spawn`, `wait`, `join`, `close`, message delivery, or a model-backed CLI.
</execute-preflight>

<preflight-receipt>
Return a structured receipt containing:

- command, dispatch ID, and caller-supplied run ID;
- status and state;
- validation and authorization status;
- host ID, required/available/missing native operations;
- action count and whether a run plan was emitted;
- `spawn_attempt_count`, which must equal zero;
- blockers.
</preflight-receipt>

<native-execution-boundary>
Only a later native execution step may consume coordinator-emitted actions and call operations declared by the host profile. Never execute an action that lacks a persisted action document. Never use nested `codex exec`, another model-backed CLI, or silent local-inline model work when a required native operation is unavailable.

The deterministic coordinator's `reduce` command remains an offline reducer
and fixture surface. Its result alone is not live execution evidence and cannot
justify a resolved closeout. A live native path must use the driver handshake
and a validator-clean causal stream. If a pre-call append blocks, do not make
the host call. If a post-call append or terminal validation blocks, preserve
the partial stream and close with error; never reconstruct the missing event.
</native-execution-boundary>

<native-spawn-action>
Consume exactly one persisted action document whose `action` is `spawn` and whose complete shape validates against `schemas/action.schema.json`.

1. Admit the action only when its `action_id` exists in the current run plan, its persisted document matches that plan entry, and no attempt event already exists for the identifier.
2. Revalidate the action's canonical `briefing_binding` digest, exact
   read/write-policy equality, `agent_name`, and exact confirmed
   `initial_prompt`. Require the briefing identity and instructions to equal
   the prompt identity and body, then pass `initial_prompt` unchanged as the
   complete host message. Preserve task-completion status separately from
   domain-gate status. Never infer forbidden reads from forbidden-write scopes.
   The host task name must be an opaque deterministic function of dispatch ID,
   run ID, and action ID. It must differ across fresh runs and must not include
   raw role, target, reference, dispatch, or run prose.
3. Run driver `prepare-spawn`; it must block on missing, changed, or incomplete
   briefing material before appending `action_attempted`, then append that event
   before exposing the exact host request. If preparation blocks, do not invoke
   the host.
4. Invoke that operation exactly once. Do not retry implicitly.
5. On return, run driver `record-spawn --agent-id <id>` to append `host_spawn_returned` and bind the returned `agent_id` to the `action_id`. A missing agent identifier is a blocking host failure.
6. On host error, run driver `record-spawn --failed` to append `host_spawn_failed`, persist the failure in the non-causal residue stream when useful, and stop dependent execution.

An unknown, non-persisted, mismatched, duplicate, or replayed action blocks before a host call. Waiting, joining, result normalization, and gate reduction are separate execution steps.
</native-spawn-action>

<native-join-wave>
Consume one persisted wave plan and the complete action-to-native-agent bindings returned by prior spawn actions. The Codex wait operation is mailbox-wide, so do not model it as a targeted per-agent API.

1. Reject bindings that are absent, duplicated, outside the selected wave, or inconsistent with the persisted actions.
2. Run driver `prepare-wait`; it derives every successful native binding from the causal stream, appends one `agent_wait_registered` per expected action and `wait_attempted`, then exposes the mailbox-wide wait request.
3. Invoke the host's mailbox-wide wait operation, then reconcile returned completions and the host inventory against only the pending identifiers. Repeat only within the declared bounded wait policy, appending another `wait_attempted` before each call.
4. For a terminal known agent, validate its declared action and agent identities, normalize its bounded result to `schemas/receipt.schema.json`, append `agent_terminal`, and mark it logically closed exactly once with `agent_closed`.
5. For an unresolved known agent when the wait policy expires, append `wait_timed_out`, invoke the mapped interrupt operation once, append `agent_interrupted`, and normalize an explicit `timed_out` receipt for its expected action.
6. Persist normalized receipts in a directory containing exactly one `<action_id>.json` file per current-wave action and no other entries.
7. Persist exactly one raw task-result JSON object per current-wave action, then
   run driver `advance-wave` with that exact directory. It validates every
   briefing-required field and task-completion status before receipt admission,
   requires a blocked task result to normalize as `status=block`, validates
   closed receipt shape and identity, and only then appends `receipt_joined`,
   invokes the reducer, appends `gate_decided`, and exposes dependents. A failed
   task-result validation writes blocking evidence and emits no join or gate.
8. When a passing gate exposes dependents, run driver `prepare-next-wave-plan` with the exact dispatch, prior run plan, gate decision, next action set, next state, causal prefix, and action directory emitted by `advance-wave`. Continue only with its exclusively created current-wave plan.

An unknown result, duplicate terminal result, missing binding, identity mismatch, non-pass result, or missing result is blocking evidence. It cannot open a dependent gate. Multi-wave progression and closeout are separate execution steps.
</native-join-wave>

<strategy-registration-closeout>
After every spawned agent has a terminal close state, create the declared
`temporary_close` JSON under `.arcanum/runtime/subagents-strategy/`. Its total
and role tree must agree, its total must equal the registered strategy topology,
and its loop count cannot exceed `max_loops`. Append it
through the Subagent Strategy registrar with consumption enabled; never edit
the ledger directly. Then run coordinator `verify-close <dispatch.json>`.
Resolved closeout requires exactly one paired `close_of` row after the dispatch
row and absence of the temporary close JSON. A missing, duplicate, out-of-order,
or unconsumed close record blocks a resolved report.
</strategy-registration-closeout>

<native-next-wave-plan>
`prepare-next-wave-plan` is a deterministic, non-causal transition. It writes
no event and performs no host operation. It requires the validator-clean event
prefix to end at the exact passed source gate, rejects replayed or terminally
blocked runs, verifies route dependencies and run-global action allocation,
and admits an action directory only when it contains exactly the canonically
serialized action files named by the next action set. The output path is
exclusive; an existing output blocks before mutation.

Invoke it as `prepare-next-wave-plan <dispatch.json> --prior-run-plan <plan>
--gate-decision <gate> --next-actions <action-set> --next-state <state>
--events <events.jsonl> --actions-dir <actions> --output <next-plan>`.

Pass the emitted plan to `prepare-spawn` with the matching
`--depends-on-gate-id`. A dependent-wave spawn without one passed gate from its
declared dependency waves blocks before appending `action_attempted`.
</native-next-wave-plan>

<partial-wave-recovery>
When one or more selected-wave spawns produce `host_spawn_failed`, keep the
normal `prepare-wait` all-action rule unchanged. Do not synthesize a failed
action receipt and do not call `advance-wave`.

1. Stop every later spawn in that wave.
2. Run driver `prepare-partial-recovery`; it derives only successful native
   bindings, appends their registrations plus one mailbox-wide wait event, and
   exposes the exact host wait request.
3. Reconcile only those known identifiers with the host inventory. Record a
   completed sibling through `record-partial-terminal`; for an unresolved one,
   run `prepare-partial-interrupt`, invoke its exact interrupt request once,
   then record it with `record-partial-interrupt`.
4. Append separate `evidence_closure` residue for every cleaned sibling.
5. Run `close-partial-wave`. It requires all known siblings to be cleaned,
   appends a terminal typed `run_blocked`, validates the complete stream, and
   emits no joins, gates, dependent actions, or retry.

Partial-wave recovery is scoped to the selected failed wave. Earlier completed
waves retain their joins and gate decisions, while `run_blocked` remains unique
and globally terminal for the run.

The blocked closeout preserves the failed run as evidence only. A fresh run
requires a distinct run ID and explicit retry authority; it must not replay an
action in the closed stream.
</partial-wave-recovery>

<causal-event-and-residue-boundary>
`events.jsonl` contains only records admitted by
`schemas/run-event.schema.json` through the native driver. Feedback,
governance repair, commentary, evidence-closure notes, and reduction notes are
not causal events. When they need preservation, append them explicitly to a
separate `residue.jsonl` through driver `append-residue` and
`schemas/run-residue.schema.yml`.

Residue is read-only collaboration or diagnostic evidence. It cannot satisfy a
spawn, wait, terminal, join, gate, closeout, authority, or promotion
obligation. Historical mixed logs remain historical failure evidence and must
not be rewritten into a passing causal stream.
</causal-event-and-residue-boundary>

<failure-policy>
- Invalid dispatch: `block`, no plan, no actions, zero spawn attempts.
- Missing, mismatched, duplicate, or unconsumed strategy registration: `block`, no actions, zero spawn attempts.
- Authorization pending or blocked: `authorization_pending|blocked`, no actions, zero spawn attempts.
- Missing host operation: `block`, no native call, zero spawn attempts.
- Coordinator failure: preserve its blockers, zero spawn attempts.
- Ready: `pass`, `wave_ready`, compiled actions only; spawning is still not part of preflight.
- Unknown or replayed native action: `block`, no host call.
- Native spawn error or missing returned agent identifier: record the attempted call and blocking failure evidence; do not retry implicitly.
- Partial-wave spawn failure: clean only already-known siblings through the dedicated partial-recovery handshake, append a terminal `run_blocked` closeout, and expose zero dependent actions.
- Source-time event append failure: make no pending host call; preserve the existing stream byte-for-byte and block.
- Missing or mismatched joined result: normalize blocking evidence for the expected action and let the deterministic reducer withhold dependents.
- Unresolved known agent: interrupt once under the wave's incomplete policy, record residue, and return an explicit `timed_out` receipt.
- Receipt directory contamination, missing exact receipt, closed-schema violation, or identity mismatch: block before reduction and emit no dependent action.
- Invalid causal prefix or terminal stream: preserve raw evidence, emit no dependent action, and close with error; never derive or synthesize missing history.
- Missing paired strategy close row or an unconsumed close JSON: block resolved closeout.
</failure-policy>
