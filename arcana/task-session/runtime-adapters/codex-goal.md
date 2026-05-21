# Codex Goal Runtime Adapter

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
- budget or stop constraint.

## Transformation

1. Read the selected work-pack row and task/SWU contract.
2. Apply [Codex Goal Profile](../../../transmutations/codex-goal-profile/).
3. Produce either:
   - a paste-ready native Codex `/goal` command, or
   - a blocked profile with exact unblock action.

## Handoff Shape

```text
/goal <outcome>, verified by <evidence>, while preserving <constraints>. Use only <allowed context and write scope>. Between iterations, <iteration policy>. If blocked or no valid paths remain, stop with <blocked report shape>.
```

Task Session may print the command for the user to run, or use the runtime command directly when native command invocation is available in the current environment.

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
- reviewing the runtime result,
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
- the work-pack and task contract disagree.

The fallback report should name the blocked field and the smallest next action to make the runtime handoff safe.
