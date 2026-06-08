# Craft Interface Goal Context

Status: strict-coverage-pass
Date: 2026-06-08
Work-pack: `development/craft/CRAFT-INTERFACE-WORK-PACK.md`
Selected unit: ordered work-pack sequence

## Objective

Execute every ready task in the Craft interface work-pack in order:

1. `CRAFT-INTERFACE-001`
2. `CRAFT-INTERACTION-001`

This context pack exists so the native Codex `/goal` can stay compact and point
to durable artifacts instead of embedding the full work-pack.

## Source Contracts

Use these as the controlling source set:

- `development/craft/CRAFT-INTERFACE-WORK-PACK.md`
- `development/craft/CRAFT-INTERFACE-REFINE.md`
- `development/craft/CRAFT-INTERFACE-CREATION-PLAN.md`
- `development/craft/CRAFT-INTERACTION-DESIGN.md`
- `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`
- `docs/decisions/craft-interface-development-risk-gates.md`
- `development/craft/CRAFT-ARCHITECTURE.md`
- `development/craft/CRAFT-LEDGER-SCHEMA.yml`
- `development/craft/LEDGER.md`
- `development/craft/CRAFT-VALIDATION.md`

## Execution Order

### CRAFT-INTERFACE-001

Create:

- `development/craft/CRAFT-INTERFACE.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERFACE-EXAMPLE.yml`
- `development/craft/CRAFT-INTERFACE-VALIDATION.md`
- `development/craft/CRAFT-LIVE-TEST-RECIPE.md`

Required method coverage:

- `start_project`
- `state`
- `describe`
- `add_blocker`
- `refine_blocker`
- `add_enabler`
- `next`
- `open_decision`
- `decide`
- `add_gap`
- `add_definition`
- `open_child_context`
- `link`
- `validate`
- `recompose`
- `export_ledger`

### CRAFT-INTERACTION-001

Create:

- `development/craft/CRAFT-INTERACTION-CONTRACT.md`
- `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERACTION-EXAMPLE.yml`
- `development/craft/CRAFT-INTERACTION-VALIDATION.md`

Required method coverage:

- `classify_route`
- `prepare_handoff`
- `receive_receipt`
- `apply_receipt`
- `open_residue`

Required capability contracts:

- `refine`
- `decision-gate`
- `invoke`
- `task-session`
- `dispatch-spec`

## Write Scope

Allowed:

- the output files named above;
- append-only synchronization to `development/craft/SESSION-LEDGER.md` when
  evidence supports it.

Not allowed:

- command surfaces;
- runtime adapters;
- registries;
- sigils;
- spells;
- canonical glossary state;
- promotion artifacts outside the local Craft package.

## Hard Gates

Stop and report `BLOCK` if any condition from
`development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md` is violated.

Especially block if:

- `CRAFT.md` becomes the source of truth instead of `.craft/ledger.yml`;
- dispatch validation is represented as execution evidence;
- a receipt can close a Craft context without recomposition evidence;
- a raw blocker can be resolved directly;
- definitions are promoted without an owner route.

## Validation

Run after each relevant task:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in [
    "development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml",
    "development/craft/CRAFT-INTERFACE-EXAMPLE.yml",
    "development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml",
    "development/craft/CRAFT-INTERACTION-EXAMPLE.yml",
]:
    if Path(path).exists():
        yaml.safe_load(Path(path).read_text())
print("craft interface yaml ok")
PY

formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/CRAFT-INTERFACE-DISPATCH.json
formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/CRAFT-INTERACTION-DISPATCH.json
```

Manual validation:

- every required method is documented with inputs, writes/returns, and
  invariants;
- interface schema includes `definitions` and `gaps`;
- interaction schema includes `route_handoffs`, `receipts`, and `route_events`;
- examples show recursive context, recomposition, and receipt ownership
  boundaries;
- validation guides return pass, flag, or block.

## Fallback Exploration

Named gaps only. Extra source reads are allowed only when a required output
needs a missing detail from a named source contract or a hard-gate ambiguity.
The final report must list each extra source, the gap it answered, and whether
it changed the result.

## Blocked Stop Condition

If a hard gate fails, source context contradicts the work-pack, validation fails
after bounded repair, or required source files are missing, stop with `BLOCK`.
Report the exact failing gate, file, validation command, and smallest unblock
action. Do not continue into promotion, runtime, registry, command, sigil, spell,
or canonical glossary mutation.
