---
tags: [arcanum-migration, capability-mapping, artifact-lifecycle, repository-governance]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-27T13:20:12-03:00
updated_at: 2026-08-27T13:20:12-03:00
expires: 2026-10-26
decisions_made: true
contradictions_found: true
specs_updated: [docs/analysis/arcanum-migration/analysis.md, docs/analysis/arcanum-migration/contracts/current-system-map.schema.json]
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session established the governed mapping contract and evidence boundaries that must precede the Arcanum migration branch."
---

# Arcanum Migration Map Foundation

## Summary

The session set out to map Arcanum's principal concepts and services before planning a migration to a new branch. It retained Craft, Task Session, and Decision Gate as the minimum product explanation while expanding the migration inventory to runtime, invocation, readiness, continuation, goals, capability distribution, and artifact lifecycle. Reviews clarified that Craft owns only its selected ledger, that external results require an explicit caller-mediated write-back, and that Arcanum composes through multiple owner-bound relations rather than one universal pipeline. The work introduced a versioned current-system-map schema, a conforming example, and a deterministic validator with relation identity, discovery coverage, reproducible-baseline, typed-unknown, and decision-readiness checks. The analysis was corrected to distinguish accepted preservation constraints from the still-proposed external artifact boundary and proof flow, and its evidence paths, hashes, and session provenance were repaired. No migration branch or canonical current-system map was created because the dirty working tree is not a reconstructible baseline. A final independent review found no major defects and left two minor inventory corrections for the next session.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Arcanum Migration](../docs/analysis/arcanum-migration/README.md) | `is-part-of` | This session established the mapping and evidence foundation for the migration project described there. |
| [Arcanum Migration Analysis](../docs/analysis/arcanum-migration/analysis.md) | `refines` | This session widened and corrected the reader-facing model while retaining its low-resolution purpose. |
| [Artifact Lifecycle and Repository Direction](2026-08-26-1400-artifact-lifecycle-repository-direction.md) | `derives-from` | The work preserves its no-clean-rewrite direction while keeping its external boundary and first proof explicitly proposed. |

## Open questions

- Which reproducible baseline should seed `mapping/current-system-map.json`: a clean Git commit or a content-addressed bundle of the required dirty state?

## Next steps

1. Split Context Builder, Work-Pack Readiness Audit, and Implementation Readiness into independently statused inventory entries.
2. Replace the capability-lifecycle aggregate owner language with explicit canonical-source, registry/resolver, generated-projection, and legacy-installer responsibilities.
3. Present the clean-commit and content-bundle baseline options through an explicit migration decision.
4. Create `mapping/current-system-map.json` from the selected baseline and run the validator with `--require-ready`.

## Recommendation

Apply the two bounded inventory corrections first, then resolve the baseline question before producing the canonical map; the schema intentionally prevents a dirty, hash-only inspection state from being declared migration-ready.

## Files touched

- `docs/analysis/arcanum-migration/analysis.md`
- `docs/analysis/arcanum-migration/README.md`
- `docs/analysis/arcanum-migration/review.md`
- `docs/analysis/arcanum-migration/review/migration-map/review.md`
- `docs/analysis/arcanum-migration/research/arcanum-composition/initial-definitions-review.md`
- `docs/analysis/arcanum-migration/contracts/current-system-map.schema.json`
- `docs/analysis/arcanum-migration/contracts/current-system-map.example.json`
- `docs/analysis/arcanum-migration/scripts/validate_mapping.py`
- `docs/analysis/arcanum-migration/requirements.txt`
- `sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md`
- `.arcanum/observability/subagents-strategy/subagents-dispatch.yaml`
- `.arcanum/runtime/orchestrate/2026-08-26-analysis-inventory-review-v2/`
- `.arcanum/runtime/orchestrate/2026-08-26-analysis-postfix-review/`
- `sessions/2026-08-27-1320-arcanum-migration-map-foundation.md`
