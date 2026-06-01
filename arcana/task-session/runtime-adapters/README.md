# Task Session Runtime Adapters

Runtime adapters let Task Session delegate bounded execution to the active agent runtime without making that runtime the Arcanum contract.

Task Session owns:

- work-pack resolution,
- task/SWU selection,
- dependency and blocker checks,
- strict context handoff coverage,
- runtime selection,
- adapter handoff,
- result review,
- evidence synchronization.

The runtime owns only the execution lifecycle it explicitly supports, such as durable run creation, adapter execution, pause/resume when available, or completion.

## Adapter Contract

Each adapter should define:

| Field | Meaning |
| --- | --- |
| `runtime_id` | Runtime name, such as `codex`. |
| `capability_kind` | Runtime capability, such as `durable-run`, `background-task`, or `subagent`. |
| `availability_check` | How to confirm the runtime feature is available. |
| `input_contract` | Required fields from the selected work-pack task or SWU. |
| `context_handoff` | Handoff pack Markdown path, JSON/index path, strict coverage status, and fallback exploration rule. |
| `transformation` | How Arcanum task context becomes the runtime command. |
| `handoff_shape` | Exact command or prompt shape given to the runtime. |
| `result_evidence` | Pack identity, strict coverage, fallback-search status, and any extra sources used for named gaps. |
| `ownership_boundary` | What the runtime owns and what Task Session still owns. |
| `blocked_fallback` | What to do when the adapter cannot safely run. |

## Current Adapters

- [Generic Runtime Handoff](runtime-handoff.md) - creates a durable Arcanum runtime run for one work-pack task/SWU through `tools/arcanum-runtime-run`.
- [Codex Goal](codex-goal.md) - legacy adapter that translates one work-pack task/SWU into native Codex `/goal` using the Codex Goal Profile transmutation.

Runtime adapters must block when the session lacks a complete session-evidence handoff pack. A runnable handoff requires Markdown plus JSON/index session evidence, strict obligation coverage, bounded write scope, validation surface, and fallback exploration limited to named gaps.

Successful delegation evidence must keep the pack identity first-class: Markdown path, JSON/index path, strict coverage, fallback-search status, and any extra source used by the runtime with the named gap that justified it.
