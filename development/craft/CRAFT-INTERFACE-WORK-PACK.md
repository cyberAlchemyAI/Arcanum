# Craft Interface Work Pack

Status: ready
Date: 2026-06-07

## Task CRAFT-INTERFACE-001

Create the local Craft project interface contract and fixtures.

### Context

Craft already has a recursive ledger MVP and validation guidance, but it lacks a
clear local interface for starting a Craft project and operating the ledger in
another repository.

This task creates the interface layer without promoting Craft or reviving the
command surface.

### Inputs

- `development/craft/CRAFT-ARCHITECTURE.md`
- `development/craft/CRAFT-LEDGER-SCHEMA.yml`
- `development/craft/LEDGER.md`
- `development/craft/CRAFT-VALIDATION.md`
- `development/craft/CRAFT-INTERFACE-REFINE.md`
- `development/craft/CRAFT-INTERFACE-CREATION-PLAN.md`
- `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`
- `docs/decisions/craft-interface-development-risk-gates.md`

### Output Files

- `development/craft/CRAFT-INTERFACE.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERFACE-EXAMPLE.yml`
- `development/craft/CRAFT-INTERFACE-VALIDATION.md`
- `development/craft/CRAFT-LIVE-TEST-RECIPE.md`

Optional append-only update:

- `development/craft/SESSION-LEDGER.md`

### Required Methods

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

### Implementation Rules

- Keep the interface local to `development/craft/`.
- Use `.craft/ledger.yml` as the target project storage model.
- Keep `CRAFT.md` as the target project human-readable view.
- Extend the ledger only for `definitions` and `gaps`.
- Preserve existing Craft vocabulary and statuses where possible.
- Treat runtime, CLI, skill helper, and generated views as deferred decisions.
- Do not edit command surfaces or canonical registries.
- Apply the hard gates from
  `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`.

### Validation Commands

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in [
    "development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml",
    "development/craft/CRAFT-INTERFACE-EXAMPLE.yml",
]:
    yaml.safe_load(Path(path).read_text())
print("craft interface yaml ok")
PY

formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/CRAFT-INTERFACE-DISPATCH.json
```

### Done Criteria

- All required methods are documented with inputs, writes, returns, and
  invariants.
- Schema extension includes `definitions` and `gaps`.
- Example ledger demonstrates root context, child context, blocker, enabler,
  decision, gap, definition, next move, and recomposition.
- Validation guide marks the candidate interface as pass, flag, or block.
- Live-test recipe names exact steps for testing Craft in another project.
- Dispatch validates without blocking.
- No hard gate from the development gap review is violated.

### Expected Result

`pass` for local interface readiness, with runtime automation still deferred.

## Task CRAFT-INTERACTION-001

Create the local Craft interaction contract for owner capability handoffs and
receipts.

### Context

`CRAFT-INTERFACE-001` defines the ledger operations for a local Craft project.
Craft also needs an interaction layer so it can route work to owner
capabilities, record handoffs, receive receipts, and recompose results without
claiming authority over the called sigil or spell.

### Dependencies

- `CRAFT-INTERFACE-001` should exist first or be executed in the same parent
  session before this task.

### Inputs

- `development/craft/CRAFT-ARCHITECTURE.md`
- `development/craft/CRAFT-INTERFACE-REFINE.md`
- `development/craft/CRAFT-INTERACTION-DESIGN.md`
- `development/craft/CRAFT-INTERACTION-DISPATCH.json`
- `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`
- `docs/decisions/craft-interface-development-risk-gates.md`

### Output Files

- `development/craft/CRAFT-INTERACTION-CONTRACT.md`
- `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERACTION-EXAMPLE.yml`
- `development/craft/CRAFT-INTERACTION-VALIDATION.md`

Optional append-only update:

- `development/craft/SESSION-LEDGER.md`

### Required Methods

- `classify_route`
- `prepare_handoff`
- `receive_receipt`
- `apply_receipt`
- `open_residue`

### Required Capability Contracts

- `refine`
- `decision-gate`
- `invoke`
- `task-session`
- `dispatch-spec`

### Implementation Rules

- Craft records route memory; called capabilities own native artifacts,
  validation, and verdicts.
- A route handoff must name exactly one owner capability.
- A receipt must reference exactly one handoff.
- A blocked receipt cannot close a Craft context.
- `dispatch-spec` pass validates route shape only.
- `invoke plan` output is planning evidence, not execution evidence.
- `task-session` pass can close execution work only after recomposition evidence
  is recorded in Craft.
- No command-surface refresh, registry mutation, promotion, or runtime adapter
  implementation.
- Apply the hard gates from
  `development/craft/CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md`.

### Validation Commands

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in [
    "development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml",
    "development/craft/CRAFT-INTERACTION-EXAMPLE.yml",
]:
    yaml.safe_load(Path(path).read_text())
print("craft interaction yaml ok")
PY

formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/CRAFT-INTERACTION-DISPATCH.json
```

### Done Criteria

- Interaction contract maps Craft to `refine`, `decision-gate`, `invoke`,
  `task-session`, and `dispatch-spec`.
- Schema extension includes `route_handoffs`, `receipts`, and `route_events`.
- Example shows at least one handoff and receipt.
- Validation guide proves owner boundaries and blocked-result behavior.
- Dispatch validates without blocking.
- No hard gate from the development gap review is violated.

### Expected Result

`pass` for local interaction design readiness, with runtime execution helpers
still deferred.
