# Task Session Context: SWU-INV-KS-006

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-003`
- SWU: `SWU-INV-KS-006`
- Goal: add pilot index and retrieval fixtures aligned with `pilot-cards.json`.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-003-pilot-fixtures.md`
- `arcana/inventory/development/pilot/evidence-card/pilot-cards.json`
- `arcana/inventory/templates/index.md`
- `arcana/inventory/development/POC-CANDIDATES.md`
- `arcana/inventory/development/POC-VALIDATION.md`

## Controlling Constraints

- Dependency `SWU-INV-KS-005` must be complete.
- `pilot-index.json` and `pilot-retrieval.json` must parse as JSON.
- Index and retrieval fixtures must reference pilot card IDs.
- Retrieval must include selected cards and excluded matches.

## Gate Verdict

Pass. Pilot cards exist and validate, retrieval shape exists in the production index template, and validation is available.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Retrieval query | Use the recommended EvidenceSet decision query. | This directly tests the active POC question. |
| Candidate set | Include a candidate EvidenceSet inside retrieval output. | It tests whether grouping reduces repeated context assembly without promoting the artifact yet. |
| Runtime | Local fallback. | This SWU is static JSON fixture authoring. |
