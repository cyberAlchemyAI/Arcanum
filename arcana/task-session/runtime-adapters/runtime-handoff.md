# Generic Runtime Handoff Adapter

## Identity

| Field | Value |
| --- | --- |
| `runtime_id` | `arcanum-runtime` |
| `capability_kind` | `durable-run` |
| `adapter_id` | `runtime-handoff` |
| `runner` | Native runtime handoff via `tools/arcanum --exec` |
| `handoff_template` | `framework/runtime/templates/RUNTIME-HANDOFF.md` |

## Purpose

Create a durable Arcanum runtime run for one selected Task Session work-pack task or SWU without making any specific agent runtime part of the Task Session contract.

Task Session remains the Arcanum coordinator. The runtime owns only the bounded execution lifecycle inside the durable run folder.

## Availability Check

Before using this adapter, confirm:

- `tools/arcanum` exists and is executable,
- `framework/runtime/templates/RUNTIME-HANDOFF.md` exists,
- the selected task/SWU has bounded write scope, concrete done criteria, and validation evidence,
- Context Builder produced a handoff pack as session evidence with Markdown and JSON/index outputs,
- the handoff pack has strict coverage,
- the requested runtime adapter is available, such as `native-skill`, `codex-skill`, `claude-skill`, `copilot-instructions`, `dry-run`, or explicit legacy `codex-exec`.

Useful local checks:

```bash
test -x tools/arcanum
test -f framework/runtime/templates/RUNTIME-HANDOFF.md
```

## Input Contract

The adapter consumes exactly one selected task or SWU from a work-pack.

Required fields:

- source `WORK-PACK.md`,
- selected task id or SWU id,
- parent task contract,
- source links,
- dependency status,
- write scope,
- done criteria,
- validation command or reviewable evidence,
- blocker state,
- handoff pack Markdown path,
- handoff pack JSON/index path,
- strict coverage status,
- fallback exploration rule,
- runtime adapter id,
- runtime run id or run directory,
- budget or stop constraint.

## Transformation

1. Read the selected work-pack row, task/SWU contract, and handoff pack/index references from Task Session.
2. Block if the handoff pack is missing, stale, contradictory, unsafe, missing write scope, missing validation, or below strict coverage.
3. Write a runtime handoff request using `framework/runtime/templates/RUNTIME-HANDOFF.md`.
4. Put task objective, write scope, validation, context pack paths, strict coverage, fallback rule, and synchronization obligations into the handoff.
5. Dispatch through the parent native runtime surface, or use `tools/arcanum --exec --adapter <adapter-id> --output <output> <command> <request>` to prepare a native handoff/receipt contract when execution is requested. `tools/arcanum-runtime-run` is a deprecated compatibility wrapper only.
6. Produce either a durable runtime run folder or a blocked handoff with exact unblock action.

## Handoff Shape

```bash
tools/arcanum --exec \
  --adapter <adapter-id> \
  --output <session-evidence>/runtime-output.md \
  <command> \
  "<request that cites the session handoff pack and index>"
```

For native adapters, `tools/arcanum --exec` must not spawn nested model-backed CLIs. It prepares a handoff prompt and receipt contract for the current host runtime. The handoff prompt must instruct the adapter to use the handoff pack Markdown and JSON/index as selected source context, keep writes inside the allowed write scope, broaden repository exploration only for named gaps, and stop with a blocked report when no valid execution path remains.

## Result Evidence

When delegation succeeds, Task Session evidence must record:

- selected runtime and adapter id,
- runtime run directory,
- runtime `RUN.json`,
- runtime `STATUS.json`,
- runtime `RESULT.md`,
- runtime `events.jsonl`,
- selected task or SWU id,
- handoff pack Markdown path,
- handoff pack JSON/index path,
- strict coverage status,
- fallback exploration status,
- any extra sources used by the runtime and the named gap that justified each source.

## Ownership Boundary

The runtime owns:

- durable run lifecycle,
- adapter-specific execution,
- runtime status,
- runtime result,
- runtime events,
- adapter state isolation.

Task Session owns:

- choosing the task/SWU,
- checking Arcanum blockers,
- choosing this adapter,
- preserving source navigation,
- preserving handoff pack/index navigation,
- enforcing strict coverage before runtime handoff,
- reviewing the runtime result,
- reviewing any fallback exploration against named gaps,
- updating work-pack status,
- recording validation and observability evidence.

## Blocked Fallback

Return `BLOCK` before mutation when:

- `tools/arcanum` is unavailable,
- no runtime adapter is selected,
- no single task/SWU is selected,
- dependencies are unmet,
- write scope is broad or missing,
- done criteria are vague,
- validation evidence is absent,
- handoff pack or JSON/index is absent,
- strict coverage failed,
- fallback exploration would require broad unnamed discovery,
- the work-pack and task contract disagree.

The fallback report should name the blocked field and the smallest next action to make the runtime handoff safe.
