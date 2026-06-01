# Distill Review: Refine

> Historical note: this review predates dispatch-route hardening. Codex Goal wording below is retained as older design evidence and superseded by dispatch-spec route validation plus runtime handoff.

## Target Context

Design the smallest coherent `refine` sigil that fills the gap before Task Session execution without duplicating existing Arcanum capabilities.

## Candidate Units

| Candidate | Description | Strength | Weakness | Verdict |
| --- | --- | --- | --- | --- |
| Seed/preflight controller | Proposes a minimal seed task/work-pack, research mode, budget, and Codex Goal route before Task Session. | Solves the missing seed problem while preserving existing ownership. | Requires careful confirmation gate. | selected |
| Task Session fallback mode | Task Session creates a minimal work-pack when none exists. | Fewer user-visible capabilities. | Blurs planning and execution authority. | rejected |
| Invoke wrapper | Invoke creates the first work-pack and routes to Task Session. | Keeps planning in Invoke. | Does not explain budget/loop choices as a reusable refinement interface. | rejected |
| New refinement engine | `refine` owns a separate loop implementation. | Self-contained. | Duplicates the Refine Loop contract and will drift. | rejected |

## Selected Smallest Coherent Unit

**Refinement seed/preflight controller**

## Closure Proof

Inputs:

- vague target, folder, idea, design concern, or existing work-pack,
- optional requested preset,
- optional requested research mode,
- local repository evidence.

Process:

- summarize the target,
- propose a seed task/work-pack when needed,
- offer research,
- select a preset and loop count by referencing `REFINEMENT-LOOP.md`,
- explain Codex Goal readiness,
- ask for confirmation,
- route to Task Session only after confirmation.

Outputs:

- seed proposal or seed work-pack,
- research decision,
- recommended Task Session command,
- blocked handoff report when strict Codex Goal coverage is missing.

## Recomposition Proof

- Task Session consumes the approved task/SWU and owns execution.
- Refine Loop owns phases and limits.
- Context Builder produces runtime handoff packs.
- Codex Goal Profile turns the selected unit into a native goal only after strict coverage.
- Sigil Development owns the reusable `refine` package and promotion evidence.

## Deferred Complexity

- direct runtime execution,
- local fallback automation,
- automatic external research,
- full Invoke replacement,
- native platform goal control.

## Distill Verdict

Pass. Build `refine` as a seed/preflight controller.
