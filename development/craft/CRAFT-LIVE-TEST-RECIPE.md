# Craft Live Test Recipe

Status: candidate-local
Date: 2026-06-08
Task: `CRAFT-INTERFACE-001`

## Purpose

Provide a manual first live test for using Craft in another repository without
installing a command, mutating runtime adapters, or promoting Craft.

## Setup

In the target project, create:

```text
.craft/
  ledger.yml
  artifacts/
CRAFT.md
```

Use `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml` as the schema guide
and `development/craft/CRAFT-INTERFACE-EXAMPLE.yml` as the first fixture model.

## Scenario

Test one root context and one child context:

1. Start a root Craft project with `start_project`.
2. Record a working description with `describe`.
3. Add one candidate definition with `add_definition`.
4. Add one raw blocker with `add_blocker`.
5. Open a child context with `open_child_context` to refine that blocker.
6. Refine the blocker with `refine_blocker`.
7. Open and close one decision with `open_decision` and `decide`.
8. Add one gap with `add_gap`.
9. Set the parent next move with `next`.
10. Recompose the child context into the parent with `recompose`.
11. Run `validate`.
12. Export or update `CRAFT.md` as a human-readable view with `export_ledger`.

## Expected Evidence

The resulting `.craft/ledger.yml` should contain:

- one root context;
- one child context;
- one description row per context;
- one candidate definition;
- one gap;
- one blocker refined or resolved with evidence;
- one decision record;
- one recomposition record;
- one parent next move after recomposition.

## Pass Criteria

- `.craft/ledger.yml` remains the source of truth.
- `CRAFT.md` is only a view or summary.
- Raw blockers are not resolved directly.
- Child context has a parent and recomposition path.
- Context closure requires validation evidence and recomposition evidence.
- Candidate definitions remain local.

## Flag Criteria

- The recipe needs an executable validator.
- The target project needs generated views.
- The target project needs repeated query patterns for a ledger index.

## Block Criteria

- The test edits command surfaces, runtime adapters, registries, sigils, spells,
  or canonical glossary state.
- `CRAFT.md` becomes the source of truth.
- A raw blocker is marked resolved without refinement, waiver, or decision
  evidence.
- A child context is closed without recomposition evidence.

## Result Recording

Record the live-test result as:

```text
target:
ledger_path:
result: pass | flag | block
validation_evidence:
residue:
next_move:
extra_sources_used:
```

This recipe proves local usability only. It is not promotion evidence by itself
until repeated across independent Craft contexts.
