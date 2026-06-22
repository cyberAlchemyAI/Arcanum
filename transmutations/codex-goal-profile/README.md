# Codex Goal Profile

Codex Goal Profile is a Transmutation sigil for turning an Arcanum work-pack task, SWU, or explicitly selected one-shot stream into a strong native Codex `/goal` contract.

It does not implement `/goal`. Codex already owns the native Goal runtime: persistent thread-scoped objectives, lifecycle controls, continuation policy, budget handling, and evidence-based completion.

This transmutation exists because Arcanum work-packs contain rich execution context, while native Codex Goals need a compact operating contract. The native goal line should stay small enough for the runtime input budget; richer Arcanum context belongs in the handoff pack or a sidecar profile.

When used from Task Session, the profile also consumes a Context Builder handoff pack. That pack is stored as session evidence, emitted as Markdown plus JSON/index, and must pass strict coverage before a runnable native Goal is generated.

## Problem It Solves

Work-packs are excellent dashboards:

- task board,
- waves,
- SWU manifest,
- task contracts,
- source links,
- blockers,
- validation,
- handoff pack paths and strict coverage status.

Native Codex Goals are excellent runtime objectives:

- persistent outcome,
- verification surface,
- constraints,
- boundaries,
- iteration policy,
- blocked stop condition.
- pack-first context boundary.

The missing bridge is a faithful transformation from one selected work-pack task, SWU, or explicitly selected one-shot stream into a native `/goal` command that Codex can run without losing scope or overstating completion.

## Use When

- a work-pack SWU is ready for execution,
- the work may require multiple Codex turns,
- the completion condition is evidence-based,
- the path is uncertain but bounded,
- the user wants Codex's native Goal lifecycle rather than a one-off prompt.
- the user selected a full ordered stream and wants one gated goal that can finish the project slice.
- a local runtime decision profile should influence risk, approval, sequencing, and stop conditions without being copied into public artifacts.

## Do Not Use When

- the task is a tiny deterministic edit,
- the work-pack/SWU lacks validation evidence,
- dependencies or write scope are unclear,
- the user wants an immediate answer,
- native Codex Goals are unavailable in the current runtime.
- the user did not select a single unit or explicit one-shot stream.
- the requested one-shot would need broad ambient authority or unbounded exploration.

## Inputs

- `WORK-PACK.md`,
- selected task contract,
- selected SWU row,
- selected one-shot stream, when explicitly requested,
- source links,
- dependencies,
- write scope,
- done criteria,
- validation command or reviewable evidence,
- handoff pack Markdown path,
- handoff pack JSON/index path,
- strict coverage status,
- fallback exploration rule,
- blockers and budget constraints.
- native goal character budget, default `4000`,
- optional private/runtime decision profile path,
- optional capability policy for `refine`, `invoke`, `craft`, `decision-gate`, and subagents.

## Output

The output is a ready-to-run native Codex Goal profile. The `/goal` line should target the configured character budget. Default: 4000 characters.

```text
/goal <compact outcome and verification>. Use <sidecar or handoff pack> as the execution frame. Stay within <write scope>. Use only named capability lanes and stop on <blocked condition>.
```

It may also include a short audit block explaining:

- source task/SWU,
- dependency status,
- write scope,
- validation surface,
- handoff pack Markdown and JSON/index,
- strict coverage status,
- fallback exploration rule,
- extra-source reporting requirement,
- known blockers,
- goal budget status,
- decision profile path and policy fields consumed, when supplied,
- one-shot capability policy and receipt gates, when enabled,
- sidecar profile path, when the compact goal needs one,
- why a native Goal is or is not appropriate.

The transmutation returns `block` instead of a runnable Goal when the handoff pack is missing, strict coverage failed, validation or write scope is absent, fallback exploration would require broad unnamed discovery, the goal cannot fit the character budget and no sidecar is available, or a one-shot stream lacks explicit capability gates.

## Compact Goal And Sidecar Pattern

When the execution vision is larger than the native `/goal` line, generate:

1. a compact `/goal` under the configured character budget;
2. a sidecar profile or handoff artifact with the richer Arcanum frame;
3. an audit block naming what lives in the sidecar.

The goal carries control. The sidecar carries density.

## Decision Profiles

When a private runtime profile such as `.arcanum/profiles/decision-profile.yml` is supplied, it may influence risk posture, approval gates, slice sequencing, ownership boundaries, gap-filling style, technique preferences, and anti-pattern stops.

Do not copy private profile contents into reusable public examples or canonical package text. A generated goal profile should name the profile path and summarize only the operational policy consumed for that run.

## One-Shot Streams

One-shot mode is for an explicitly selected ordered stream, not an unselected bundle. A one-shot goal may authorize bounded use of Arcanum capabilities:

- `refine` for named design or plan gaps,
- `invoke` for missing define/design/plan/handoff artifacts,
- `craft` for scoped ledger state,
- `decision-gate` for blocker-level choices,
- subagents when explicitly authorized and receipt-gated.

The one-shot goal should still run prerequisite and contract gates before runtime implementation and stop when a decision or scope change is needed.

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
