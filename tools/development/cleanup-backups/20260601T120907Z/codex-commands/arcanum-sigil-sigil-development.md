# Arcanum Sigil: sigil development

<!-- arcanum:capability-id sigil-development -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-sigil-development -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-sigil-development-<UTC timestamp>`.
- `capability.id`: `sigil-development`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `sigil-development` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `sigil-development`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/sigil-development/README.md

````markdown
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

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/sigil-development/SKILL.md

````markdown
---
name: sigil-development
description: "Use when: creating, revising, observing, reflecting on, or iterating a sigil through the governed sigil lifecycle. Includes subagent-based observability and telemetry generation."
argument-hint: "<sigil-name-or-candidate> [--new | --update | --observe | --reflect] [--threshold <count>]"
tier: arcana
domain: sigil-governance
version: 0.1.0
origin: created to make sigil authoring observable, ready for reflection, and iteratively maintainable
allowed-tools: Read, Write, Glob, Grep, Task
---

# Sigil: Sigil Development

<objective>
Guide a sigil through design, validation, observability, reflection, and iteration so the sigil can improve from usage evidence while preserving its core contract.
</objective>

<logic-type>
Arcana: recursive lifecycle governance with subagent-assisted observation and reflection gates.
</logic-type>

<applicability>
Use this sigil for:

- creating a new sigil,
- converting a draft workflow into a sigil,
- continuing from an Invoke handoff that targets sigil creation or revision,
- revising an existing sigil's behavior contract,
- adding observability or telemetry to a sigil,
- adding a post-run hook that summarizes the latest sigil request into JSON telemetry,
- selecting or installing a repository-local observability package for a consuming repository,
- reflecting on accumulated usage signals,
- improving Quality Bar, Anti-Patterns, templates, or output contracts after evidence shows gaps.
  </applicability>

<inputs>
Expected inputs, if available:

- sigil name or candidate capability,
- target tier or suspected tier,
- problem statement,
- current `README.md`, `SKILL.md`, templates, or draft notes,
- examples of successful or failed usage,
- generated outputs from prior sigil runs,
- experiment harness files under `development/`,
- known workflow gaps, repeated confusion, or review comments,
- desired telemetry threshold, if different from defaults.
  </inputs>

<chain-boundary>
Sigil Development is the lifecycle owner for sigil artifacts.

- `invoke` owns early discovery, definition, design, planning, and handoff packets.
- `sigil-development` owns sigil contract mutation, experiment harness, validation, observability, reflection, iteration, and promotion readiness.
- `spellcraft` owns composed multi-sigil spell workflows.
- `task-session` owns bounded execution from approved work-pack tasks or SWUs.
- `experiment-harness` owns repeatable test mechanics, realistic prompts, live Codex examples, validation reports, and telemetry emission for reusable sigils.

When the input is an Invoke handoff, consume the handoff as source context, then take lifecycle ownership of the sigil. Do not send the user back to Invoke unless the handoff is missing the target intent, scope, or artifact objective needed to proceed.
</chain-boundary>

<codex-goal-closure-loop>
Codex Goal is a runtime execution lane, not a validation substitute.

When implementation work is delegated through Task Session and the `codex-goal` adapter:

1. Sigil Development owns the lifecycle work-pack and promotion decision.
2. Task Session selects one ready task/SWU and checks gates.
3. The Codex Goal adapter generates or hands off one native `/goal`.
4. Codex executes the bounded runtime goal.
5. Task Session reviews the result against the original task/SWU and syncs work-pack evidence.
6. Experiment Harness runs or validates the artifact-local examples/regimes.
7. Sigil Development consumes the experiment report, observability signal, and reflection trigger state before marking lifecycle progress.

Required runtime evidence shape:

```yaml
runtime: codex
adapter: codex-goal
source_swu: <id>
result: pass | flag | block | interrupted
files_touched:
  - <path>
validation:
  - <command or review evidence>
experiment_harness:
  status: pass | flag | block | not_run
  report: <path or none>
remaining_blockers:
  - <blocker or none>
lifecycle_owner_next_step: validate | observe | reflect | iterate | promote
```

A sigil implementation SWU is not lifecycle-complete until runtime evidence is reviewed and the relevant experiment harness state is updated or explicitly blocked.
</codex-goal-closure-loop>

<default-output>
If creating or updating a sigil, write or update files in:

```text
<tier>/<sigil-name>/
```

If draft planning artifacts are needed, colocate them under:

```text
<tier>/<sigil-name>/development/
```

If adding observability, create or update templates under:

```text
<tier>/<sigil-name>/templates/
```

If reflecting on a sigil, produce a reflection report using `templates/reflection-report.md` or a sigil-local equivalent.
</default-output>

<subagent-contract>
Use a separate observer subagent for observability and reflection work when a subagent mechanism is available.

Observer subagent scope:

1. Inspect the target sigil files and usage outputs.
2. Generate telemetry signals using the usage telemetry schema.
3. Identify workflow gaps, quality failures, anti-pattern hits, and output-contract drift.
4. Recommend reflection triggers and iteration candidates.
5. Return findings only; do not edit files directly unless explicitly delegated.

If no subagent mechanism is available, run the observer pass as a separate clearly labeled analysis step and preserve the same report structure.
</subagent-contract>

<process>
1. Determine mode: `--new`, `--update`, `--observe`, or `--reflect`. If no mode is provided, infer the smallest mode that satisfies the user request and state the inference.
2. Gather target context: read existing sigil files, Invoke handoff artifacts when present, relevant templates, usage outputs, and any prior telemetry or reflection artifacts.
3. Classify or confirm the sigil tier using the Formulae, Transmutations, and Arcana concept files.
4. Design or revise the human-facing `README.md`: problem solved, usage conditions, non-usage conditions, inputs, outputs, tier rationale, and lifecycle expectations.
5. Design or revise `SKILL.md`: objective, logic type, applicability, inputs, process, Quality Bar, Anti-Patterns, output contract, and origin.
6. Ensure a reusable sigil has an experiment harness:
   - initialize `development/` through `experiment-harness` when creating a new sigil,
   - use `--profile sigil-development` when validating the Sigil Development lifecycle around a target sigil,
   - add or preserve low, medium, and complex task examples when the sigil will be promoted,
   - keep Codex CLI runs explicit through `development/run-example-with-codex.sh`,
   - require real output bodies, not save-summary evidence.
7. When implementation tasks are executed through Task Session or Codex Goal, require the runtime evidence shape and route reusable-behavior proof through Experiment Harness before promotion readiness.
8. Add observability design:
   - define what counts as a meaningful execution,
   - define which usage outputs should emit telemetry,
   - define whether the general post-run hook should append invocation JSON,
   - define default reflection thresholds,
   - define gap categories and severity levels,
   - add telemetry and reflection templates when useful.
9. Delegate to the observer subagent when telemetry or reflection is needed. The observer must inspect usage outputs and return structured signals before synthesis.
10. Synthesize observer results into one of three outcomes:
   - no change needed,
   - targeted iteration recommended,
   - reflection gate required before further use.
11. Apply targeted edits only after the reflection outcome is clear. Preserve the sigil's core contract unless the evidence shows the contract itself is wrong.
12. Validate the result: folder structure, markdown links, tier fit, Quality Bar, Anti-Patterns, experiment harness state, telemetry schema, reflection triggers, and product-neutral wording.
13. Return a concise result with files changed, validation performed, reflection trigger state, and next recommended lifecycle step.
</process>

<observability-model>
A meaningful execution is any sigil use that produces or attempts to produce a user-facing artifact, decision, validation result, orchestration result, or reflection report.

Telemetry should capture:

- sigil name and tier,
- execution mode,
- generated output count,
- Quality Bar pass/fail/partial status,
- Anti-Patterns observed or avoided,
- workflow gaps,
- output-contract drift,
- user correction or clarification signals,
- observer recommendations,
- reflection trigger state.

Use `templates/usage-telemetry.md` as the default schema reference.

Use `framework/observability/SIGIL-OBSERVABILITY-HOOK.md` as the default hook pattern when a sigil needs to summarize the latest request and save it as JSON telemetry.

Use `framework/observability/REPOSITORY-PACKAGE.md` and the `observability-setup` sigil when a consuming repository needs local telemetry storage.
</observability-model>

<reflection-policy>
Run reflection when any of these triggers occur:

- Manual trigger: the user asks to reflect, review, improve, tune, or iterate the sigil.
- Usage threshold: the sigil reaches 5 meaningful executions unless a sigil-local threshold overrides it.
- Output threshold: the sigil produces or modifies 10 artifacts since the last reflection.
- Gap threshold: 3 related workflow gaps are observed.
- Severe gap: 1 severe workflow gap appears, such as repeated wrong invocation, unreviewable output, invalid Quality Bar, missing Anti-Pattern, or unsafe scope expansion.

Reflection must produce:

- signal summary,
- patterns found,
- proposed changes,
- changes explicitly rejected,
- updated thresholds if needed,
- next review trigger.

Use `templates/reflection-report.md` as the default report shape.
</reflection-policy>

<quality-bar>
A successful execution of this sigil must:

- produce or update a self-contained sigil folder when in design or update mode,
- initialize or preserve an experiment harness for reusable sigils,
- treat Codex Goal evidence as SWU execution evidence, not as reusable-behavior validation,
- require experiment harness evidence or a named block before promotion readiness,
- define observability signals for any sigil that will be reused,
- define a post-run JSON hook when usage history is needed for later reflection,
- use an observer subagent or clearly labeled observer pass when generating telemetry or reflection,
- preserve the distinction between usage evidence, observer inference, and applied edits,
- define manual, threshold-based, and gap-based reflection triggers,
- validate markdown links and product-neutral wording before completion,
- return the next lifecycle step for the sigil.
  </quality-bar>

<anti-patterns>
Avoid:

- treating sigil creation as complete when no observability or reflection path exists,
- allowing the observer subagent to edit the sigil without synthesis and review,
- collecting telemetry that cannot inform an iteration decision,
- reflecting on anecdote without usage evidence or an explicit manual trigger,
- changing the core contract of a sigil without naming the evidence that justifies it,
- using thresholds as rigid bureaucracy when a severe gap needs immediate reflection,
- storing vague gap notes that cannot be connected to a Quality Bar, Anti-Pattern, process step, or output contract.
  </anti-patterns>

<output-contract>
Return:

```markdown
## Sigil Development Result

- Target sigil: <name>
- Mode: new | update | observe | reflect
- Tier: formulae | transmutations | arcana
- Files changed: <paths>
- Observer pass: subagent | local fallback | not needed
- Telemetry updated: yes | no | not applicable
- Reflection trigger state: none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap
- Iteration decision: no change | targeted update | reflection required
- Validation: <checks performed>
- Next lifecycle step: <step>
```

</output-contract>

````
