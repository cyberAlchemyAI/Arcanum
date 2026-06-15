# S08 Distill Repair

Status: pass

Repairs applied:

- Renamed CSV output namespace to `.craft/projections/`.
- Added `pending.csv` and `pending_by_node` to support all-status reads.
- Added row-family gap as explicit work-pack residue.
- Made CSV import dry-run-only until fixture proof passes.
- Split decision projection columns into workflow and final-state fields.

Remaining flag: implementation must prove round-trip safety with a public-safe
fixture before enabling writeback.
