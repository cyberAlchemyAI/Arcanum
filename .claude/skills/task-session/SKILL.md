---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/task-session/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: task-session
description: "Use when: executing one bounded work-pack task or SWU end to end with explicit trade-offs, context building, gate checks, completion criteria, validation, synchronized evidence, and optional runtime handoff delegation."
argument-hint: "<task-reference|to <target>> [--task <TASK-ID>] [--swu <SWU-ID>] [--runtime <id>] [--via runtime] [--auto] [--dry-run] [--output <path>]"
tier: arcana
domain: guided-execution
version: 0.3.1
origin: generalized from recurring single-task execution governance practice
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Agent, Bash
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
| `context-builder` | Build a bounded context pack from the selected task/SWU, source links, constraints, related architecture/spec artifacts, write scope, and validation surface before decisions, gates, or runtime handoff. For `--via runtime`, produce a strict Markdown plus JSON/index handoff pack stored as session evidence. | lean or standard |
| `decision-gate` | Convert unresolved blocker-level choices into user-ready option cards with context, trade-offs, recommendation, and a durable decision record before returning `BLOCK`. | blocker-only |

</required-sigils>

<flags>
- `--auto`: choose the recommended option for each non-blocking decision and record that it was auto-selected.
- `--dry-run`: return the execution path, decision pack, and gate checks without mutating files.
- `--output <path>`: write the session report to a specific path.
- `to <target>`: resolve a work-pack target by explicit path or current context.
- `--task <TASK-ID>`: select one task from a work-pack.
- `--swu <SWU-ID>`: select one Smallest Working Unit from a work-pack.
- `--runtime <id>`: choose the execution runtime adapter, such as `codex`.
- `--via runtime`: delegate through the selected runtime adapter when available.
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
12. When `--via runtime` is set, request a runtime handoff pack from Context Builder, emitted as Markdown plus JSON/index and persisted under session/run evidence.
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
18. Classify each decision as blocker, deferrable, or assumption.
19. Ask the user to choose each blocker decision when the blocker is discovered before mutation.
20. If `--auto` is provided, auto-select only decisions that are non-blocking or where a recommendation is clearly safe, and record the auto-selection.
21. If a blocker-level decision remains unresolved and consequential work cannot proceed, invoke `decision-gate` before returning `BLOCK`; include the exact context, option cards, recommendation, and decision artifact path in the task-session report.

## Step 4 - Evaluate Gates

22. Check task dependencies, stated constraints, required approvals, source links, context-pack obligations, strict handoff coverage when applicable, write scope, and available validation paths.
23. If a blocker exists because a human approval, policy choice, destructive cleanup, irreversible mutation, cost/risk acceptance, or rollout option is unresolved, run `decision-gate` for that blocker before returning `BLOCK`.
24. If a blocker exists for missing evidence, missing files, unavailable tools, or contradictory context with no meaningful user option, return `BLOCK` with exact unblock actions and stop before mutation.
25. If the task can proceed with assumptions, record those assumptions before mutation.

## Step 5 - Select Runtime

26. Resolve the current repository runtime from the installed command context or `--runtime`.
27. If `--via runtime` is set, load the matching runtime adapter from `arcana/task-session/runtime-adapters/`.
28. For durable Arcanum runtime runs, use the `runtime-handoff` adapter and selected executor adapter such as `native-skill`, `codex-skill`, `claude-skill`, `copilot-instructions`, `dry-run`, or explicit legacy `codex-exec`.
29. If `--via runtime` is set and the session lacks a complete session-evidence handoff pack with Markdown plus JSON/index and strict coverage, return `BLOCK`.
30. If the adapter cannot safely produce a runtime command, return `BLOCK` with the exact missing field or setup action.

## Step 6 - Execute Task

31. Convert selected options, context-pack obligations, and checklist items into an ordered execution path.
32. If a runtime adapter is used, pass the handoff pack Markdown path and JSON/index path to the runtime handoff and preserve the Task Session synchronization obligations.
33. If running locally, make only the changes required for the task scope.
34. Avoid unrelated refactors or opportunistic cleanup unless they are necessary for completion.

## Step 7 - Validate Completion

35. Validate against every done criterion and context-pack obligation.
36. Run relevant checks based on touched assets.
37. If a runtime adapter performed execution, review the runtime result against the original work-pack contract, context pack, handoff pack/index, and any reported fallback exploration.
38. If the task-session route spawned, inherited, or requested subagents, verify the subagent lifecycle ledger before reporting success: every agent must be joined, closed, blocked with residue, timed out with residue and reroute, or handed off with reroute.
39. Treat hidden open agents, pending joins, pending closes, and unreported thread-cap failures as `BLOCK`, not as successful fallback exploration.
40. If validation cannot be run, record why and provide the closest useful substitute.
41. If validation fails, attempt bounded recovery when appropriate; otherwise return `FLAG` with required follow-up.

## Step 8 - Synchronize Evidence

42. Update the task record when evidence supports completion.
43. Update related traceability, checklist, registry, or status artifacts only when the task scope requires it.
44. If the task belongs to a spell or sigil lifecycle, preserve experiment harness status and report whether reusable-behavior validation is updated, pending, blocked, or not applicable.
45. If no synchronization is needed, report why.

## Step 9 - Report

46. Return a compact task-session report with context pack, handoff pack artifact, strict coverage, fallback-search status, decisions, runtime adapter, gate verdict, subagent closeout, files updated, validations, experiment harness status, and remaining follow-up.
47. Report subagent closeout as `n/a`, `pass`, `flag`, or `block`; when it is not `n/a`, include counts for spawned, joined, closed, blocked, timed-out, handed-off, open, plus residue and reroute paths.
48. When the result is `BLOCK` because a decision is required, append a `Decision Gate Result` section that names the target scope, lists the blocker question, presents 2-4 concrete options with trade-offs, records the recommended option if one exists, and points to the decision artifact path.
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
- subagent closeout result and unresolved agent count when delegated execution is present,
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
- require strict handoff-pack coverage before `--via runtime` delegation,
- block when required source context is missing, contradictory, or too weak to check constraints,
- expose meaningful implementation trade-offs,
- stop before mutation when blockers remain,
- run `decision-gate` before reporting blocker-level human approval, destructive cleanup, rollout, or policy choices,
- keep runtime delegation behind an explicit adapter boundary,
- block success when delegated subagents remain open, pending, hidden, or only implicitly abandoned,
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
- delegating through `--via runtime` without a complete session-evidence handoff pack and JSON/index,
- treating `--auto` as permission to guess consequential user choices,
- changing files outside the task scope without recording why,
- marking completion without evidence,
- skipping validation because the edit looks small,
- hiding failed checks inside a success report,
- letting synchronization updates rewrite unrelated planning or status history.
- ending with a vague approval request when a blocker-level decision could be presented as concrete options with context.
- hardcoding Codex as the only possible runtime,
- treating a generated runtime handoff as completed work before evidence returns.
- reporting AFK research as successful while subagent joins, closes, residues, or reroutes are unproven.
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
- Subagent closeout: n/a | pass | flag | block, <spawned/joined/closed/blocked/timed_out/handed_off/open counts, residue, reroute>
- Files updated: <paths or none>
- Validation: <commands and results>
- Experiment harness: pass | flag | block | not_run | not_applicable
- Synchronized records: <paths or none>
- Follow-up: <items or none>

## Decision Gate Result

- Target scope: <scope | n/a>
- Result: PASS | BLOCK | n/a
- Decisions resolved: <count>
- Blockers remaining: <count>
- Decision artifact: <path | none>
- Options: <numbered option cards with benefit, cost/risk, when to choose, downstream impact | none>
- Recommendation: <recommended option and rationale | none>
- Next step: <proceed | ask remaining decision | stop>
```
</output-contract>
