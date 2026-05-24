# Refine

Refine is an Arcana sigil for creating a confirmed refinement seed before Task Session execution.

It is the front door for requests such as "refine this design," "use full refinement on this folder," or "turn this vague target into a refinement run." It proposes the first bounded task/work-pack, offers research, selects a budget preset, explains the loop, asks for confirmation, and then routes the approved unit to Task Session.

## Problem It Solves

Task Session needs one approved task or SWU. Users often start one step earlier: they have a target, concern, or folder, but not a work-pack with write scope, done criteria, validation, and runtime handoff fields.

Refine creates that missing seed without making Task Session invent work. This keeps planning, execution, and lifecycle ownership separate.

## Use When

- a refinement target is vague or only points to a folder, idea, design, or plan,
- the user wants a budget and loop count before execution,
- research should be offered before refinement,
- Codex Goal should be the default runtime once the seed is approved,
- a seed task/work-pack is needed before Task Session can run safely.

## Do Not Use When

- an approved work-pack task/SWU is already selected and the user wants immediate execution,
- the work only needs a direct edit,
- the user wants a full Invoke design/plan without execution routing,
- Codex Goal strict handoff requirements are impossible and the user has not explicitly requested local fallback.

## Ownership Model

| Capability | Owns |
| --- | --- |
| Refine | Seed proposal, research offer, preset recommendation, confirmation gate, default runtime route. |
| Task Session | Context pack, gates, execution, validation, runtime handoff, evidence sync. |
| Refinement Loop | Loop phases, pass limits, research bounds, repair and synthesis requirements. |
| Context Builder | Context packs and Codex Goal handoff packs. |
| Codex Goal Profile | Native Codex Goal text from one selected task/SWU. |
| Sigil Development | Reusable sigil lifecycle, examples, observability, experiment evidence, promotion. |

## Refinement Loop

Refine owns the one-loop unit in [Refinement Loop](REFINEMENT-LOOP.md), but it does not hand-roll or babysit the phase behavior. Refine prepares the executable loop plan, then Task Session runs it through Codex Goal so each stage routes through the installed skill/sigil contract and preserves the stage's observation envelope, gates, and embedded workflow:

```text
context-builder
  -> invoke define
  -> interrogation
  -> Research Offer
  -> distill
  -> invoke redefine + design/plan
  -> sigil-development handoff or synthesis
```

The loop contract is the source of truth for loop mechanics. Refine selects and prepares the loop; Task Session executes it; the required skills own their stage internals.

## Research Offer

Refine always offers research before running refinement:

- `no-research`: local repository and supplied context only.
- `bounded-research`: one external comparison pass within the loop's research bounds.
- `research-if-gap-appears`: default; start local-first and ask again only if a named gap appears.

External research never overrides local repository evidence.

## Runtime Default

Refine defaults to Codex Goal through Task Session:

```text
/task-session to <seed-work-pack> --task <TASK-ID> --runtime codex --via goal
```

If strict handoff coverage is missing, Refine blocks and names the missing field. It does not silently fall back to local execution.

## Output

Refine returns a seed proposal first. It writes seed artifacts or delegates only after confirmation.

## Lifecycle Evidence

`refine` is a pilot sigil. Its Experiment Harness lives under [development/](development/) with the `sigil-development` profile:

```text
development/run-example-with-codex.sh next
development/run-validation-fixtures.sh
development/write-experiment-report.sh
```

Promotion requires realistic live outputs for seed proposal, existing work-pack preflight, research decision, blocked handoff, confirmed Task Session route behavior, and at least one final refinement result produced through Task Session/Codex Goal. Proposal-only output is preflight evidence, not promotion evidence. Sigil-local telemetry and reflection templates live under [templates/](templates/).
