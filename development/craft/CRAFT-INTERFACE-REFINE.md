# Craft Interface Refine

Status: refined-seed
Date: 2026-06-07
Owner surface: `development/craft/`

## Purpose

Define the first local Craft interface for starting a Craft project and operating
its recursive ledger. This is a candidate local surface for Craft development
and live tests; it does not promote Craft, mutate command surfaces, or install a
runtime adapter.

## Refined Interface Target

Craft needs a small file-backed interface that can:

- initialize a Craft project in another repository;
- create and query the current Craft state;
- record descriptions, blockers, enablers, next moves, open decisions, gaps, and
  candidate definitions;
- create child Craft contexts recursively;
- preserve the recomposition path from child context back to parent context;
- validate ledger invariants before any context is treated as closed.

## Storage Contract

The target project gets a local Craft workspace:

```text
.craft/
  ledger.yml
  artifacts/
CRAFT.md
```

`.craft/ledger.yml` is the structured source of truth. `CRAFT.md` is the human
readable view or summary. `artifacts/` holds optional evidence, receipts, and
linked outputs.

## Core Methods

### start_project

Creates the root Craft context and initial ledger.

Inputs:

- `project_id`
- `title`
- `purpose`
- `description`
- `source_contracts`
- `initial_definitions`

Writes:

- one `contexts` row with `parent_id: null`;
- one `description` entry;
- zero or more candidate `definitions` rows;
- initial `next_move`.

### state

Returns the current ledger state for a context.

Inputs:

- `context_id`, optional; defaults to root context.

Returns:

- context stage;
- gate;
- description;
- blockers;
- enablers;
- open decisions;
- gaps;
- candidate definitions;
- next move;
- children;
- recomposition status.

### describe

Adds or replaces the working description for a context.

Inputs:

- `context_id`
- `description`
- `evidence`, optional.

Invariant:

- description changes are ledger events; they do not silently overwrite the
  reason a context exists.

### add_blocker

Records a blocker without resolving it.

Inputs:

- `context_id`
- `summary`
- `blocker_type`
- `lane`
- `evidence`
- `closure_condition`

Writes:

- typed item row with `kind: blocker`;
- relation row when the blocker affects another context or artifact.

Invariant:

- raw blockers cannot be resolved directly; they must be refined or waived by a
  decision.

### refine_blocker

Turns a raw blocker into a typed blocker with closure evidence.

Inputs:

- `blocker_id`
- `blocker_type`
- `lane`
- `closure_condition`
- `owner`

Writes:

- updated typed item with `refinement_status: refined`.

### add_enabler

Records a positive condition that unlocks or supports a next move.

Inputs:

- `context_id`
- `summary`
- `enabler_type`
- `lane`
- `evidence`

Writes:

- typed item row with `kind: enabler`;
- optional `enables` relation.

### next

Sets the next Craft move for a context.

Inputs:

- `context_id`
- `next_move`
- `route`
- `evidence`

Invariant:

- every active context has exactly one current next move.

### open_decision

Creates an explicit decision row.

Inputs:

- `scope_id`
- `question`
- `options`
- `default_option`, optional
- `decision_type`
- `blocking`, boolean.

Writes:

- decision row with `status: active`.

### decide

Closes a decision with rationale and evidence.

Inputs:

- `decision_id`
- `selected_option`
- `rationale`
- `evidence`

Writes:

- decision row update;
- optional relation updates for blockers, gaps, or next move.

### add_gap

Records something missing from the Craft project.

Inputs:

- `scope_id`
- `summary`
- `severity`
- `treatment`
- `owner`
- `evidence`

Writes:

- gap row with `status: active`.

### add_definition

Adds a candidate local definition.

Inputs:

- `scope_id`
- `term`
- `statement`
- `evidence`

Writes:

- definition row with `status: candidate`.

Invariant:

- local Craft definitions do not become canonical glossary entries without an
  owner route.

### open_child_context

Creates a recursive Craft context under a parent.

Inputs:

- `parent_id`
- `child_id`
- `title`
- `purpose`
- `description`
- `entry_reason`

Writes:

- child `contexts` row;
- `contains` relation from parent to child;
- child next move.

Invariant:

- every child context must name how it will recompose into the parent before it
  can execute.

### link

Creates a typed relation between ledger objects.

Inputs:

- `source_id`
- `target_id`
- `relation_type`
- `reason`
- `evidence`

### validate

Checks ledger invariants for one context or the whole project.

Returns:

- `pass`, `flag`, or `block`;
- invariant failures;
- missing evidence;
- open blockers and blocking decisions.

### recompose

Closes or returns evidence from a child context to its parent.

Inputs:

- `child_id`
- `parent_id`
- `summary`
- `evidence`
- `residue`
- `next_parent_move`

Writes:

- recomposition relation or update;
- parent next move update;
- child closure status when validation passes.

### export_ledger

Exports the ledger as a stable structured document and optional Markdown view.

## Ledger Extensions

The existing Craft ledger already has context, artifact, relation, typed item,
and decision rows. The interface needs two candidate row families:

### definitions

Required fields:

- `definition_id`
- `scope_id`
- `term`
- `statement`
- `status`
- `evidence`

Allowed statuses:

- `candidate`
- `active-local`
- `superseded`
- `promoted-by-owner`

### gaps

Required fields:

- `gap_id`
- `scope_id`
- `summary`
- `severity`
- `treatment`
- `owner`
- `status`
- `evidence`

Allowed statuses:

- `active`
- `planned`
- `resolved`
- `waived`
- `superseded`

## Recursive Property

Craft is recursive because every context can be treated as a smaller Craft
project with the same interface:

- a project is a root context;
- a workstream, decision, blocker, or live test can become a child context;
- child contexts carry their own blockers, enablers, decisions, gaps,
  definitions, and next move;
- child contexts must report residue and recomposition evidence back to the
  parent;
- parent contexts remain responsible for deciding whether child evidence
  changes the route, closes a gap, or opens another context.

This prevents Craft from becoming a flat backlog. It also prevents child work
from disappearing after local success.

## Invariants

- Every active context has a `next_move`.
- Every non-root context has one parent context.
- Every non-root context has a recomposition path.
- Raw blockers cannot be directly resolved.
- Blocking decisions stop execution until closed, waived, or explicitly
  deferred.
- Gaps must name treatment: `plan`, `defer`, `waive`, `delegate`, or `split`.
- Definitions remain local candidates unless a glossary owner route promotes
  them.
- Validation must return `block` when a context is closed without evidence.
- Interface work does not mutate command surfaces, skill installs, registries,
  or canonical promotion surfaces.

## Decision Gate Result

Decision: proceed with a local file-backed interface first.

Rationale: this satisfies the live-test need while preserving Craft promotion
deferral and avoiding the retired command surface.

Open decisions deferred to later owner routes:

- whether the interface becomes a CLI, library API, skill helper, or all three;
- whether `.craft/ledger.yml` should be generated from Markdown or become the
  only source of truth;
- whether definitions get a dedicated promotion bridge to glossary governance;
- whether the Markdown view is generated automatically.

## Codex Goal Profile Readiness

Status: not generated yet.

Reason: the interface is now refined as a build target, but native goal creation
should wait until a single execution task has a context pack and selected file
set. `CRAFT-INTERFACE-WORK-PACK.md` defines that task.
