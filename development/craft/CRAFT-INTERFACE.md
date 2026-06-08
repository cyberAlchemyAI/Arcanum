# Craft Interface Contract

Status: candidate-local
Date: 2026-06-08
Task: `CRAFT-INTERFACE-001`
Storage model: `.craft/ledger.yml`

## Purpose

Define the local Craft project interface for starting a Craft project and
operating its recursive ledger. This contract is documentation and fixture
authority for local testing only. It does not install a runtime, refresh command
surfaces, promote Craft, or mutate canonical registries.

## Storage Contract

Target projects use:

```text
.craft/
  ledger.yml
  artifacts/
CRAFT.md
```

`.craft/ledger.yml` is the source of truth. `CRAFT.md` is a human-readable view
or summary. Evidence and receipts may be stored under `.craft/artifacts/`.

## Method Contract

### start_project

Inputs:

- `project_id`
- `title`
- `purpose`
- `description`
- `source_contracts`
- `initial_definitions`

Writes:

- root `contexts` row with `parent_id: root`;
- description row scoped to the root context;
- candidate `definitions` rows when provided;
- first `next_move`.

Returns:

- root `context_id`;
- ledger path.

Invariants:

- root context starts with one current `next_move`;
- candidate definitions remain local.

### state

Inputs:

- `context_id`, optional; defaults to root.

Returns:

- context stage and gate;
- latest description;
- blockers, enablers, open decisions, gaps, candidate definitions;
- children and recomposition status;
- current `next_move`.

Invariant:

- state is read-only.

### describe

Inputs:

- `context_id`
- `description`
- `evidence`, optional.

Writes:

- description row.

Returns:

- description id.

Invariant:

- description history is preserved; updates do not erase context purpose.

### add_blocker

Inputs:

- `context_id`
- `summary`
- `blocker_type`
- `lane`
- `evidence`
- `closure_condition`

Writes:

- typed item row with `kind: blocker`;
- optional relation row.

Returns:

- blocker id.

Invariant:

- raw blockers cannot be resolved directly.

### refine_blocker

Inputs:

- `blocker_id`
- `blocker_type`
- `lane`
- `closure_condition`
- `owner`

Writes:

- typed item update with `refinement_status: refined`.

Returns:

- updated blocker id.

Invariant:

- refinement supplies closure criteria, not closure evidence by itself.

### add_enabler

Inputs:

- `context_id`
- `summary`
- `enabler_type`
- `lane`
- `evidence`

Writes:

- typed item row with `kind: enabler`;
- optional `enables` relation.

Returns:

- enabler id.

### next

Inputs:

- `context_id`
- `next_move`
- `route`
- `evidence`

Writes:

- context `next_move` update;
- optional route note.

Returns:

- updated context id.

Invariant:

- active contexts must have exactly one current next move.

### open_decision

Inputs:

- `scope_id`
- `question`
- `options`
- `default_option`, optional
- `decision_type`
- `blocking`

Writes:

- decision row with `status: active`.

Returns:

- decision id.

Invariant:

- blocking decisions stop dependent execution until closed, waived, or deferred.

### decide

Inputs:

- `decision_id`
- `selected_option`
- `rationale`
- `evidence`

Writes:

- decision row update with `status: closed`;
- optional relation or condition updates.

Returns:

- closed decision id.

Invariant:

- decision evidence is required.

### add_gap

Inputs:

- `scope_id`
- `summary`
- `severity`
- `treatment`
- `owner`
- `evidence`

Writes:

- gap row.

Returns:

- gap id.

Invariant:

- treatment must be one of `plan`, `defer`, `waive`, `delegate`, or `split`.

### add_definition

Inputs:

- `scope_id`
- `term`
- `statement`
- `evidence`

Writes:

- definition row with `status: candidate`.

Returns:

- definition id.

Invariant:

- definitions are local candidates unless an owner governance route promotes
  them.

### open_child_context

Inputs:

- `parent_id`
- `child_id`
- `title`
- `purpose`
- `description`
- `entry_reason`
- `recomposition_target`

Writes:

- child `contexts` row;
- `contains` relation from parent to child;
- description row;
- recomposition relation or note.

Returns:

- child context id.

Invariant:

- non-root contexts must have a recomposition path before execution.

### link

Inputs:

- `source_id`
- `target_id`
- `relation_type`
- `reason`
- `evidence`

Writes:

- relation row.

Returns:

- relation id.

### validate

Inputs:

- `context_id`, optional;
- validation profile, optional.

Returns:

- `pass`, `flag`, or `block`;
- failed invariants;
- open blockers and blocking decisions;
- missing recomposition evidence.

Invariant:

- closed contexts without validation and recomposition evidence return `block`.

### recompose

Inputs:

- `child_id`
- `parent_id`
- `summary`
- `evidence`
- `residue`
- `next_parent_move`

Writes:

- recomposition event;
- relation updates;
- parent next move update;
- child closure status when validation passes.

Returns:

- recomposition result.

Invariant:

- child output is not closed for Craft until parent fit is explicit.

### export_ledger

Inputs:

- output format: `yaml` or `markdown-view`.

Returns:

- exported ledger path or rendered view path.

Invariant:

- export does not change the source of truth; `.craft/ledger.yml` remains
  authoritative.

## Validation Boundary

This interface can be used for local Craft tests. It cannot be used as evidence
for promotion, runtime integration, command-surface readiness, or canonical
glossary authority without later owner-route review.
