# Arcanum Sigil: task session

<!-- arcanum:capability-id task-session -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command task-session -->
<!-- arcanum:runtime codex -->
<!-- arcanum:runtime-goal-adapter codex-goal -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-task-session-<UTC timestamp>`.
- `capability.id`: `task-session`
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

Run the installed Arcanum sigil `task-session` using the canonical definition snapshot embedded below.

## Repository Runtime Interface

This installed command runs in the `codex` runtime.

Task Session is the stable Arcanum coordinator. Runtime goal-like execution is delegated through adapters under `arcana/task-session/runtime-adapters/`.

For this repository, the current goal-like adapter is:

- adapter: `codex-goal`
- contract: `arcana/task-session/runtime-adapters/codex-goal.md`
- profile transmutation: `transmutations/codex-goal-profile/`
- native runtime command: `/goal`

When the user asks Task Session to execute a work-pack through a goal-like runtime, resolve one task/SWU from the work-pack, build a bounded context pack with `context-builder`, produce a strict Markdown plus JSON/index handoff pack as session evidence, check blockers and context-pack obligations, then use the `codex-goal` adapter to produce or hand off a native Codex `/goal`. Task Session still owns final evidence review, fallback-exploration review, and work-pack synchronization.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Before decision cards, gate checks, runtime-goal handoff, or mutation, build a bounded context pack from the selected task/SWU, source links, related architecture/spec artifacts, work-pack rows, blocker rows, write scope, done criteria, validation surface, and local repository conventions. For `--via goal`, require a strict handoff pack with Markdown plus JSON/index stored as session evidence.
4. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
5. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `task-session`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/task-session/README.md

````markdown
# Task Session

Task Session is an Arcana sigil for executing one bounded task end to end with explicit decisions, gate checks, completion criteria, validation, and synchronization.

It is the stable Arcanum execution surface. Runtime-specific goal systems, such as Codex native `/goal`, are treated as adapters rather than as the task-session identity itself.

It is useful when a task is too consequential for a quick edit but too narrow for a full planning workflow. The sigil keeps the session focused on one task, exposes trade-offs before action, blocks on unresolved gates, and leaves a concise record of what changed and why.

## Problem It Solves

Single-task execution can drift when the agent starts implementing before the task is fully resolved. Dependencies may be missed, options may be chosen silently, and completion criteria may be updated without evidence.

Task Session solves this by turning one task into a guided execution loop: resolve scope, build a bounded context pack, prepare decision options, check gates, perform the work, validate outcomes, and synchronize the task record.

Refinement, discovery, and multi-pass planning should happen before Task Session. Use [refine](../refine/) when the target still needs a refinement seed, research decision, loop budget, or design/plan shaping before execution.

## Use When

- there is one explicit task to execute,
- the task has dependencies, trade-offs, or validation requirements,
- the user wants focused progress without opening a broad planning cycle,
- completion needs evidence rather than a verbal claim,
- task records or traceability artifacts should be kept current.

## Do Not Use When

- the task is trivial and reversible,
- the work is undefined or spans many independent tasks,
- unresolved blocker decisions should be handled by [decision-gate](../decision-gate/),
- the task belongs to an existing project-specific execution workflow,
- validation cannot be run or meaningfully substituted.

## Session Loop

1. Resolve one task scope.
2. Parse objective, dependencies, deliverables, and done criteria.
3. Build a bounded context pack from source links, architecture/spec artifacts, constraints, write scope, and validation surface.
4. Build option cards for unresolved implementation choices.
5. Ask the user or auto-select only when explicitly allowed.
6. Evaluate blockers, dependency gates, context-pack obligations, write scope, and validation gates.
7. Select the execution runtime for this repository and task.
8. Execute directly or delegate through a runtime-goal adapter.
9. Validate against done criteria and context-pack obligations.
10. Synchronize task state and related records.
11. Return a compact session report.

## Refinement Boundary

Task Session is an executor. It should not run iterative refinement for arbitrary tasks.

Use [refine](../refine/) before Task Session when the user has a vague target, folder, design concern, or architecture question. Refine owns the research offer, loop budget, seed proposal, confirmation gate, and handoff into an execution-ready work-pack task or SWU.

## Context Builder Baseline

Task Session must run a context-building pass before decision cards, gate checks, runtime-goal handoff, or mutation. The context pack keeps the selected task/SWU connected to the surrounding architecture, source contracts, work-pack rows, blocker rows, constraints, write scope, validation surface, and local repository conventions.

If required source context is missing, contradictory, or too weak to check the task safely, Task Session returns `BLOCK` with the smallest context gap to resolve. It should not execute from the task file alone when linked architecture or work-pack context can change the correct implementation choice.

For runtime-goal delegation, Task Session requires a handoff pack from Context Builder. The handoff pack must be emitted as Markdown plus JSON/index, persisted under session/run evidence, and pass strict coverage. Strict coverage means every parsed obligation is covered by selected evidence or explicitly resolved before delegation. Missing, contradictory, stale, unsafe, missing write-scope, or missing validation obligations block goal handoff.

## Work-Pack Runtime Flow

When the input is a `WORK-PACK.md`, Task Session should treat the work-pack as the executable dashboard:

1. Resolve the target work-pack by explicit path or current context.
2. Select exactly one ready task or SWU.
3. Build the bounded context pack from the selected task/SWU, parent task file, source links, related architecture/spec artifacts, dependency rows, blocker rows, write scope, done criteria, and validation surface.
4. If `--via goal` is requested, build a strict handoff pack as session evidence with Markdown plus JSON/index outputs.
5. Check dependencies, blocker rows, source links, context-pack obligations, strict handoff coverage when applicable, write scope, done criteria, and validation surface.
6. Choose the repository runtime from the installed command context or explicit user flag.
7. If the runtime supports goal-like execution, translate the selected task/SWU through the matching runtime-goal adapter and include the handoff pack path/index in the handoff.
8. Let the runtime own continuation while Task Session remains responsible for final evidence review, fallback-exploration review, and work-pack synchronization.

The intended shorthand is:

```text
/task-session to <work-pack-path> [--task <TASK-ID>] [--swu <SWU-ID>] [--runtime <runtime>] [--via goal]
```

Examples:

```text
/task-session to ./arcana/distill/development/WORK-PACK.md --swu SWU-CLO-003-001 --via goal
```

## Runtime Adapter Interface

Task Session supports runtime adapters so the repository can use the best available execution system without hardcoding one vendor or command.

An adapter defines:

- runtime id,
- capability kind, such as `goal`,
- availability check,
- input contract from the selected task/SWU,
- transformation rule,
- handoff command shape,
- ownership boundary,
- blocked fallback.

For goal-like adapters, the input contract also includes the handoff pack Markdown path, JSON/index path, strict coverage status, and fallback exploration rule. An adapter must block when the handoff pack is absent, incomplete, stale, contradictory, unsafe, missing write scope, missing validation, or below strict coverage.

The current Codex adapter is [runtime-adapters/codex-goal.md](runtime-adapters/codex-goal.md). It uses [Codex Goal Profile](../../transmutations/codex-goal-profile/) to turn one work-pack task or SWU into a native Codex `/goal` command.

## Output

The sigil produces:

- selected task scope,
- bounded context pack summary,
- decisions and trade-offs,
- gate verdict,
- files or artifacts updated,
- validation results,
- synchronized completion evidence,
- follow-up items.

For runtime-backed execution, the report also includes:

- selected runtime,
- adapter used,
- handoff pack Markdown and JSON/index paths,
- strict coverage status,
- fallback exploration/search status,
- generated runtime command or blocked reason,
- runtime-owned lifecycle actions,
- synchronization required after runtime completion.

## Lifecycle Closure Evidence

When Task Session executes a work-pack task or SWU for a spell or sigil lifecycle, it should return evidence that lifecycle owners and Experiment Harness can consume:

```yaml
runtime: codex | local
adapter: codex-goal | none
source_swu: <id or none>
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

Task Session may complete an execution unit, but it does not decide reusable spell or sigil promotion. That decision belongs to Spellcraft or Sigil Development after Experiment Harness evidence is reviewed.

## Why This Is Arcana

Task Session coordinates decisions, gates, execution, validation, and state synchronization across a whole task lifecycle. It is more than a checklist: it governs whether the task may proceed, how choices are recorded, and when completion is credible.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/task-session/SKILL.md

````markdown
---
name: task-session
description: "Use when: executing one bounded work-pack task or SWU end to end with explicit trade-offs, context building, gate checks, completion criteria, validation, synchronized evidence, and optional runtime-goal delegation."
argument-hint: "<task-reference|to <target>> [--task <TASK-ID>] [--swu <SWU-ID>] [--runtime <id>] [--via goal] [--auto] [--dry-run] [--output <path>]"
tier: arcana
domain: guided-execution
version: 0.3.0
origin: generalized from recurring single-task execution governance practice
allowed-tools: Read, Write, Glob, Grep, AskQuestions, Task, Bash
---

# Sigil: Task Session

<objective>
Execute one bounded task end to end while making trade-offs explicit, enforcing blockers, validating completion, and synchronizing task evidence.
</objective>

<logic-type>
Arcana: guided execution loop with human decision points, hard gates, and completion evidence.
</logic-type>

<required-sigils>

| Sigil | Role In Task Session | Required Mode |
| --- | --- | --- |
| `context-builder` | Build a bounded context pack from the selected task/SWU, source links, constraints, related architecture/spec artifacts, write scope, and validation surface before decisions, gates, or runtime handoff. For `--via goal`, produce a strict Markdown plus JSON/index handoff pack stored as session evidence. | lean or standard |

</required-sigils>

<flags>
- `--auto`: choose the recommended option for each non-blocking decision and record that it was auto-selected.
- `--dry-run`: return the execution path, decision pack, and gate checks without mutating files.
- `--output <path>`: write the session report to a specific path.
- `to <target>`: resolve a work-pack target by explicit path or current context.
- `--task <TASK-ID>`: select one task from a work-pack.
- `--swu <SWU-ID>`: select one Smallest Working Unit from a work-pack.
- `--runtime <id>`: choose the execution runtime adapter, such as `codex`.
- `--via goal`: delegate through the selected runtime's goal-like execution adapter when available.
</flags>

<applicability>
Use this sigil when:

- there is one explicit task to execute,
- the task has dependencies, deliverables, or done criteria,
- implementation choices need visible trade-offs,
- gate failures must stop mutation,
- the task record should be synchronized with evidence after completion.
</applicability>

<inputs>
Expected inputs, if available:

- explicit task reference or task file,
- task objective,
- dependency list,
- implementation checklist,
- deliverables,
- done criteria,
- relevant constraints,
- validation commands or accepted substitutes,
- optional `WORK-PACK.md` with task board, SWU manifest, waves, and task contracts,
- optional runtime adapter selection from the installed repository command context.
- optional lifecycle owner and experiment harness path when executing spell or sigil development work.
</inputs>

<process>
## Step 1 - Resolve Task Scope

1. Resolve exactly one target task from the user input.
2. If the input is `to <target>`, resolve the target to an explicit work-pack path or current-context work-pack; otherwise return `BLOCK` with the missing work-pack path.
3. If a work-pack is provided, select exactly one ready task or SWU using `--task`, `--swu`, or the next ready unit.
4. If multiple tasks are implied, ask the user to choose one or return `BLOCK`.
5. Parse the task objective, dependencies, deliverables, write scope, done criteria, and validation surface.
6. Identify related artifacts that may need synchronization after completion.

## Step 2 - Build Context Pack

10. Run `context-builder` in lean or standard mode for the selected task/SWU.
11. Include the task contract, source links, architecture/spec references, work-pack row, dependency rows, blocker rows, write scope, done criteria, validation surface, and known repository conventions.
12. When `--via goal` is set, request a `codex-goal` handoff pack from Context Builder, emitted as Markdown plus JSON/index and persisted under session/run evidence.
13. Extract hard constraints and cross-artifact obligations from the context pack before selecting an implementation path.
14. If linked context is missing, contradictory, stale, unsafe, too weak, missing write scope, missing validation, or lacks strict coverage for a runtime handoff, return `BLOCK` with the missing context or contradiction and stop before mutation.
15. Record the context pack summary, handoff artifact paths, strict coverage status, and the source artifacts that controlled execution.

## Step 3 - Build Decision Pack

16. Enumerate unresolved task decisions with more than one viable option.
17. For each decision, build option cards with:
   - what the option entails,
   - short-term consequence,
   - long-term consequence,
   - speed impact,
   - complexity impact,
   - risk impact,
   - maintenance impact,
   - recommended option with rationale.
19. Ask the user to choose each blocker decision.
20. If `--auto` is provided, auto-select only decisions that are non-blocking or where a recommendation is clearly safe, and record the auto-selection.

## Step 4 - Evaluate Gates

21. Check task dependencies, stated constraints, required approvals, source links, context-pack obligations, strict handoff coverage when applicable, write scope, and available validation paths.
22. If a blocker exists, return `BLOCK` with exact unblock actions and stop before mutation.
23. If the task can proceed with assumptions, record those assumptions before mutation.

## Step 5 - Select Runtime

24. Resolve the current repository runtime from the installed command context or `--runtime`.
25. If `--via goal` is set, load the matching runtime-goal adapter from `arcana/task-session/runtime-adapters/`.
26. For Codex native Goals, use the `codex-goal` adapter and the `codex-goal-profile` transmutation.
27. If `--via goal` is set and the session lacks a complete session-evidence handoff pack with Markdown plus JSON/index and strict coverage, return `BLOCK`.
28. If the adapter cannot safely produce a runtime command, return `BLOCK` with the exact missing field or setup action.

## Step 6 - Execute Task

30. Convert selected options, context-pack obligations, and checklist items into an ordered execution path.
31. If a runtime-goal adapter is used, pass the handoff pack Markdown path and JSON/index path to the runtime command and preserve the Task Session synchronization obligations.
32. If running locally, make only the changes required for the task scope.
33. Avoid unrelated refactors or opportunistic cleanup unless they are necessary for completion.

## Step 7 - Validate Completion

35. Validate against every done criterion and context-pack obligation.
36. Run relevant checks based on touched assets.
37. If a runtime-goal adapter performed execution, review the runtime result against the original work-pack contract, context pack, handoff pack/index, and any reported fallback exploration.
38. If validation cannot be run, record why and provide the closest useful substitute.
39. If validation fails, attempt bounded recovery when appropriate; otherwise return `FLAG` with required follow-up.

## Step 8 - Synchronize Evidence

40. Update the task record when evidence supports completion.
41. Update related traceability, checklist, registry, or status artifacts only when the task scope requires it.
42. If the task belongs to a spell or sigil lifecycle, preserve experiment harness status and report whether reusable-behavior validation is updated, pending, blocked, or not applicable.
43. If no synchronization is needed, report why.

## Step 9 - Report

44. Return a compact task-session report with context pack, handoff pack artifact, strict coverage, fallback-search status, decisions, runtime adapter, gate verdict, files updated, validations, experiment harness status, and remaining follow-up.
</process>

<authority-rule>
No consequential mutation proceeds when gate status is `BLOCK`. Completion state may only be updated when supporting evidence exists.
</authority-rule>

<observability>
For reusable use, emit a post-run invocation signal using the repository-local observability package when available.

Recommended signals:

- task reference,
- context pack status and source count,
- handoff pack markdown and JSON/index paths when runtime delegation is used,
- strict coverage status,
- fallback exploration/search status,
- decision count,
- gate result,
- files changed count,
- validation commands,
- validation result,
- completion status,
- follow-up count,
- dry-run or auto mode usage.
- selected runtime and adapter when used,
- runtime handoff command shape or blocked fallback.
- experiment harness status when the task belongs to spell or sigil lifecycle work.
</observability>

<quality-bar>
A successful execution of this sigil must:

- resolve exactly one task scope,
- resolve exactly one work-pack task or SWU when the input is a work-pack,
- build a bounded context pack before decisions, gates, runtime selection, or mutation,
- require strict handoff-pack coverage before `--via goal` delegation,
- block when required source context is missing, contradictory, or too weak to check constraints,
- expose meaningful implementation trade-offs,
- stop before mutation when blockers remain,
- keep runtime-goal delegation behind an explicit adapter boundary,
- keep edits within the declared task scope,
- validate all available done criteria,
- distinguish task/SWU execution evidence from reusable-behavior experiment evidence,
- synchronize completion evidence accurately,
- return a report that a reviewer can audit without reconstructing the full session.
</quality-bar>

<anti-patterns>
Avoid:

- using the sigil for many unrelated tasks at once,
- executing from the task file alone when source links, architecture, or work-pack context can change the correct implementation choice,
- delegating through `--via goal` without a complete session-evidence handoff pack and JSON/index,
- treating `--auto` as permission to guess consequential user choices,
- changing files outside the task scope without recording why,
- marking completion without evidence,
- skipping validation because the edit looks small,
- hiding failed checks inside a success report,
- letting synchronization updates rewrite unrelated planning or status history.
- hardcoding Codex `/goal` as the only possible runtime,
- treating a generated runtime goal as completed work before evidence returns.
</anti-patterns>

<output-contract>
Return:

```markdown
## Task Session Result

- Task: <task-reference>
- Result: PASS | BLOCK | FLAG
- Decisions: <resolved count and summary>
- Context pack: <source count and controlling constraints | blocked reason>
- Handoff pack: <markdown path and JSON/index path | none | blocked reason>
- Strict coverage: pass | block | n/a
- Fallback search: none | named gaps only | blocked
- Runtime: <runtime id or local>
- Adapter: <adapter id or none>
- Gate verdict: <summary>
- Files updated: <paths or none>
- Validation: <commands and results>
- Experiment harness: pass | flag | block | not_run | not_applicable
- Synchronized records: <paths or none>
- Follow-up: <items or none>
```
</output-contract>
````
