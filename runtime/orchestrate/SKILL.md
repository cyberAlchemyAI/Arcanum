---
name: orchestrate
description: "Route repository work through installed Arcanum capabilities and execute validated capability-bound dispatches through host-native operations."
surface_kind: canonical-native-runtime-package
runtime: native
canonical_source: runtime/orchestrate
mutation_policy: canonical-source
argument_hint: "execute <dispatch.json>"
execute_contract:
  grammar: "orchestrate execute <dispatch.json>"
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
</commands>

<execute-preflight>
Run these checks in order:

1. Parse the exact execute grammar.
2. Run the canonical Dispatch Spec validator. Continue only when the result is `pass`; `flag` and `block` emit a blocked receipt.
3. Read `subagent_strategy.authorization`. Continue only for `approved` or `not_needed`. Use `authorization_pending` for `requires_user_permission`; use `blocked` for `blocked` or missing authorization.
4. Load the selected host profile and compare every `required_execute_operation` with the active host tool catalog. The active host catalog is runtime evidence; a shell executable or prose claim is not a substitute.
5. If any required operation is missing, emit `state=blocked`, name the missing operations, set `spawn_attempt_count=0`, and stop.
6. Ask the deterministic coordinator to compile the first eligible wave. A passing preflight ends at `state=wave_ready` with action documents and `spawn_attempt_count=0`.

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
</native-execution-boundary>

<native-spawn-action>
Consume exactly one persisted action document whose `action` is `spawn` and whose complete shape validates against `schemas/action.schema.json`.

1. Admit the action only when its `action_id` exists in the current run plan, its persisted document matches that plan entry, and no attempt event already exists for the identifier.
2. Build bounded host context from only the action's role, capability, target, mode, mutation policy, write scope, forbidden scopes, input references, and output references.
3. Append `action_attempted` to the run event stream before invoking the host operation mapped from `spawn` by the selected host profile.
4. Invoke that operation exactly once. Do not retry implicitly.
5. On return, append `host_spawn_returned` and persist the returned `agent_id` with the `action_id`. A missing agent identifier is a blocking host failure.
6. On host error, append `host_spawn_failed`, persist a blocking native-spawn receipt, and stop dependent execution.

An unknown, non-persisted, mismatched, duplicate, or replayed action blocks before a host call. Waiting, joining, result normalization, and gate reduction are separate execution steps.
</native-spawn-action>

<native-join-wave>
Consume one persisted wave plan and the complete action-to-native-agent bindings returned by prior spawn actions. The Codex wait operation is mailbox-wide, so do not model it as a targeted per-agent API.

1. Reject bindings that are absent, duplicated, outside the selected wave, or inconsistent with the persisted actions.
2. Register every known native identifier exactly once in a pending set and append `agent_wait_registered` for each.
3. Append `wait_attempted`, invoke the host's mailbox-wide wait operation, then reconcile returned completions and the host inventory against only the pending identifiers. Repeat only within the declared bounded wait policy.
4. For a terminal known agent, validate its declared action and agent identities, normalize its bounded result to `schemas/receipt.schema.json`, append `agent_terminal`, and mark it logically closed exactly once with `agent_closed`.
5. For an unresolved known agent when the wait policy expires, append `wait_timed_out`, invoke the mapped interrupt operation once, append `agent_interrupted`, and normalize an explicit `timed_out` receipt for its expected action.
6. Give the deterministic reducer exactly one normalized receipt per expected action. Return its state, gate decision, and next action set without reinterpretation.

An unknown result, duplicate terminal result, missing binding, identity mismatch, non-pass result, or missing result is blocking evidence. It cannot open a dependent gate. Multi-wave progression and closeout are separate execution steps.
</native-join-wave>

<failure-policy>
- Invalid dispatch: `block`, no plan, no actions, zero spawn attempts.
- Authorization pending or blocked: `authorization_pending|blocked`, no actions, zero spawn attempts.
- Missing host operation: `block`, no native call, zero spawn attempts.
- Coordinator failure: preserve its blockers, zero spawn attempts.
- Ready: `pass`, `wave_ready`, compiled actions only; spawning is still not part of preflight.
- Unknown or replayed native action: `block`, no host call.
- Native spawn error or missing returned agent identifier: record the attempted call and blocking failure evidence; do not retry implicitly.
- Missing or mismatched joined result: normalize blocking evidence for the expected action and let the deterministic reducer withhold dependents.
- Unresolved known agent: interrupt once under the wave's incomplete policy, record residue, and return an explicit `timed_out` receipt.
</failure-policy>
