# Craft Interface Creation Plan

Status: ready-for-task-session
Date: 2026-06-07

## Objective

Create the first local Craft interface in one bounded execution pass so Craft
can be used as a test in another project without relying on the retired command
surface or claiming canonical promotion.

## One-Go Slice

Build one local, file-backed interface slice:

1. Define the interface contract.
2. Extend the ledger schema for `definitions` and `gaps`.
3. Add a structured example ledger for a new Craft project.
4. Add validation rules for recursive contexts and closure evidence.
5. Add a short live-test recipe for using the interface in another repository.

Then keep the interaction layer as the next bounded slice:

6. Define how Craft hands off to owner capabilities and receives receipts.
7. Add route handoff, receipt, and route event row families.
8. Validate that Craft does not absorb `refine`, `decision-gate`, `invoke`,
   `task-session`, or `dispatch-spec` authority.

## Proposed Files

Create or update only Craft-local files:

- `development/craft/CRAFT-INTERFACE.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERFACE-EXAMPLE.yml`
- `development/craft/CRAFT-INTERFACE-VALIDATION.md`
- `development/craft/CRAFT-LIVE-TEST-RECIPE.md`
- `development/craft/CRAFT-INTERACTION-DESIGN.md`
- `development/craft/CRAFT-INTERACTION-DISPATCH.json`
- `development/craft/SESSION-LEDGER.md`, only to append evidence after the task
  completes.

## Interface Surface

The first implementation is a documented local interface plus structured
fixtures, not a runtime adapter.

Required method groups:

- project lifecycle: `start_project`, `state`, `validate`, `export_ledger`;
- context lifecycle: `open_child_context`, `describe`, `next`, `recompose`;
- condition operations: `add_blocker`, `refine_blocker`, `add_enabler`;
- decision operations: `open_decision`, `decide`;
- residue operations: `add_gap`, `add_definition`, `link`.
- interaction operations: `classify_route`, `prepare_handoff`,
  `receive_receipt`, `apply_receipt`, `open_residue`.

## Validation Surface

The validation artifact must prove:

- root context can start a project;
- child contexts preserve parent and recomposition links;
- blockers, enablers, decisions, gaps, and definitions can be queried by
  context;
- raw blockers cannot be resolved directly;
- active contexts cannot lose `next_move`;
- closed child context without recomposition evidence returns `block`;
- local definitions do not claim canonical glossary promotion.
- route handoffs name one owner capability;
- receipts reference handoffs and do not overwrite native owner verdicts;
- `dispatch-spec` validation is route-shape evidence, not execution evidence.

## Live Test Shape

Use a tiny target project with one root Craft context and one child context:

- root: define a small project intention;
- child: refine a blocker or gap;
- recomposition: return child evidence to root;
- final state: root has updated next move and no untyped blockers.

The live test can be manual first. Automation is explicitly deferred unless the
task has time and the schema is stable.

## Non-Goals

- Do not install a command.
- Do not refresh `.codex/commands`.
- Do not promote Craft to registry, sigil, spell, glossary, or ontology.
- Do not build role automation.
- Do not require a generated ledger index.

## Completion Criteria

- Interface contract exists and maps methods to ledger rows.
- Schema extension exists for definitions and gaps.
- Example ledger parses as YAML.
- Validation guide covers recursive closure and local authority boundaries.
- Live-test recipe can be followed in another repository.
- Session ledger records the new interface artifact set and next move.

## Blockers

No current blocker for the local interface slice.

Known deferred decisions:

- runtime shape;
- generated Markdown view;
- glossary promotion bridge;
- automated validation runner;
- whether interaction helpers become a library, CLI, or skill-native helper.
