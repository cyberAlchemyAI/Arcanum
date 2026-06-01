# Refine Result: EvidenceSet Schema

## Status

flag

## Why Flag

The target is refined enough for a Task Session, but the canonical Refine command-backed loop did not fully execute. `context-builder` resolved but `tools/arcanum --exec` timed out after 120 seconds and emitted no stage artifact.

This result is therefore a Refine-owned local synthesis, not a fully successful ten-stage command-backed refine run.

## Final Synthesis

`EvidenceSet` should become a candidate schema design, not a canonical production artifact yet.

The smallest coherent unit is:

> A stable, task-scoped grouping of evidence-card IDs with inclusion reasons, exclusion reasons, index terms, handoff intent, synthesis note, residue, status, and promotion owner.

The schema should be flat JSON and optimized for shell plus `jq` agent access. It should reference cards by ID rather than duplicating evidence. It should preserve boundaries through explicit exclusions and residue.

## Candidate Schema

See `SCHEMA-CANDIDATE.md`.

## Remaining Blocker

Canonical production promotion remains blocked until a Task Session implements and validates the candidate schema against both existing candidate sets.

## Recommended Next Route

Run `task-session` for `B-EVIDENCESET-SCHEMA` with this scope:

- add `arcana/inventory/templates/evidence-set-schema.md`;
- add `arcana/inventory/templates/evidence-set.md`;
- add candidate stored fixture(s) derived from both existing candidate sets;
- update `validate-evidence-card-fixtures.sh` or add a sibling validator section for EvidenceSet references;
- update readiness and work-pack records only after validation passes.

## Stop Conditions For Next Route

- block if stored set IDs conflict with retrieval IDs;
- block if EvidenceSet starts duplicating evidence-card content;
- block if validation cannot prove every included/excluded card ID resolves;
- block if status/promotion ownership is ambiguous;
- defer human UI fields.
