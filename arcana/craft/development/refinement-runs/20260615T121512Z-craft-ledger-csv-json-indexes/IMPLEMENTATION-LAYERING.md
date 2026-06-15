# Implementation Layering: Craft Projection Layer

## L0: Contract

Define projection authority, folder names, freshness metadata, and import safety
rules in Craft schema/docs. No generator yet.

## L1: Fixture

Add a tiny public-safe ledger fixture and expected projection outputs. Fixture
must include nested links, an open decision, a blocker, a gap, and at least one
row family beyond the initial schema set.

## L2: Build And Validate

Add deterministic build and validate tooling:

- generate `index.json`;
- generate `.craft/projections/*.csv`;
- detect stale projections;
- flag unsupported row families.

## L3: Import Dry Run

Add `import-csv --dry-run` to produce a patch plan without mutating YAML. Only
allow editable columns proven by the fixture.

## L4: Runtime Mirrors And Publication

Refresh generated runtime surfaces after canonical source and fixtures pass.
Publish submodule-first only after validation and public-boundary checks.

## Active Layer Window

Start at L0. Import writeback is explicitly outside the first executable slice.
