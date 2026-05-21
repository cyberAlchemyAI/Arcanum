---
name: task-session
description: "Use when: executing one bounded task end to end with explicit trade-offs, gate checks, completion criteria, validation, synchronized evidence, and optional runtime-goal delegation."
argument-hint: "<task-reference|to <target>> [--task <TASK-ID>] [--swu <SWU-ID>] [--runtime <id>] [--via goal] [--auto] [--dry-run] [--output <path>]"
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
- validation commands or accepted substitutes.
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
5. Parse the task objective, dependencies, deliverables, write scope, and done criteria.
6. Identify related artifacts that may need synchronization after completion.

## Step 2 - Build Decision Pack

7. Enumerate unresolved task decisions with more than one viable option.
8. For each decision, build option cards with:
   - what the option entails,
   - short-term consequence,
   - long-term consequence,
   - speed impact,
   - complexity impact,
   - risk impact,
   - maintenance impact,
   - recommended option with rationale.
9. Ask the user to choose each blocker decision.
10. If `--auto` is provided, auto-select only decisions that are non-blocking or where a recommendation is clearly safe, and record the auto-selection.

## Step 3 - Evaluate Gates

11. Check task dependencies, stated constraints, required approvals, source links, write scope, and available validation paths.
12. If a blocker exists, return `BLOCK` with exact unblock actions and stop before mutation.
13. If the task can proceed with assumptions, record those assumptions before mutation.

## Step 4 - Select Runtime

14. Resolve the current repository runtime from the installed command context or `--runtime`.
15. If `--via goal` is set, load the matching runtime-goal adapter from `arcana/task-session/runtime-adapters/`.
16. For Codex native Goals, use the `codex-goal` adapter and the `codex-goal-profile` transmutation.
17. If the adapter cannot safely produce a runtime command, return `BLOCK` with the exact missing field or setup action.

## Step 5 - Execute Task

18. Convert selected options and checklist items into an ordered execution path.
19. If a runtime-goal adapter is used, produce or hand off the runtime command and preserve the Task Session synchronization obligations.
20. If running locally, make only the changes required for the task scope.
21. Avoid unrelated refactors or opportunistic cleanup unless they are necessary for completion.

## Step 6 - Validate Completion

22. Validate against every done criterion.
23. Run relevant checks based on touched assets.
24. If a runtime-goal adapter performed execution, review the runtime result against the original work-pack contract.
25. If validation cannot be run, record why and provide the closest useful substitute.
26. If validation fails, attempt bounded recovery when appropriate; otherwise return `FLAG` with required follow-up.

## Step 7 - Synchronize Evidence

27. Update the task record when evidence supports completion.
28. Update related traceability, checklist, registry, or status artifacts only when the task scope requires it.
29. If the task belongs to a spell or sigil lifecycle, preserve experiment harness status and report whether reusable-behavior validation is updated, pending, blocked, or not applicable.
30. If no synchronization is needed, report why.

## Step 8 - Report

31. Return a compact task-session report with decisions, runtime adapter, gate verdict, files updated, validations, experiment harness status, and remaining follow-up.
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
- selected runtime and adapter when used,
- runtime handoff command shape or blocked fallback.
- experiment harness status when the task belongs to spell or sigil lifecycle work.
</observability>

<quality-bar>
A successful execution of this sigil must:

- resolve exactly one task scope,
- resolve exactly one work-pack task or SWU when the input is a work-pack,
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
