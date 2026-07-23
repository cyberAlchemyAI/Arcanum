---
host_id: codex
profile_version: arcanum.orchestrate.host-profile.v0.1
availability_authority: active-host-tool-catalog
native_operation_map:
  spawn: collaboration.spawn_agent
  wait: collaboration.wait_agent
  interrupt: collaboration.interrupt_agent
  inventory: collaboration.list_agents
  message: collaboration.send_message
required_execute_operations:
  - collaboration.spawn_agent
  - collaboration.wait_agent
  - collaboration.interrupt_agent
  - collaboration.list_agents
optional_execute_operations:
  - collaboration.send_message
missing_operation_behavior: block
nested_model_cli_fallback: forbidden
preflight_spawn_attempt_count: 0
spawn_contract:
  input_schema: ../schemas/action.schema.json
  operation: collaboration.spawn_agent
  fork_turns: none
  pre_event: action_attempted
  success_event: host_spawn_returned
  failure_event: host_spawn_failed
  replay_policy: block
  unknown_action_policy: block
  calls_per_action: 1
  required_request_fields:
    - task_name
    - message
    - fork_turns
join_contract:
  join_policy: all
  wait_operation: collaboration.wait_agent
  wait_targeting: mailbox-wide
  inventory_operation: collaboration.list_agents
  recovery_operation: collaboration.interrupt_agent
  pending_set_required: true
  registration_per_agent: 1
  terminal_close_per_agent: 1
  interrupt_per_unresolved_agent: 1
  missing_result_status: timed_out
  identity_mismatch_status: block
---

# Codex Native Host Profile

This profile maps Orchestrate actions to the Codex host's native collaboration operations. It is host-specific implementation material; Dispatch Spec remains runtime-neutral.

## Preflight

Compare `required_execute_operations` with operations currently exposed by the host. Do not infer availability from a shell binary, documentation, an earlier run, or an installed adapter profile.

Preflight records availability and returns. It must not call any mapped operation.

## Execution Boundary

- `spawn` creates exactly one native agent for one persisted coordinator action.
- `wait` joins known agent identifiers under the declared wave policy.
- `interrupt` closes known live agents during bounded recovery.
- `inventory` audits known live agents before closeout.
- `message` is optional and may only deliver bounded action context to an already-known agent.

If any required operation is absent, block. Do not invoke a nested model-backed CLI and do not synthesize a host receipt.

## Spawn Mapping

For one admitted `spawn` action, call `collaboration.spawn_agent` exactly once with:

- a stable `task_name` derived from the action role and action identifier;
- `fork_turns: none`, so the child receives only explicitly bounded action context;
- a `message` containing the action identifier, role, capability, target, mode, mutation policy, write scope, forbidden scopes, input references, output references, and required receipt shape.

Persist `action_attempted` before the call. On success, persist `host_spawn_returned` with the native `agent_id` bound to the action. On error or a missing identifier, persist `host_spawn_failed` and block without implicit retry. Waiting for the returned identifier belongs to the later join action, not spawn mapping.

## Join Mapping

`collaboration.wait_agent` waits for mailbox activity and does not accept a target identifier. Register each known wave agent once in a pending set, call the mailbox-wide wait operation in bounded rounds, and use `collaboration.list_agents` plus returned completion messages to reconcile only those known identifiers.

A completed known agent is logically closed once and needs no interrupt. An unresolved known agent is interrupted at most once through `collaboration.interrupt_agent`; its expected action receives an explicit `timed_out` receipt. Unknown or duplicated result identities are blocking evidence. The native driver passes the complete normalized receipt set to the deterministic reducer and never opens a gate itself.
