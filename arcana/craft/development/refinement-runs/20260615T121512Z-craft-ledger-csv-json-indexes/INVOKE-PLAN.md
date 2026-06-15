# Invoke Plan: Craft Ledger Projection Layer

## Objective

Make Craft faster to read and safer to bulk-edit by adding generated JSON and
CSV projection contracts before implementation.

## Plan

1. Update the Craft projection contract.
   - Add `.craft/projections/*.csv` as generated review/import surfaces.
   - Add `index.json` freshness and lookup requirements.
   - Preserve YAML authority.

2. Add a public-safe toy fixture.
   - Cover row IDs, links, evidence, open decisions, active blockers, gaps, and
     a row family beyond the first schema contract.
   - Include expected `index.json` and CSV outputs.

3. Add build/validate tooling.
   - Generate JSON and CSV from the fixture.
   - Validate deterministic headers and row counts.
   - Flag stale hashes and unsupported families.

4. Add import dry-run.
   - Permit only known editable columns.
   - Produce a patch plan.
   - Block on ID churn, unresolved references, nested-link loss, stale source,
     or unsupported family changes.

5. Refresh generated mirrors after canonical validation.
   - Do not publish until public-boundary checks and submodule discipline pass.

## Validation

- `python3 -m json.tool` for JSON outputs.
- YAML parse for source fixture.
- CSV header and row-count checks.
- Round-trip dry-run proof.
- Public-boundary scan on generated outputs.
- `git -C arcanum diff --check`.

## Status

`flag`: plan is executable, but implementation must begin with L0 contract work
and a toy fixture. Import mutation remains blocked until fixture proof passes.
