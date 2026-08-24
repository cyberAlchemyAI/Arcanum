# Runtime Adapter Profile: app-server-fixture

## Purpose

`app-server-fixture` is a development-only reducer for deterministic synthetic Codex App Server traces. It exercises the proposed provider-local identity, cursor, ordering, replay, policy, terminal-normalization, and authority-separation contracts without starting App Server, making a network request, or running a model turn.

The id `app-server` is reserved for a future live adapter. This fixture profile is not registered in `tools/arcanum` and must not be selected as an execution adapter.

## Contract

| Field | Value |
| --- | --- |
| `adapter_id` | `app-server-fixture` |
| `runtime_kind` | `synthetic-event-reducer` |
| `execution_mode` | `fixture-replay-only` |
| `state_model` | provider-local identity map plus ordered cursor |
| `input_shape` | pinned profile, immutable handoff, JSONL events |
| `output_shape` | adapter state, `app-server.host-result.v0`, runtime status |
| `proof_status` | `fixture-observed` |

The reducer accepts exactly one ordered F-01 lifecycle:

```text
runtime.created
  -> app_server.initialized
  -> thread.started
  -> turn.started
  -> item.started
  -> item.completed
  -> turn.completed
  -> normalized host result
  -> STOP: owner-local stage verdict pending
```

It rejects missing, extra, reordered, duplicated, identity-conflicting, payload-changing, or policy-expanding events. It never treats resume, replay, host completion, or a JSON-RPC identity as Arcanum admission or authority.

## Output Boundary

The validator writes only to a caller-supplied output directory that is nonexistent or empty. Existing output bytes are never overwritten. Output JSON is canonical and contains no runtime-generated timestamps.

`host-result.json` is fixture-observed raw host evidence. Owner and semantic verdicts, gates, receipts, Task Session, Craft, Goal, and promotion fields remain null. A successful fixture therefore proves the reducer contract only; it does not prove installed-binary parity, live integration, execution correctness, semantic acceptance, promotion, publication, release, deployment, or production readiness.
