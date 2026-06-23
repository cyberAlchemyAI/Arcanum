# UX Lessons

Turn a UI iteration session into **saved lessons** and **reusable ux-patterns** — then hand those patterns to the tools that consume them. A thin producer: it owns the lesson/pattern artifacts and two consumer adapters, and **composes** existing Arcanum capabilities for everything else.

## Problem solved

When you iterate a page (try 3D, revert it, move a panel, add a tour…), the *reasons* for each change are valuable and usually lost. UX Lessons captures each move as a typed **lesson**, distills recurring lessons into a reusable **ux-pattern**, and emits that pattern as ready-to-use intents for:

- **[ux-evidence-validator](../ux-evidence-validator/)** — as a claim map across five authority classes (`hard_gate`/`soft_flag`/`screenshot_review`/`human_study`/`not_automatable`), entering at `--mode spec`.
- **`ui-prototyping-studio`** (a separate consuming project) — as a `CommentEvent → MutationTask` annotation intent.

## Use it when

- a UI iteration session produced changes worth keeping,
- a recurring UX move should become a named, evidence-linked pattern,
- a pattern should feed evidence validation or prototyping.

## Do not use it when

- you want to run browser validation now → use ux-evidence-validator,
- you want to generate/mutate UI variants now → use ui-prototyping-studio,
- the input is generic workflow telemetry → use workflow-reflect,
- there is no session evidence (patterns may not be invented without a lesson).

## Inputs & outputs

| Mode | In | Out |
| ---- | -- | --- |
| `capture` | session ref + evidence | `lesson` records |
| `distill` | ≥1 lessons | a `ux-pattern` card (`seed`) |
| `promote` | a pattern | advanced status (honesty-gated) |
| `emit-validator` | a pattern | validator claim map → `--mode spec` |
| `emit-studio` | a pattern | `CommentEvent → MutationTask` |

## What it owns vs composes

**Owns:** the `lesson` schema, the `ux-pattern` schema, the two consumer adapters, the promotion honesty gate.

**Composes (never re-implements):** `signal-observer`/`observed-invocation-loop` (session signal), `workflow-reflect` (analysis shape), `distill` (reduction), `architecture-pattern-inventory` (pattern store, `ux` tag), `residuality-spec` (residue).

## Tier & status

Tier: **arcana** (cross-session learning translation). Status: **seed** — contract + one founding example exist; no experiment-harness or cross-session evidence yet. A `ux-pattern` stays `seed` until usage evidence supports it (claim ≤ proof).

## Honesty rules

- `lesson.evidence` is constrained to `{dom_measurement, aria_snapshot, screenshot_diff, trace_event}`.
- An **anecdote-signal** lesson cannot drive a validator **hard gate** — only soft flags or screenshot review until cross-session signal accrues.
- The studio **variant/fitness** intake is deferred behind a named unblock (studio OQ-5 + a fitness evaluator); only the annotation intake is live.

## Provenance

Designed by the refine run at [development/refinement-runs/2026-06-23-ux-lessons/](development/refinement-runs/2026-06-23-ux-lessons/) (RESULT.md), using the x-ray HTML iteration session as the founding fixture. First pattern: [`detail-beside-the-subject`](examples/detail-beside-the-subject.md).
