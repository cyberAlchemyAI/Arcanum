# Task Session Architecture Design

## Invocation

- Spell: `invoke`
- Mode: `design`
- Target artifact: `task-session`
- Target type: sigil architecture design
- Owner/cycle: `arcana/task-session`
- Source contracts:
  - `arcana/task-session/development/TASK-SESSION-DEFINE.md`
  - `arcana/task-session/development/TASK-SESSION-GLOSSARY.md`
  - `arcana/task-session/SKILL.md`
  - `transmutations/context-builder/SKILL.md`
  - `transmutations/codex-goal-profile/SKILL.md`
  - `arcana/task-session/runtime-adapters/codex-goal.md`
  - `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`

## Design Intent

Task Session is the bounded execution coordinator for one work-pack task or SWU. Its architecture should make one thing hard to violate:

> No mutation or runtime delegation happens until task scope, selected context, blockers, write boundaries, and validation evidence are explicit.

The optimized architecture is pack-first:

1. Resolve one task or SWU.
2. Build a task-scoped context pack.
3. Evaluate decisions and gates against that pack.
4. Execute locally or through a runtime adapter.
5. Validate and synchronize evidence.

Context selection happens before execution. Runtime agents should not be responsible for broad discovery except where the context pack names an uncovered obligation or gap.

## Define Alignment

This architecture implements the definition baseline in `TASK-SESSION-DEFINE.md`:

- one selected unit per session,
- context pack before decisions, gates, runtime selection, runtime handoff, or mutation,
- explicit decision and gate discipline,
- runtime delegation through adapter boundaries,
- validation before evidence synchronization,
- no reusable spell/sigil promotion authority.

The glossary in `TASK-SESSION-GLOSSARY.md` controls term usage. In this design, `context pack` is the general selected evidence bundle and `handoff pack` is the runtime-facing form of that bundle: Markdown plus JSON/index, persisted as session evidence, and gated by strict coverage.

## Six-View Architecture

### 1. Context View

Task Session sits between planning artifacts and execution runtimes.

Inputs:

- user command and flags,
- work-pack, task file, or SWU reference,
- task contract and source links,
- dependency and blocker state,
- architecture/spec references,
- write scope,
- done criteria and validation surface,
- optional runtime target such as `codex --via goal`.

Outputs:

- task-session result,
- context pack reference,
- decision records,
- gate verdict,
- files changed,
- validation evidence,
- synchronized task/work-pack records,
- observability signal when available.

Neighbor capabilities:

- `context-builder` selects and packages relevant evidence.
- `decision-gate` resolves blocker-level choices when needed.
- runtime adapters translate a safe task session into runtime-specific execution.
- `codex-goal-profile` turns a selected task/SWU plus context pack into a native Codex Goal profile.
- work-pack artifacts remain the planning source of truth.

### 2. High-Level Structure View

Task Session has six architectural responsibilities:

| Component | Responsibility | Owned By |
| --- | --- | --- |
| Task Resolver | Resolve exactly one task or SWU and parse execution obligations. | Task Session |
| Context Pack Builder | Produce task-ready context and obligation coverage. | Context Builder, orchestrated by Task Session |
| Decision And Gate Engine | Surface trade-offs, stop blockers, and approve assumptions. | Task Session |
| Execution Coordinator | Choose local execution or runtime adapter and preserve scope. | Task Session |
| Runtime Adapter Boundary | Convert safe task sessions into runtime-specific handoffs. | Adapter, selected by Task Session |
| Evidence Synchronizer | Validate, update status, and report audit evidence. | Task Session |

The key architecture boundary is the context pack. Everything after context building should consume it rather than rediscovering source context from scratch.

### 3. Low-Level Components View

#### Task Resolver

Responsibilities:

- parse `to <target>`, `--task`, and `--swu`,
- locate the work-pack or task file,
- ensure exactly one selected execution unit,
- collect parent task, SWU, dependency, blocker, write-scope, and validation fields.

Failure modes:

- no work-pack path,
- multiple candidate tasks,
- selected SWU not present,
- dependency or blocker state cannot be read.

#### Context Pack Builder

Responsibilities:

- call Context Builder in lean or standard mode,
- seed from explicit source links before search,
- map selected snippets to obligations,
- extract architecture guidance, related implementation context, constraints, write scope, validation, and gaps,
- persist a task-scoped handoff pack under session/run evidence when runtime delegation needs a durable handoff.

Pack shape:

- identity,
- obligations,
- selected sources and selectors,
- architecture guidance,
- related feature context,
- constraints and non-goals,
- write scope,
- validation surface,
- gaps and blockers,
- authority precedence,
- fallback exploration rule,
- provenance.

For Codex Goal handoff, the pack must also expose Markdown and JSON/index paths and strict coverage status.

Failure modes:

- missing source links for required obligations,
- contradictory architecture/task/code guidance,
- stale source references,
- pack too broad or noisy,
- unsafe material included.

#### Decision And Gate Engine

Responsibilities:

- derive unresolved choices from the task and context pack,
- ask for blocker decisions or apply safe `--auto` choices,
- evaluate dependencies, blockers, scope, context coverage, write boundaries, and validation availability,
- stop before mutation on `BLOCK`.

Gate classes:

- scope gate,
- dependency gate,
- context coverage gate,
- authority contradiction gate,
- write-scope gate,
- runtime-readiness gate,
- validation gate.

#### Execution Coordinator

Responsibilities:

- convert selected choices and context-pack obligations into an execution path,
- choose local execution or runtime adapter,
- keep edits inside write scope,
- avoid unrelated refactors,
- preserve synchronization obligations even when another runtime performs the implementation.

#### Runtime Adapter Boundary

Responsibilities:

- receive only a safe, gated task session,
- validate adapter-specific readiness,
- produce blocked profile or handoff command,
- pass the session-evidence handoff pack Markdown path and JSON/index path to the runtime,
- pass the handoff pack Markdown path and JSON/index path to the runtime,
- block when strict coverage fails,
- report any extra context used by the runtime.

For Codex Goal:

- `codex-goal-profile` should include the context pack as first-class input.
- broad repository exploration is allowed only for named context gaps.
- goal completion must report validation, changed files, and any extra sources consulted.

#### Evidence Synchronizer

Responsibilities:

- run validation commands or reviewable substitutes,
- compare runtime result against task/SWU contract and context-pack obligations,
- update work-pack/task status only with evidence,
- record skipped validation and residual follow-up,
- emit observability when available.

### 4. Workflow Process View

Normal local execution:

```text
User request
  -> Task Resolver
  -> Context Pack Builder
  -> Decision And Gate Engine
  -> Execution Coordinator
  -> Local Edits
  -> Validation
  -> Evidence Synchronizer
  -> Task Session Result
```

Runtime goal execution:

```text
User request --via goal
  -> Task Resolver
  -> Context Pack Builder
  -> Decision And Gate Engine
  -> Runtime Adapter Boundary
  -> Codex Goal Profile
  -> Native Codex Goal
  -> Runtime Result Review
  -> Validation
  -> Evidence Synchronizer
  -> Task Session Result
```

The same gates apply to both paths. Runtime delegation changes who performs implementation, not who owns task selection, safety gates, or evidence sync.

### 5. Decision Flow View

| Decision | Preferred Rule | Block Condition |
| --- | --- | --- |
| Which task? | Select exactly one explicit task/SWU. | Multiple or missing candidates. |
| How much context? | Standard Context Builder mode by default. | Required obligations uncovered. |
| Can context search expand? | Expand only for uncovered obligations. | Broad search without named gap. |
| Can goal handoff run? | Only with session-evidence handoff pack, JSON/index, and strict coverage pass. | Missing or incomplete pack, failed strict coverage, stale evidence, missing write scope, or missing validation. |
| Can mutation begin? | Only after scope, context, blockers, and validation are known. | Any gate is `BLOCK`. |
| Local or runtime? | Local by default; runtime when requested and adapter is ready. | Runtime selected but adapter lacks required inputs. |
| Can status sync happen? | Sync only after evidence supports completion. | Validation missing/failing without accepted substitute. |

Authority precedence when sources disagree:

1. explicit user instruction in the current session,
2. selected task/SWU contract and blocker state,
3. work-pack and wave/dependency records,
4. architecture/spec/source contracts,
5. current implementation and tests,
6. inferred notes from Context Builder.

Contradictions at the same authority level should become blocker decisions, not silent assumptions.

### 6. Dependency Interface View

#### Task Session -> Context Builder

Input:

- task/SWU identity,
- source links,
- obligations,
- write scope,
- validation surface,
- related architecture/spec artifacts,
- mode and budget.

Output:

- context pack markdown and optional structured index,
- obligation coverage,
- strict coverage status when handoff is requested,
- source selectors,
- uncovered obligations,
- contradictions,
- provenance.

Contract:

- every selected item maps to an obligation,
- broad search only closes uncovered obligations,
- evidence and inference are separated.

#### Task Session -> Runtime Adapter

Input:

- selected task/SWU,
- context pack path or inline pack,
- handoff pack Markdown path and JSON/index path for goal delegation,
- strict coverage status,
- resolved decisions,
- gate verdict,
- write scope,
- done criteria,
- validation surface,
- stop condition.

Output:

- runtime command/profile or blocked profile,
- adapter readiness verdict,
- expected result shape.

Contract:

- adapter cannot override Task Session blockers,
- adapter cannot broaden write scope,
- adapter must preserve context-pack authority.

#### Runtime Adapter -> Codex Goal Profile

Input:

- work-pack path,
- selected unit,
- context pack,
- verification surface,
- constraints,
- boundaries,
- iteration policy,
- blocked stop condition.

Output:

- native Codex Goal objective,
- verification and boundary summary,
- blocked profile when unsafe.

Contract:

- pack-first execution,
- broad exploration only for named gaps,
- final report includes extra sources if any.

#### Task Session -> Work-Pack

Input:

- validation result,
- completion evidence,
- files changed,
- follow-up items.

Output:

- status update,
- evidence link,
- synchronized task or SWU notes.

Contract:

- no completion sync without evidence,
- no unrelated planning rewrite,
- runtime completion is reviewed before status mutation.

## Architecture Decisions

### AD-001: Task Session Owns Coordination, Not Context Selection Logic

Context Builder owns evidence selection and obligation coverage. Task Session owns when Context Builder runs and whether its output is sufficient to proceed.

### AD-002: Context Pack Is The Execution Boundary

The context pack is the shared artifact between planning, gates, and runtime execution. For runtime goal handoff, it becomes a handoff pack persisted as session evidence in Markdown plus JSON/index form.

### AD-003: Runtime Delegation Is Optional And Adapter-Bound

Codex Goal is a runtime option, not Task Session's default execution model. Runtime adapters must consume the same gated task-session state as local execution.

### AD-004: Subagent Is A Strategy, Not A Contract

Context Builder may run as a subagent when available. The contract is the handoff pack, so inline/local execution remains valid.

### AD-005: Completion Requires Evidence Sync

Task Session cannot mark a task or SWU complete merely because implementation ran. Validation and work-pack synchronization remain separate required steps.

## Risks And Controls

| Risk | Control |
| --- | --- |
| Goal runtime wastes budget rediscovering architecture. | Pass the session-evidence handoff pack and JSON/index into goal and restrict broad exploration to named gaps. |
| Context pack becomes stale. | Include timestamp, source refs, and optional hashes/git SHA. |
| Context pack becomes too large. | Use selector-level excerpts and mode budgets. |
| Generated context is mistaken for canonical docs. | Store under session/runtime evidence and label as execution context. |
| Adapter bypasses gates. | Adapter consumes only post-gate task-session state and returns `BLOCK` when fields are missing. |
| Work-pack status drifts from evidence. | Synchronizer updates status only after validation or accepted substitute evidence. |

## Design Gaps

- Contract implementation must keep Context Builder, Task Session, Codex Goal Profile, and the Codex Goal adapter in sync on strict coverage and session-evidence pack paths.
- Task Session observability does not yet distinguish local execution context from runtime handoff context in a structured way.

## Glossary Consistency

Glossary consistency is checked in `TASK-SESSION-GLOSSARY-CONSISTENCY.md`.

Design terms are consistent with the define glossary. The only caution is that implementation plans must preserve the difference between `context pack` and `handoff pack`; using those interchangeably would blur the execution boundary.

## Plan-Ready Handoff

Recommended next route: `invoke plan`.

Plan should create SWUs for:

1. Context Builder handoff pack schema.
2. Context Builder persistence/handoff mode.
3. Task Session context phase update.
4. Codex Goal Profile context-pack input.
5. Codex Goal adapter pack-first enforcement.
6. Observability/reporting updates for context pack provenance and runtime fallback search.
