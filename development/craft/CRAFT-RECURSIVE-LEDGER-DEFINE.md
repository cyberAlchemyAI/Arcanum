# Craft Recursive Ledger Define

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: Craft development package
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `development/craft/CRAFT-RECURSIVE-LEDGER-DEFINE.md`, `development/craft/CRAFT-RECURSIVE-LEDGER-GLOSSARY.md`
- Template selection: generic define artifact
- Decisions: define the MVP as a recursive operational ledger for contexts/projects; defer scoring and automation
- Unresolved gaps: persistence format, exact relation schema, UI/runtime surface, priority scoring model, role mapping validation
- Next route: design

## Objective

Define the MVP for Craft's first operational capability: a recursive ledger that tracks many development contexts, their artifacts, their own development cycles, and their blocker/enabler relationships across nested and sibling contexts.

The ledger exists because a normal work-pack is useful as a task ledger, but it is not enough when the work itself contains contexts inside contexts. Craft needs an operational memory surface where each context can act like a project with its own artifacts, cycles, decisions, blockers, enablers, and child contexts.

## Intent Record

The user wants to start Craft's operational development with a ledger rather than with the full philosophical method.

Core intent:

```text
I have many different contexts. Each context can have its own development cycle and artifacts.
Work-pack behaves like a ledger, but it is not enough.
Start Craft by building the operational recursive ledger.
The ledger should support projects inside projects, and blockers/enablers between them.
Later it can add scoring to decide priorities.
It should eventually support cross-project blockers and enablers.
```

## MVP Definition

The MVP is a file-backed recursive ledger for Craft contexts.

A Craft context is any bounded development space that has:

- an identity,
- a purpose,
- a lifecycle status,
- owned artifacts,
- open decisions or gaps,
- blockers,
- enablers,
- parent/child relationships,
- cross-context relationships,
- a next responsible move.

The recursive ledger is the coordinating surface that lets one context contain other contexts while still allowing relationships across branches.

## Scope

In scope for MVP:

- define a canonical ledger shape for Craft contexts,
- support parent/child context nesting,
- support sibling or cross-project blocker/enabler relationships,
- record artifacts owned by each context,
- record each context's development cycle state,
- record next moves and gate status,
- keep enough structure for later scoring without implementing scoring,
- remain local and reviewable inside `development/craft/`.

Out of scope for MVP:

- automated priority scoring,
- UI,
- database persistence,
- runtime command integration,
- canonical Arcanum registry mutation,
- cross-repository synchronization,
- automatic task execution,
- replacing existing work-packs or task-session.

Target operator:

- a human or agent managing multiple nested Craft development contexts inside one repository.

## Source Evidence

| Evidence ID | Source | Relevance |
| --- | --- | --- |
| E-001 | User request, 2026-05-26 | Defines the MVP as a recursive ledger for contexts with nested projects, blockers, enablers, and future scoring. |
| E-002 | [DURABLE-SESSION-CONTEXT.md](DURABLE-SESSION-CONTEXT.md) | Establishes Craft as candidate method work under `development/craft/` and prohibits canonical mutation during this phase. |
| E-003 | [CRAFT-INITIAL-DEFINITION.md](CRAFT-INITIAL-DEFINITION.md) | Defines Craft around schema/data translation, SCU/SWU selection, residue handling, validation, reflection, and recomposition. |
| E-004 | `spells/invoke/define.md` | Define mode requires a governed baseline with decisions, evidence, gaps, and next route. |
| E-005 | `spells/invoke/templates/work-pack.md` | Work-pack already models tasks, blockers, gates, and SWUs, but it is task-execution oriented rather than recursive context oriented. |

## Specialized Family Eligibility

| Family | Eligible | Rationale |
| --- | --- | --- |
| research | no | The user supplied a concrete operational direction; external research is not needed for the define baseline. |
| architecture | partial | Architecture is the next route after the MVP definition stabilizes. |
| implementation-plan | partial | A work-pack should follow, but the ledger shape needs one definition pass first. |
| spell | no | This is not yet a reusable spell composition. |
| sigil | no | This is not yet an approved sigil lifecycle mutation. |
| ux-plan | no | UI is explicitly out of MVP scope. |

## Core Model

The recursive ledger should model five things:

1. Contexts
2. Artifacts
3. Lifecycle states
4. Relationships
5. Gates
6. Typed blockers, gates, and enablers

### Context

A context is a recursive project-like unit.

Examples:

- Craft itself,
- Craft recursive ledger MVP,
- a future scoring model,
- a child experiment under a larger method,
- a project inside a project,
- a work-pack-like execution context.

### Artifact

An artifact is any file, output, decision record, work-pack, design, validation result, or handoff owned by a context.

### Lifecycle State

Each context should name its own development stage. Initial MVP stages:

| State | Meaning |
| --- | --- |
| `idea` | Context exists as a rough intent. |
| `define` | Context is being clarified into a baseline. |
| `design` | Structure and relationships are being chosen. |
| `plan` | Work is being decomposed into executable units. |
| `execute` | Artifacts are being produced. |
| `validate` | Outputs are checked against the context schema. |
| `reflect` | Lessons, residue, and next-layer needs are recorded. |
| `blocked` | A dependency, decision, missing artifact, or contradiction prevents progress. |
| `closed` | Context has no current next move. |

### Relationship

Relationships connect contexts and artifacts.

MVP relationship types:

| Type | Meaning |
| --- | --- |
| `contains` | Parent context contains child context. |
| `blocks` | Source context or artifact prevents target progress. |
| `enables` | Source context or artifact makes target progress possible. |
| `depends_on` | Target requires source to be stable or accepted. |
| `informs` | Source provides context but does not gate progress. |
| `supersedes` | Source replaces or obsoletes target. |

### Gate

A gate is the current pass/flag/block state for a context.

Initial gate values:

| Gate | Meaning |
| --- | --- |
| `pass` | Context can proceed to the next responsible move. |
| `flag` | Context can proceed, but named gaps remain. |
| `block` | Context cannot proceed until a blocker is resolved. |

## Candidate Ledger Shape

The MVP can begin as Markdown plus optional JSON index. Markdown is the human coordination surface; JSON becomes useful when scoring, validation, or visualization appears later.

Minimum context row:

| Field | Purpose |
| --- | --- |
| `context_id` | Stable local identifier. |
| `parent_id` | Parent context, or `root`. |
| `title` | Human-readable name. |
| `purpose` | Why this context exists. |
| `stage` | Current lifecycle state. |
| `gate` | pass, flag, or block. |
| `owned_artifacts` | Files or outputs owned by this context. |
| `next_move` | Next responsible action. |
| `blockers` | Blocking context/artifact/relation IDs. |
| `enablers` | Enabling context/artifact/relation IDs. |
| `notes` | Short context-specific residue or decision note. |

Minimum relationship row:

| Field | Purpose |
| --- | --- |
| `relation_id` | Stable local identifier. |
| `source_id` | Source context or artifact. |
| `target_id` | Target context or artifact. |
| `type` | contains, blocks, enables, depends_on, informs, or supersedes. |
| `status` | active, proposed, resolved, rejected. |
| `reason` | Why the relation exists. |
| `evidence` | Source file, section, decision, or validation result. |

## MVP Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| The ledger can represent a root Craft context and at least one child operational context. | Example rows in the next design/work-pack artifact. |
| A child context can have its own stage, artifacts, gate, and next move. | Ledger schema includes lifecycle and artifact fields per context. |
| A context can block or enable another context outside its parent branch. | Relationship schema supports source/target IDs independent of nesting. |
| Priority scoring is deferred without closing the design path. | Scoring is listed as future extension and fields leave room for later metrics. |
| Work-pack remains an execution ledger, not the whole recursive context ledger. | Boundary rule recorded in this define artifact. |
| Canonical Arcanum mutation remains out of scope. | Scope and guardrail sections preserve the durable session boundary. |

## Open Gaps

| Gap ID | Description | Severity | Next Action |
| --- | --- | --- | --- |
| G-001 | Exact persistence format is not decided: Markdown-only, JSON-only, or paired Markdown/JSON. | medium | Decide during architecture/design. |
| G-002 | Relationship semantics need validation against real Craft examples. | medium | Create example ledger with nested and cross-context blockers. |
| G-003 | Priority scoring is desired later but not defined. | low | Defer until blocker/enabler model is stable. |
| G-004 | No command/runtime integration exists. | low | Defer until file-backed MVP is useful. |
| G-005 | No migration rule from existing work-packs to ledger contexts. | medium | Define conversion rules after MVP schema. |
| G-006 | Type-to-role mapping is only a candidate model. | medium | Validate base and context-specific types against example ledger rows before delegation. |

## Typed Blockers, Gates, And Enablers

The recursive ledger should classify blockers, gates, and enablers by type.

Type classification has two purposes:

1. make ledger entries more precise than `blocked` or `enabled`,
2. preserve a future delegation path where a type can imply a responsible role.

See [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) for the candidate base types, context-specific type pattern, role mapping fields, and validation rules.

## Boundary With Work-Pack

Work-pack is task-execution oriented. It answers:

```text
What executable work units are ready, blocked, or done?
```

Craft recursive ledger is context-orchestration oriented. It answers:

```text
What contexts exist, how do they nest, what artifacts do they own,
and how do they block or enable each other?
```

A work-pack can be an artifact owned by a context. It should not be forced to become the whole recursive context model.

## Future Extension: Scoring

Scoring is explicitly deferred.

Future scoring may use:

- number and severity of blockers,
- number and strength of enablers,
- depth in the context tree,
- artifact readiness,
- gate status,
- downstream contexts affected,
- time since last progress,
- user-selected importance,
- validation confidence.

The MVP should not choose scoring weights. It only needs stable IDs and relationship fields so scoring can be added later without rewriting the ledger.

## Next Route

Recommended route: implementation-plan.

Reason:

The definition is specific enough to produce a first work-pack for a file-backed recursive ledger MVP under `development/craft/`. The next artifact should define the first ledger files, example rows, validation checks, and task sequence.

## Gate Result

- Status: pass
- Reason: The MVP has a clear objective, bounded scope, source evidence, core vocabulary, acceptance criteria, and non-blocking gaps. The next step is design/plan, not a user decision.
