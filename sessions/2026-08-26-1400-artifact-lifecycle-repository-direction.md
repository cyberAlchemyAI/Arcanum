---
tags: [artifact-lifecycle, repository-governance, execution-evidence, migration]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-26T14:00:56-03:00
updated_at: 2026-08-26T22:06:26-03:00
expires: 2026-10-25
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session changed the repository recovery direction from copying or discarding capabilities to governing their artifact lifecycle before any migration."
---

# Artifact Lifecycle and Repository Direction

## Summary

The session investigated why Arcanum creates many Markdown and JSON artifacts and whether anything governs their lifecycle. The repository was found to mix reusable product source, development workspaces, historical evidence, generated runtime output, and governance material. The composition analysis preserved a comparatively simple product purpose, while its research showed that contracts are ahead of several integrations and that authority and write-back remain uneven. The user clarified that the existing services and their accumulated work should be preserved rather than replaced. The chosen direction is therefore not to create a clean clone yet, but first to stop services from writing unmanaged execution artifacts into the repository. Arcanum already has an Artifact Constitution with useful classes, but its current enforcement is path-heuristic and does not centrally own storage, retention, promotion, verification, rehydration, or garbage collection. The proposed boundary is that source remains in Git while execution output passes through one external artifact-lifecycle service and enters Git only through explicit promotion. The first bounded proof should use the previously selected Task Session to Invoke Refresh execution package, preserve all bytes by content hash, verify cold rehydration, and include corruption and omission controls. No existing artifacts were deleted, moved, or rewritten in this session. The next work begins with an inventory of artifact producers and consumers rather than another repository-wide redesign.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Arcanum Migration Analysis](../docs/analysis/arcanum-migration/analysis.md) | `derives-from` | The product purpose and central work-state relation used in this session are preserved in the migration analysis. |
| [Arcanum Composition Findings](../docs/analysis/arcanum-migration/research/arcanum-composition/findings.md) | `derives-from` | The decision preserves the findings that current composition is plural, authority-bound, and unevenly implemented. |
| [Artifact Constitution](../framework/ARTIFACT-CONSTITUTION.md) | `contradicts` | The session records that current storage and enforcement do not yet operationally satisfy the constitution's declared lifecycle separation and validation boundary. |

## Open questions

- Which services create each artifact family, and which later services actually consume those artifacts?
- Which retention periods and backup guarantees should apply to ordinary runs and promoted evidence?
- Which compatibility obligations must an external artifact store preserve for existing services?

## Next steps

1. Inventory artifact producers, write locations, artifact families, downstream consumers, and current Git status without modifying or deleting outputs.
2. Specify the smallest artifact-lifecycle interface that implements the existing constitution's classes, promotion boundary, verification, rehydration, and garbage collection.
3. Adapt the selected Task Session to Invoke Refresh witness to the external store and prove byte preservation, cold verification, negative controls, rehydration, and a clean Git worktree.
4. Decide whether a successor repository is still necessary only after the first governed service flow passes.

## Recommendation

Stabilize artifact production before repository migration: preserve the existing services and bytes, make one external lifecycle boundary mandatory for a single witnessed flow, and expand only after that proof succeeds.

## Files touched

- `sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md`
