# Task Session Runtime Adapters

Runtime adapters let Task Session delegate bounded execution to the active agent runtime without making that runtime the Arcanum contract.

Task Session owns:

- work-pack resolution,
- task/SWU selection,
- dependency and blocker checks,
- runtime selection,
- adapter handoff,
- result review,
- evidence synchronization.

The runtime owns only the execution lifecycle it explicitly supports, such as goal continuation, pause, resume, or completion.

## Adapter Contract

Each adapter should define:

| Field | Meaning |
| --- | --- |
| `runtime_id` | Runtime name, such as `codex`. |
| `capability_kind` | Runtime capability, such as `goal`, `background-task`, or `subagent`. |
| `availability_check` | How to confirm the runtime feature is available. |
| `input_contract` | Required fields from the selected work-pack task or SWU. |
| `transformation` | How Arcanum task context becomes the runtime command. |
| `handoff_shape` | Exact command or prompt shape given to the runtime. |
| `ownership_boundary` | What the runtime owns and what Task Session still owns. |
| `blocked_fallback` | What to do when the adapter cannot safely run. |

## Current Adapters

- [Codex Goal](codex-goal.md) - translates one work-pack task/SWU into native Codex `/goal` using the Codex Goal Profile transmutation.
