# Validator Runtime: Inventory Evidence-Card

## Purpose

Define the first executable validator surface for Inventory evidence-card fixtures.

## Selected Surface

The agent/runtime validator uses shell plus `jq`.

This surface is optimized for agents: it should be fast, local, composable with `tools/arcanum`, and cheap to run before lookup, retrieval, handoff, or task-session execution.

## Deferred Surface

The human UI is deferred.

Do not build browsable reports, dashboards, or review screens in the validator runtime task. Revisit the human UI only after the shell plus `jq` surface proves useful or its reports become too hard for humans to inspect.

## Validator Scope

The first validator checks:

- JSON parseability;
- evidence-card required fields;
- controlled vocabularies;
- `source_refs` presence and selector shape;
- full/minimal profile rules;
- `promotion_owner` and terminal `promotion_status` pairing;
- relation candidate evidence refs, target resolution, and non-authority notice;
- retrieval selected/excluded card references;
- EvidenceSet required fields, controlled vocabularies, unique IDs, and card ID references;
- handoff packet `source_refs`;
- handoff packet non-authority text.

## Historical Batch Note

`SWU-INV-KS-010`, `SWU-INV-KS-011`, and `SWU-INV-KS-012` were previously run as a completed W4 batch because their write scopes were disjoint.

That batch remains completion evidence only. Future Inventory task-session execution follows `task-session/SEQUENTIAL-RUN-POLICY.md`: one ready task or SWU at a time, stop at the first blocker or gap, and route blocker-level choices through `decision-gate`.

The human UI remains deferred and non-blocking unless a future task proposes a human-facing validator surface. That future proposal should run through `decision-gate` before implementation.

## Command

```sh
bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card
```

## Output Contract

The validator prints one `PASS:` or `FAIL:` line per check and exits nonzero on any failure.
