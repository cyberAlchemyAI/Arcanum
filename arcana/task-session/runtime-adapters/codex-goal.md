# Codex Goal Runtime Adapter

Status: legacy compatibility adapter. New Task Session runtime handoffs should use [Generic Runtime Handoff](runtime-handoff.md) and treat Codex as the `codex-exec` runtime adapter when needed.

## Identity

| Field | Value |
| --- | --- |
| `runtime_id` | `codex` |
| `capability_kind` | `goal` |
| `adapter_id` | `codex-goal` |
| `profile_transmutation` | [Codex Goal Profile](../../../transmutations/codex-goal-profile/) |

## Purpose

Use Codex native `/goal` as the long-running execution runtime for one selected Arcanum work-pack task or SWU.

Task Session remains the Arcanum coordinator. Codex Goal owns only the runtime continuation loop after a safe goal profile exists.

## Availability Check

Before using this adapter, confirm:

- Codex is the active runtime for the repository command surface.
- Native Codex Goals are available and enabled for the current Codex installation.
- The selected task/SWU has bounded write scope, concrete done criteria, and validation evidence.
- Context Builder produced a handoff pack as session evidence with Markdown and JSON/index outputs.
- The handoff pack has strict coverage: every obligation is covered or explicitly resolved.

Useful local checks:

```bash
codex features list
codex features enable goals
```

If native Goals are unavailable, Task Session should either run the task locally as a bounded session or return `BLOCK` with the exact setup action.

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
- budget or stop constraint.

## Transformation

1. Read the selected work-pack row, task/SWU contract, and handoff pack/index references from Task Session.
2. Block if the handoff pack is missing, stale, contradictory, unsafe, missing write scope, missing validation, or below strict coverage.
3. Apply [Codex Goal Profile](../../../transmutations/codex-goal-profile/) with the handoff pack Markdown path and JSON/index path as first-class inputs.
4. Preserve the handoff pack identity and fallback exploration rule in the generated goal.
5. Produce either:
   - a paste-ready native Codex `/goal` command, or
   - a blocked profile with exact unblock action.

## Handoff Shape

```text
/goal <outcome>, verified by <evidence>, while preserving <constraints>. Use the handoff pack at <markdown path> and structured index at <json path> as selected source context, plus only <allowed write scope>. Broaden repository exploration only for named gaps from the pack. If you use extra sources, report the named gap, source path, and whether it changed the result. Between iterations, <iteration policy>. If blocked or no valid paths remain, stop with <blocked report shape>.
```

Task Session may print the command for the user to run, or use the runtime command directly when native command invocation is available in the current environment.

## Result Evidence

When delegation succeeds, Task Session evidence must record:

- selected runtime and adapter id,
- selected task or SWU id,
- handoff pack Markdown path,
- handoff pack JSON/index path,
- strict coverage status,
- fallback exploration status,
- any extra sources used by the runtime and the named gap that justified each source.

## Ownership Boundary

Codex Goal owns:

- native `/goal` state,
- continuation,
- pause,
- resume,
- clear,
- evidence-based runtime completion.

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

- native Goals are not enabled,
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
