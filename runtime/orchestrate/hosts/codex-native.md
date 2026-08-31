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
  prepare_command: scripts/native_dispatch_driver.py prepare-spawn
  record_command: scripts/native_dispatch_driver.py record-spawn
  record_request_binding_required: true
  returned_agent_id_task_name_match: basename_exact
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
  prepare_wait_command: scripts/native_dispatch_driver.py prepare-wait
  prepare_partial_recovery_command: scripts/native_dispatch_driver.py prepare-partial-recovery
  record_partial_terminal_command: scripts/native_dispatch_driver.py record-partial-terminal
  prepare_partial_interrupt_command: scripts/native_dispatch_driver.py prepare-partial-interrupt
  record_partial_interrupt_command: scripts/native_dispatch_driver.py record-partial-interrupt
  close_partial_wave_command: scripts/native_dispatch_driver.py close-partial-wave
  advance_wave_command: scripts/native_dispatch_driver.py advance-wave
evidence_contract:
  causal_append_command: scripts/native_dispatch_driver.py append-event
  residue_append_command: scripts/native_dispatch_driver.py append-residue
  binding_correction_command: scripts/native_dispatch_driver.py correct-agent-binding
  source_time_append_required: true
  pure_reduce_live_evidence: false
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

The Python driver does not invoke `collaboration.*`. It performs the
fail-closed prepare/record handshake around the host-owned call. The parent
must receive a passing preparation receipt, invoke the exact returned request
once through the active host tool, and record the result before continuing.

## Spawn Mapping

For one admitted `spawn` action, call `collaboration.spawn_agent` exactly once with:

- a stable `task_name` derived from the action role and action identifier;
- `fork_turns: none`, so the child receives only explicitly bounded action context;
- a `message` containing the action identifier, role, capability, target, mode,
  mutation policy, input/output references, and the exact digest-bound role
  briefing: identity, angle, instructions, task-completion semantics, separate
  domain-gate semantics, explicit read policy, exact write policy, required
  receipt shape, and authority ceiling;
- a structured `briefing_binding` envelope equal to the persisted action so a
  host adapter can audit the text projection without inferring policy. A
  forbidden-write scope remains readable unless the explicit forbidden-read
  policy also prohibits it.

Use `native_dispatch_driver.py prepare-spawn` to revalidate the canonical
briefing digest and action-policy equality before persisting `action_attempted`.
Expose the exact request only after both validation and append succeed.
On success, use `record-spawn --request <prepared-request> --agent-id` to
persist `host_spawn_returned` with the native `agent_id` bound to the action.
The returned identifier basename must equal the prepared request's exact
`task_name`; mismatch blocks without changing the stream. On error
or a missing identifier, use `record-spawn --failed`, preserve any diagnostic
text in the separate residue stream, and block without implicit retry. Waiting
for the returned identifier belongs to the later join action, not spawn
mapping.

## Binding Correction

The Codex host returns a canonical agent path whose basename is the requested
`task_name`. An owner-accepted `agent_binding_corrected` batch may repair a
transcription error only before same-wave terminal or gate evidence. The
dedicated command validates the persisted action and prepared request, retains
the original host and registration events, and appends one correction. Generic
`append-event` is not the correction workflow. The mailbox-wide wait itself
is not replayed; only its non-causal pending-set projection is rebuilt for
audit.

## Join Mapping

`collaboration.wait_agent` waits for mailbox activity and does not accept a target identifier. Register each known wave agent once in a pending set, call the mailbox-wide wait operation in bounded rounds, and use `collaboration.list_agents` plus returned completion messages to reconcile only those known identifiers.

A completed known agent is logically closed once and needs no interrupt. An unresolved known agent is interrupted at most once through `collaboration.interrupt_agent`; its expected action receives an explicit `timed_out` receipt. Unknown or duplicated result identities are blocking evidence.

Use `prepare-wait` before every mailbox-wide wait. After terminal cleanup,
persist exactly one raw `<action_id>.json` task result and one closed-schema
normalized `<action_id>.json` receipt per current action, then call
`advance-wave --raw-results-dir ...`. That command first proves the raw result
satisfies the action briefing and that blocked task status cannot normalize as
PASS, then owns exact receipt admission,
`receipt_joined`, deterministic reduction, `gate_decided`, and full event
validation before dependent actions are written. The coordinator's pure
`reduce` command is offline reducer evidence only and must not be cited as a
live native-run closeout.

## Partial Spawn Recovery

If a selected-wave spawn returns `host_spawn_failed`, do not issue another
spawn in that wave and do not fabricate a receipt for the failed action. Use
`prepare-partial-recovery` to register only the successfully spawned sibling
identifiers and prepare one mailbox-wide wait. Reconcile those identifiers with
the host inventory: record completed siblings with
`record-partial-terminal`; for a still-live sibling, use
`prepare-partial-interrupt`, make its exact interrupt call once, then use
`record-partial-interrupt`.

Append one `evidence_closure` residue record for each cleaned sibling, then
use `close-partial-wave`. It emits a terminal `run_blocked` event and a typed
blocked closeout with no receipt joins, gate decision, dependent actions, or
retry. A new host run needs separate retry authority and a distinct run ID.
