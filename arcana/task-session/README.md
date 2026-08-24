# Task Session

Task Session is an Arcana sigil for executing or resuming one bounded task end
to end with explicit decisions, gate checks, completion criteria, validation,
synchronization, and an optional one-hop continuation handoff. Ordered
multi-SWU intent is routed to the `task-session-until-blocker` spell, which
opens a fresh Task Session for each bounded unit.

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
- the requested unit is an ordered stream of SWUs; use
  `task-session-until-blocker` instead.

## Session Loop

1. Detect ordered-series intent before resolving an implementation unit. Route
   it to `task-session-until-blocker` and stop direct execution.
2. Resolve one task scope explicitly or, with no arguments, from the nearest
   evidence-backed current-session continuity source.
3. Parse objective, dependencies, deliverables, and done criteria.
4. Build a bounded context pack from source links, architecture/spec artifacts, constraints, write scope, and validation surface.
5. Complete closeout prerequisite preflight before mutation admission.
6. Build option cards for unresolved implementation choices.
7. Ask the user, or auto-select only an option explicitly classified both
   nonconsequential and reversible.
8. Evaluate blockers, dependency gates, context-pack obligations, write scope, and validation gates.
9. Select the execution runtime for this repository and task.
10. Execute directly or delegate through a runtime handoff adapter.
11. Classify validation obligations, then validate against every done criterion
   and context-pack obligation. Failed or unavailable acceptance-critical
   validation blocks unless a named accepted equivalent passes; only named
   noncritical residue that cannot falsify a done criterion may return `FLAG`.
12. Revalidate the closeout preflight and build a typed closeout-sync record from the terminal receipt, declared
    synchronization targets, baselines, delta classes, and validation.
13. When synchronization is required and deterministic, derive the exact
    closeout-only `invoke:refresh:apply-approved` authorization, dispatch it
    through Continuation Router, and join the owner receipt without asking for
    a second approval.
14. Return the synchronized next route without executing the next task/SWU.
15. Optionally dispatch one separately authorized non-closeout route through
    Continuation Router.
16. Persist a repository-local continuity cursor so a later no-argument call
    can recover the returned route even after conversational context compacts.
17. Return a compact session report with separate execution and closeout
    outcomes.

## Series Intent

Explicit requests such as `--until-blocker`, `all until blocker`, `all SWUs`, or
`one go` do not expand a Task Session beyond one bounded unit. They route to the
installed `task-session-until-blocker` spell. The spell captures the initial
same-work-pack frontier and invokes a distinct Task Session for each eligible
successor:

```text
task-session-until-blocker <work-pack-or-selector>
```

Each inner Task Session retains its own approval, validation, closeout, and
terminal receipt. The spell stops at the first genuine blocker or when the
captured frontier is complete.

## Zero-Argument Resume

Calling Task Session without parameters means `resume-nearest`. It executes at
most one SWU and uses a fixed precedence order:

1. an explicit selector present in visible current-session evidence,
2. the exact current native session cursor, with `--session <id>` available as
   an override,
3. the nearest ancestor `WORK-PACK.md` from the current working directory,
4. one uniquely scope-matched Task Session continuity cursor.

The resolver never uses the globally latest telemetry row, fuzzy relevance, or
unscoped transcript search. If the highest available tier contains multiple
candidates, or if its evidence is stale or contradictory, Task Session blocks
with the ranked candidates instead of switching projects or silently falling
through.

Conversational compaction is handled through durable evidence, not assumed
access to discarded tokens. After closeout, Task Session writes a cursor under
`.arcanum/task-session/continuity/` using the native runtime session id when
available and a stable scope-derived id otherwise. This lets repeated calls in
one work-pack scope update the same cursor rather than accumulating ambiguous
receipt cursors. The cursor records where the session stopped and which route
was returned. It is only a selector: Task Session must re-read the live work
pack and prove that the selected SWU still exists, is incomplete,
dependency-ready, unblocked, and has a declared write scope and validation
surface.

Useful forms:

```text
/task-session
/task-session --list-nearest
/task-session --session <session-id>
/task-session --from path/to/WORK-PACK.md
/task-session --from .arcanum/task-session/continuity/<cursor-id>.json
```

`scripts/resolve-nearest-swu.py` provides the deterministic filesystem portion
of this resolution and emits a machine-readable ranked result.

## Required Closeout Synchronization

Task Session is not closed merely because implementation or validation
finished. When a terminal receipt changes declared task, work-pack, blocker,
route, Dispatch, registry, or Craft projection state, Task Session must
synchronize that state before it returns.

The synchronization still belongs to its lifecycle owner. Task Session creates
one exact, receipt-bound closeout authorization and passes it through
[Continuation Router](../continuation-router/) to
`invoke:refresh:apply-approved`. Invoke validates the source receipt, target
inventory, baselines, typed deltas, and validation commands, performs the
bounded mutation, and returns a separate owner receipt.

This derived authorization admits only evidence, blocker, status, and route
bookkeeping over the declared synchronization inventory. It never authorizes
implementation, another task, authority changes, promotion, publication,
deployment, destructive cleanup, policy/cost/risk acceptance, or unrelated
targets. A successor may be selected only when it is the unique,
already-declared dependency-ready successor, and closeout returns that route
without executing it.

If current artifacts already represent the terminal receipt, closeout records
`no-op`. If the inventory, baselines, validation, unique successor, owner
receipt, or join is missing, the execution result remains preserved but Task
Session closeout returns `BLOCK`.

The same information is a pre-mutation admission prerequisite whenever closeout
synchronization is expected. Task Session must not begin implementation and
discover only afterward that the owner route cannot be joined. The preflight
must bind the terminal source receipt contract, declared target inventory,
baseline state, admitted delta classes, owner validation commands, expected
owner receipt, and any declared successor rule.

## Terminal Continuation Boundary

Task Session still owns exactly one task or SWU. Required closeout
synchronization happens first. When that task then needs a non-closeout owner
route after `BLOCK`, `FLAG`, or a completed handoff, it can pass a normalized
terminal receipt to [Continuation Router](../continuation-router/).

For optional non-closeout continuation, the router exposes one to three
probable routes before dispatch. With `--follow-next-route` and an exact
`--authorize-route <capability>:<mode>[:<mutation-mode>]` grant, it may run one
owner capability and return that owner's separate receipt and next route. It
never recursively resumes Task Session.

For example, contradictory planning state that is not mechanically determined
by the terminal receipt remains optional continuation and can route to
`invoke:refresh`. Task Session preserves its original block, Invoke owns any
approved planning mutation, and the returned Invoke receipt may name a fresh
Task Session SWU. A route string alone never grants apply authority.

The blocker fingerprint prevents a fresh invocation from re-entering the same Task Session gate with unchanged controlling evidence. When evidence changed, a fresh Task Session must still rebuild its context pack.

## Refinement Boundary

Task Session is an executor. It should not run iterative refinement for arbitrary tasks.

Use [refine](../refine/) before Task Session when the user has a vague target, folder, design concern, or architecture question. Refine owns the research offer, loop budget, seed proposal, confirmation gate, and handoff into an execution-ready work-pack task or SWU.

## Context Builder Baseline

For an exact Work-Pack-bound request, Task Session first classifies the
execution entry with `scripts/classify-fast-execution-entry.py`. This boundary
reads only the Work Pack policy, selected unit, current execution binding, and
execution-entry projection. It enters one guard phase and performs no target
mutation. `task-ready` continues to Context Builder. `owner-prerequisite`
returns the exact bound owner packet to Implementation Readiness with
`authorization_prompt_required=false`. Blocked, stale, mismatched, and
selection-only entries stop before Context Builder, deep material inspection,
mutation admission, target hashing/mutation, or owner dispatch.

When the guard returns `TASK_READY`, the deterministic governance runner
accepts a `work-pack-fast-entry` profile containing exact references to both
the guard request and its receipt. The runner revalidates the receipt against
the original four logical inputs and binds the selected unit, Task Session
route, write scope, expected terminal receipt, plan selection, and single-use
admission. This replaces only the legacy prose `selected` row check; every
other context, admission, live-baseline, validation, and closeout gate remains
mandatory. A receipt without its exact request is not execution authority.

Broad lifecycle routes may opt into
`task-session.fast-entry-route-scope-partition.v1`. This additive contract
separates executor write scopes, the exact Task Session terminal receipt, and
typed lifecycle-owner closeout scopes while requiring their disjoint union to
equal the already-bound route. Executor scope still closes exactly against the
mutation admission. Legacy requests without the partition keep the original
two-way route-to-executor closure behavior.

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
/task-session
/task-session to <work-pack-path> [--task <TASK-ID>] [--swu <SWU-ID>] [--runtime <runtime>] [--via runtime]
```

Examples:

```text
/task-session to ./arcana/distill/development/WORK-PACK.md --swu SWU-CLO-003-001 --via runtime
```

## Routed Write Admission

Routed or reusable mutation has one additional gate immediately before the
first write. Task Session creates a machine request binding the live selected
task/SWU, strict controlling artifacts and digests, dependency frontier,
material writes, validation-owned execution outputs, their complete
allowed-write union, validation commands, lifecycle owner, authority class,
and publication class. It consumes the material package and Invoke receipt
through the exact producer-owned receipt schema only when material writes
exist.

The deterministic consumer is
`scripts/verify-mutation-readiness.py`. Its request and receipt contracts are
`schemas/mutation-admission-request.schema.json` and
`schemas/mutation-admission-receipt.schema.json`.

The verifier derives one of two profiles from the normalized write partitions:

- `material-bound`: at least one material write. The Invoke material package,
  receipt, and exact producer-owned receipt schema are mandatory.
- `execution-output-only`: no material writes and at least one declared
  execution output. Material package evidence is forbidden because no material
  change exists to package.

The strict context pack repeats the exact write partitions, validation surface,
lifecycle owner, and authority/publication classes. This prevents a material
target from being relabeled as an execution output to bypass the producer
package. For `material-bound`, the Invoke receipt proves that the package
passed its producer validator, and Task Session recomputes the package binding
against its consumer-owned live controls without copying Invoke validity
logic. Missing evidence, schema failure, drift, task/SWU mismatch, changed
dependencies, expanded writes, context-contract mismatch, validation mismatch,
or absent boundary class blocks before mutation.

An admitted receipt is evidence, not authority. Task Session still performs
the declared live validation after the mutation. Material writes and execution
outputs must be normalized, disjoint, and exactly recompose allowed writes.
The material package and producer receipt cover only material writes.
Validation may create only the predeclared execution outputs; Task Session
verifies all of them and writes its terminal receipt last. Standalone
non-mutating use returns `not-applicable` and does not require an Invoke
receipt.

An admitted `execution-output-only` receipt permits only the declared output
writes and still requires live validation plus post-run write reconciliation.
It grants no material mutation, lifecycle, promotion, publication, deployment,
or release authority. Task Session must never invent a placeholder material
write for an output-only or audit-only task.

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
- closeout-sync source receipt, target inventory, authorization, owner receipt,
  validation, and status,
- follow-up items.
- continuation handoff and blocker fingerprint for terminal results,
- one to three probable routes,
- exact continuation authorization and dispatch status,
- separate owner receipt and returned next route.

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
