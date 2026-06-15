# Implementation Layering Seed: Craft Row Update Planner Architecture

## Seed Status

- Mode: design-stage seed.
- Status: `pass`
- Plan requirement: full implementation layering remains owned by a later
  `invoke plan` or `task-session` route.

## Layer Sketch

| Layer | Question | Candidate Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can the contract and toy fixture define safe row update semantics? | schema/docs plus public-safe fixture expectations | YAML/JSON parse and targeted grep |
| L1 | Can an internal planner emit deterministic pass/no-op/block patch reports? | `arcana/craft/scripts/` internal implementation | fixture command output and stable JSON |
| L2 | Can CSV import dry-run call the planner for many row deltas? | CSV import integration | multi-row dry-run report and stale blocking |
| L3 | Can generated mirrors and publication checks absorb the new contract? | generated runtime surfaces and release checks | generation evidence and diff/public-boundary checks |

## Layer Guardrails

- L0 must not implement mutation.
- L1 must not add direct apply mode.
- L2 must treat CSV as a delta producer, not reconciliation owner.
- L3 must follow submodule discipline before parent publication.

## Next Planning Hook

Use this seed to refresh or execute the existing row-updater work-pack if the
next route wants more than `SWU-CRU-001`.
