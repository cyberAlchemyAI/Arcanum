# Strategy Preview

## Inferred Target

Canonical Craft package: `arcana/craft`, using `development/craft` as historical
evidence.

## Desired Outcome

A compact non-executed decision and plan for whether Craft should add a
deterministic row updater/reconciler before broad CSV import writeback.

## Selected Route

Selected route-menu item: `deterministic-row-updater`.

Reason: existing projection planning already gates CSV writeback behind a
dry-run reconcile script, but the first safe primitive appears smaller: compute
a deterministic patch plan for one row family and one row ID, block stale or
unsafe edits, and only then allow broader CSV import semantics to compose it.

## Subagents

Subagent strategy: `none`.

This strategy is narrow enough for parent-owned compact refinement. Subagents
can be reconsidered if the confirmed run exposes competing implementation
routes.

## Confirmation Boundary

No runtime-backed stage runs until the operator confirms this strategy. No
canonical Craft source, generated runtime mirror, publication state, or parent
gitlink is mutated by the strategy proposal.
