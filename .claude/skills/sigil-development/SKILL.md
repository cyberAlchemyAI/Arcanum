---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/sigil-development/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: sigil-development
description: "Use when: creating, revising, observing, reflecting on, or iterating a sigil through the governed sigil lifecycle. Includes subagent-based observability and telemetry generation."
argument-hint: "<sigil-name-or-candidate> [--new | --update | --observe | --reflect] [--threshold <count>]"
tier: arcana
domain: sigil-governance
version: 0.1.0
origin: created to make sigil authoring observable, ready for reflection, and iteratively maintainable
allowed-tools: Read, Write, Glob, Grep, Agent
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
