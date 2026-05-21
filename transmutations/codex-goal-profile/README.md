# Codex Goal Profile

Codex Goal Profile is a Transmutation sigil for turning an Arcanum work-pack task or SWU into a strong native Codex `/goal` contract.

It does not implement `/goal`. Codex already owns the native Goal runtime: persistent thread-scoped objectives, lifecycle controls, continuation policy, budget handling, and evidence-based completion.

This transmutation exists because Arcanum work-packs contain rich execution context, while native Codex Goals need a compact operating contract.

## Problem It Solves

Work-packs are excellent dashboards:

- task board,
- waves,
- SWU manifest,
- task contracts,
- source links,
- blockers,
- validation.

Native Codex Goals are excellent runtime objectives:

- persistent outcome,
- verification surface,
- constraints,
- boundaries,
- iteration policy,
- blocked stop condition.

The missing bridge is a faithful transformation from one selected work-pack task or SWU into a native `/goal` command that Codex can run without losing scope or overstating completion.

## Use When

- a work-pack SWU is ready for execution,
- the work may require multiple Codex turns,
- the completion condition is evidence-based,
- the path is uncertain but bounded,
- the user wants Codex's native Goal lifecycle rather than a one-off prompt.

## Do Not Use When

- the task is a tiny deterministic edit,
- the work-pack/SWU lacks validation evidence,
- dependencies or write scope are unclear,
- the user wants an immediate answer,
- native Codex Goals are unavailable in the current runtime.

## Inputs

- `WORK-PACK.md`,
- selected task contract,
- selected SWU row,
- source links,
- dependencies,
- write scope,
- done criteria,
- validation command or reviewable evidence,
- blockers and budget constraints.

## Output

The output is a ready-to-run native Codex Goal profile:

```text
/goal <outcome>, verified by <evidence>, while preserving <constraints>. Use <allowed context and write scope>. Between iterations, <iteration policy>. If blocked or no valid paths remain, <stop condition and report shape>.
```

It may also include a short audit block explaining:

- source task/SWU,
- dependency status,
- write scope,
- validation surface,
- known blockers,
- why a native Goal is or is not appropriate.

## Codex Runtime Boundary

Native Codex Goals own:

- `/goal`,
- `/goal pause`,
- `/goal resume`,
- `/goal clear`,
- thread-scoped goal state,
- continuation at safe idle boundaries,
- budget-limited continuation,
- evidence-based completion.

Arcanum owns only the profile transformation and optional observability around whether the profile was useful.

Official reference: <https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex>

## Why This Is A Transmutation

The sigil transforms a structured Arcanum execution unit into a native Codex operating contract. It does not coordinate the work itself, own task execution, or create a competing runtime.
