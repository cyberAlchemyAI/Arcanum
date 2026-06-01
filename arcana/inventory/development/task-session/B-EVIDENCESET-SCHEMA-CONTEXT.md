# Task Session Context: B-EVIDENCESET-SCHEMA

## Selected Unit

Resolve `B-EVIDENCESET-SCHEMA` by implementing and validating the minimal candidate EvidenceSet schema.

## Source Artifacts

- `arcana/inventory/development/WORK-PACK.md`
- `arcana/inventory/development/refinement-runs/20260527T160759Z-evidenceset-schema/SCHEMA-CANDIDATE.md`
- `arcana/inventory/development/refinement-runs/20260527T160759Z-evidenceset-schema/RESULT.md`
- `arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json`
- `arcana/inventory/development/pilot/evidence-card/craft-stressor-retrieval.json`
- `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`

## Gate Verdict

Pass. The blocker is ready for local execution because the schema candidate names the required fields, non-goals, validation rules, and promotion boundary.

## Controlling Constraints

- Keep EvidenceSet candidate-only.
- Do not duplicate evidence-card source excerpts, summaries, trace arrays, or captured metadata.
- Preserve shell plus `jq` as the fast agent/runtime surface.
- Keep human UI deferred.
- Validate both current candidate sets against existing card IDs.

## Write Scope

- `arcana/inventory/templates/evidence-set-schema.md`
- `arcana/inventory/templates/evidence-set.md`
- `arcana/inventory/development/pilot/evidence-card/evidence-sets.json`
- `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`
- `arcana/inventory/templates/index.md`
- `arcana/inventory/README.md`
- `arcana/inventory/SKILL.md`
- `arcana/inventory/development/READINESS.md`
- `arcana/inventory/development/WORK-PACK.md`
- `arcana/inventory/development/task-session/B-EVIDENCESET-SCHEMA-RESULT.md`

## Done Criteria

- Candidate schema and authoring template exist.
- Stored candidate fixture contains both current EvidenceSets.
- Validator proves EvidenceSet references resolve to known card IDs.
- Readiness and work-pack records show the schema blocker resolved but canonical promotion still deferred.
