# Distill Repair

Status: pass
Owner capability: distill

## Repairs

- Split one vague "database handling" concern into two records: selection and migration command.
- Added `source_of_truth_role` so derived/cache/search/vector/analytics stores cannot silently become authoritative.
- Added environment policy so destructive commands are blocked by default outside disposable environments.
- Added schema history/checksum/lock/drift fields.
- Added expand-contract and backfill fields for production-safe migrations.
- Kept runtime command output as evidence, not canonical spec truth.

## Residue Ledger

| Residue | Owner | Next route |
| --- | --- | --- |
| Final local names for data-resource records | integration-spec governance | decision-gate after L0 example |
| Tool-specific command profiles | task-session or discipline-governance | after generic command profile is accepted |
| Validator fixture schema | formula route | after one filled example |
| Live command proof | task-session | explicit user approval required |
