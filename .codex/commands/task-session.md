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

When the user asks Task Session to execute a work-pack through a goal-like runtime, resolve one task/SWU from the work-pack, check blockers, then use the `codex-goal` adapter to produce or hand off a native Codex `/goal`. Task Session still owns final evidence review and work-pack synchronization.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `task-session`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/task-session/README.md

````markdown
# Task Session

Task Session is an Arcana sigil for executing one bounded task end to end with explicit decisions, gate checks, completion criteria, validation, and synchronization.

It is useful when a task is too consequential for a quick edit but too narrow for a full planning workflow. The sigil keeps the session focused on one task, exposes trade-offs before action, blocks on unresolved gates, and leaves a concise record of what changed and why.

## Problem It Solves

Single-task execution can drift when the agent starts implementing before the task is fully resolved. Dependencies may be missed, options may be chosen silently, and completion criteria may be updated without evidence.

Task Session solves this by turning one task into a guided execution loop: resolve scope, prepare decision options, check gates, perform the work, validate outcomes, and synchronize the task record.

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
3. Build option cards for unresolved implementation choices.
4. Ask the user or auto-select only when explicitly allowed.
5. Evaluate blockers and dependency gates.
6. Execute the chosen path.
7. Validate against done criteria.
8. Synchronize task state and related records.
9. Return a compact session report.

## Output

The sigil produces:

- selected task scope,
- decisions and trade-offs,
- gate verdict,
- files or artifacts updated,
- validation results,
- synchronized completion evidence,
- follow-up items.

## Why This Is Arcana

Task Session coordinates decisions, gates, execution, validation, and state synchronization across a whole task lifecycle. It is more than a checklist: it governs whether the task may proceed, how choices are recorded, and when completion is credible.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/task-session/SKILL.md

````markdown
---
name: task-session
description: "Use when: executing one bounded task end to end with explicit trade-offs, gate checks, completion criteria, validation, and synchronized evidence."
argument-hint: "<task-reference> [--auto] [--dry-run] [--output <path>]"
tier: arcana
domain: guided-execution
version: 0.1.0
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

<flags>
- `--auto`: choose the recommended option for each non-blocking decision and record that it was auto-selected.
- `--dry-run`: return the execution path, decision pack, and gate checks without mutating files.
- `--output <path>`: write the session report to a specific path.
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
- validation commands or accepted substitutes.
</inputs>

<process>
## Step 1 - Resolve Task Scope

1. Resolve exactly one target task from the user input.
2. If multiple tasks are implied, ask the user to choose one or return `BLOCK`.
3. Parse the task objective, dependencies, deliverables, and done criteria.
4. Identify related artifacts that may need synchronization after completion.

## Step 2 - Build Decision Pack

5. Enumerate unresolved task decisions with more than one viable option.
6. For each decision, build option cards with:
   - what the option entails,
   - short-term consequence,
   - long-term consequence,
   - speed impact,
   - complexity impact,
   - risk impact,
   - maintenance impact,
   - recommended option with rationale.
7. Ask the user to choose each blocker decision.
8. If `--auto` is provided, auto-select only decisions that are non-blocking or where a recommendation is clearly safe, and record the auto-selection.

## Step 3 - Evaluate Gates

9. Check task dependencies, stated constraints, required approvals, and available validation paths.
10. If a blocker exists, return `BLOCK` with exact unblock actions and stop before mutation.
11. If the task can proceed with assumptions, record those assumptions before mutation.

## Step 4 - Execute Task

12. Convert selected options and checklist items into an ordered execution path.
13. Make only the changes required for the task scope.
14. Avoid unrelated refactors or opportunistic cleanup unless they are necessary for completion.

## Step 5 - Validate Completion

15. Validate against every done criterion.
16. Run relevant checks based on touched assets.
17. If validation cannot be run, record why and provide the closest useful substitute.
18. If validation fails, attempt bounded recovery when appropriate; otherwise return `FLAG` with required follow-up.

## Step 6 - Synchronize Evidence

19. Update the task record when evidence supports completion.
20. Update related traceability, checklist, registry, or status artifacts only when the task scope requires it.
21. If no synchronization is needed, report why.

## Step 7 - Report

22. Return a compact task-session report with decisions, gate verdict, files updated, validations, and remaining follow-up.
</process>

<authority-rule>
No consequential mutation proceeds when gate status is `BLOCK`. Completion state may only be updated when supporting evidence exists.
</authority-rule>

<observability>
For reusable use, emit a post-run invocation signal using the repository-local observability package when available.

Recommended signals:

- task reference,
- decision count,
- gate result,
- files changed count,
- validation commands,
- validation result,
- completion status,
- follow-up count,
- dry-run or auto mode usage.
</observability>

<quality-bar>
A successful execution of this sigil must:

- resolve exactly one task scope,
- expose meaningful implementation trade-offs,
- stop before mutation when blockers remain,
- keep edits within the declared task scope,
- validate all available done criteria,
- synchronize completion evidence accurately,
- return a report that a reviewer can audit without reconstructing the full session.
</quality-bar>

<anti-patterns>
Avoid:

- using the sigil for many unrelated tasks at once,
- treating `--auto` as permission to guess consequential user choices,
- changing files outside the task scope without recording why,
- marking completion without evidence,
- skipping validation because the edit looks small,
- hiding failed checks inside a success report,
- letting synchronization updates rewrite unrelated planning or status history.
</anti-patterns>

<output-contract>
Return:

```markdown
## Task Session Result

- Task: <task-reference>
- Result: PASS | BLOCK | FLAG
- Decisions: <resolved count and summary>
- Gate verdict: <summary>
- Files updated: <paths or none>
- Validation: <commands and results>
- Synchronized records: <paths or none>
- Follow-up: <items or none>
```
</output-contract>
````
