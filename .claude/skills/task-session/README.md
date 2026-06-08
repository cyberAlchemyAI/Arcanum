# Task Session

Task Session is an Arcana sigil for executing one bounded task end to end with explicit decisions, gate checks, completion criteria, validation, and synchronization.

It is the stable Arcanum execution surface. Runtime-specific systems, including Codex, are treated as adapters rather than as the task-session identity itself.

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
8. Execute directly or delegate through a runtime handoff adapter.
9. Validate against done criteria and context-pack obligations.
10. Synchronize task state and related records.
11. Return a compact session report.

## Refinement Boundary

Task Session is an executor. It should not run iterative refinement for arbitrary tasks.

Use [refine](../refine/) before Task Session when the user has a vague target, folder, design concern, or architecture question. Refine owns the research offer, loop budget, seed proposal, confirmation gate, and handoff into an execution-ready work-pack task or SWU.

## Context Builder Baseline

Task Session must run a context-building pass before decision cards, gate checks, runtime handoff, or mutation. The context pack keeps the selected task/SWU connected to the surrounding architecture, source contracts, work-pack rows, blocker rows, constraints, write scope, validation surface, and local repository conventions.

If required source context is missing, contradictory, or too weak to check the task safely, Task Session returns `BLOCK` with the smallest context gap to resolve. It should not execute from the task file alone when linked architecture or work-pack context can change the correct implementation choice.

For runtime delegation, Task Session requires a handoff pack from Context Builder. The handoff pack must be emitted as Markdown plus JSON/index, persisted under session/run evidence, and pass strict coverage. Strict coverage means every parsed obligation is covered by selected evidence or explicitly resolved before delegation. Missing, contradictory, stale, unsafe, missing write-scope, or missing validation obligations block runtime handoff.

## Work-Pack Runtime Flow

When the input is a `WORK-PACK.md`, Task Session should treat the work-pack as the executable dashboard:

1. Resolve the target work-pack by explicit path or current context.
2. Select exactly one ready task or SWU.
3. Build the bounded context pack from the selected task/SWU, parent task file, source links, related architecture/spec artifacts, dependency rows, blocker rows, write scope, done criteria, and validation surface.
4. If runtime delegation is requested, build a strict handoff pack as session evidence with Markdown plus JSON/index outputs.
5. Check dependencies, blocker rows, source links, context-pack obligations, strict handoff coverage when applicable, write scope, done criteria, and validation surface.
6. Choose the repository runtime from the installed command context or explicit user flag.
7. If the runtime supports durable execution, translate the selected task/SWU through the matching runtime adapter and include the handoff pack path/index in the handoff.
8. Let the runtime own continuation while Task Session remains responsible for final evidence review, fallback-exploration review, and work-pack synchronization.

The intended shorthand is:

```text
/task-session to <work-pack-path> [--task <TASK-ID>] [--swu <SWU-ID>] [--runtime <runtime>] [--via runtime]
```

Examples:

```text
/task-session to ./arcana/distill/development/WORK-PACK.md --swu SWU-CLO-003-001 --via runtime
```

## Runtime Adapter Interface

Task Session supports runtime adapters so the repository can use the best available execution system without hardcoding one vendor or command.

An adapter defines:

- runtime id,
- capability kind, such as `durable-run`,
- availability check,
- input contract from the selected task/SWU,
- transformation rule,
- handoff command shape,
- ownership boundary,
- blocked fallback.

For runtime adapters, the input contract also includes the handoff pack Markdown path, JSON/index path, strict coverage status, and fallback exploration rule. An adapter must block when the handoff pack is absent, incomplete, stale, contradictory, unsafe, missing write scope, missing validation, or below strict coverage.

The current generic adapter is [runtime-adapters/runtime-handoff.md](runtime-adapters/runtime-handoff.md). Legacy native-goal compatibility remains documented under `runtime-adapters/` for old handoffs.

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
runtime: arcanum-runtime | local
adapter: runtime-handoff | none
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
