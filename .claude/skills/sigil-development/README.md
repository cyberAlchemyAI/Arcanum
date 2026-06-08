# Sigil Development

Sigil Development is an Arcana sigil for designing, validating, observing, reflecting on, and iterating other sigils.

It turns sigil authoring into a governed lifecycle rather than a one-time file-writing task. The sigil guides the author through candidate capture, tier classification, behavior design, validation, trial execution, observability setup, reflection, and maintenance.

For reusable sigils, observability should include a post-run hook that can summarize the latest request and save one JSON event for later reflection.

Sigil Development is the lifecycle owner for sigil artifacts. It may consume handoff packets produced by [Invoke](../../spells/invoke/), but Invoke does not replace this lifecycle.

## Problem It Solves

Sigils can decay after they are written. A process can look clear in the first draft but later reveal ambiguous triggers, weak Quality Bars, missing Anti-Patterns, output drift, or repeated workflow gaps.

This sigil solves that by making observability part of the development lifecycle. Each sigil should emit enough usage telemetry for later reflection, and reflection should feed targeted improvements back into the sigil instead of relying on memory or anecdote.

## Use When

- creating a new sigil,
- revising an existing sigil,
- continuing from an Invoke handoff that targets sigil creation or revision,
- adding observability or telemetry to a sigil,
- evaluating whether a sigil is ready for promotion,
- reflecting on usage signals after repeated executions,
- investigating workflow gaps discovered during sigil use.

## Do Not Use When

- the task is only to run an already-defined sigil,
- the requested change is a tiny typo fix with no behavior impact,
- the user only needs a quick explanation of the library structure,
- no reusable capability is being created or maintained,
- the work is only early intent discovery and has no sigil target yet; use Invoke first.

## Chain Position

Sigil Development sits after Invoke and before execution:

```text
invoke handoff -> sigil-development lifecycle work -> task-session for approved implementation tasks
```

Responsibilities:

- Invoke owns discovery, authoring baseline, and handoff artifacts.
- Sigil Development owns sigil contract mutation, experiment harness, validation, observability, reflection, and promotion readiness.
- Task Session owns bounded execution of approved work-pack tasks or SWUs.
- Experiment Harness owns repeatable test mechanics, live Codex examples, validation reports, and telemetry emission for reusable sigils.

If a sigil needs a composed multi-sigil workflow, route that composition through Spellcraft instead of expanding this sigil's contract.

## Codex Goal And Experiment Closure

When sigil implementation work uses Codex native Goals, close the loop through both Task Session and Experiment Harness:

```text
sigil-development owns lifecycle work-pack
  -> task-session selects one ready task/SWU
  -> codex-goal adapter creates native /goal
  -> Codex executes the bounded runtime goal
  -> task-session reviews evidence and syncs the work-pack
  -> experiment-harness validates reusable behavior
  -> sigil-development consumes validation, telemetry, and reflection signals
```

Codex Goal evidence can prove that one bounded implementation unit completed. It does not replace the experiment harness. A reusable sigil is not promotion-ready until experiment evidence checks realistic prompts, output shape, Quality Bar, Anti-Patterns, and observability.

For sigil lifecycle proof, initialize the harness with the Sigil Development profile:

```bash
arcana/experiment-harness/scripts/init-harness.sh <sigil-path> --type sigil --profile sigil-development
```

This keeps Experiment Harness responsible for mechanics while Sigil Development remains responsible for lifecycle judgment.

## Lifecycle Model

Sigil Development uses a closed lifecycle:

1. Design: define intent, tier, scope, and behavior.
2. Implement: execute approved work-pack tasks or SWUs through Task Session, optionally via Codex Goal.
3. Experiment: run or preserve the artifact-local Experiment Harness for realistic examples and regimes.
4. Validate: check folder structure, links, Quality Bar, Anti-Patterns, output contract, and experiment evidence.
5. Observe: define usage telemetry and emit a signal after meaningful usage or experiment reports.
6. Reflect: synthesize usage signals manually, by threshold, or when workflow gaps appear.
7. Iterate: apply targeted updates while preserving the sigil's core contract.

## Subagent Observer

This sigil uses a separate observer subagent when telemetry or reflection is needed.

The observer subagent should not rewrite the sigil directly. Its job is to inspect usage outputs, identify signals, classify gaps, and produce telemetry or reflection recommendations. The main agent remains responsible for applying changes after review.

If a subagent mechanism is unavailable, run the observer pass as a clearly labeled separate analysis step and preserve the same output format.

## Observability Outputs

The sigil can produce:

- per-use telemetry signals,
- post-run invocation JSON,
- threshold state summaries,
- reflection reports,
- iteration recommendations,
- updated Quality Bar or Anti-Patterns proposals.

## Path Model

Sigil Development is artifact-local. Keep active draft artifacts inside each sigil folder, not in a top-level shared development index.

Use:

```text
<tier>/<sigil-name>/
	README.md
	SKILL.md
	development/
		WAVE-PLAN.md                optional
		IMPLEMENTATION-LAYERING.md  optional
		DECISIONS.md                optional
		VALIDATION.md               optional
```

Templates live in [templates/](templates/).

## Reflect Triggers

Reflection can be triggered in three ways:

- Manual: a user asks for review, reflection, or improvement.
- Threshold-based: usage signals or generated outputs exceed a configured count.
- Gap-based: a workflow gap, repeated misuse, failed Quality Bar, or unclear output contract is identified.

Default thresholds are intentionally conservative: reflect after 5 meaningful executions, 10 generated artifacts, 3 repeated gap signals, or 1 severe workflow gap.

## Why This Is Arcana

This sigil coordinates a recursive lifecycle, delegates observation to a subagent, preserves evidence across executions, and routes reflection into governed iteration. Its primary behavior is lifecycle orchestration, not a single deterministic check or bounded synthesis artifact.
