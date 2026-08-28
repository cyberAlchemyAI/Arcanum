---
tags: [craft, ledger-integrity, deterministic-mutation, runtime-design]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-28T17:18:45-03:00
updated_at: 2026-08-28T17:22:46-03:00
expires: 2026-10-27
decisions_made: true
contradictions_found: true
specs_updated: [runtime/craft-ledger/docs/features/ledger-mutation/discovery.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session establishes the proposed boundary between semantic Craft decisions and deterministic ledger mutation before DomainSpec or implementation planning."
---

# Craft ledger mutation discovery

## Summary

The session evaluated why the current Craft ledger contract does not yet guarantee its own mechanical invariants. It distinguished the model or human as the source of semantic choices from a proposed runtime responsible for validation, candidate construction, indexing, concurrency protection, and atomic persistence. It established that `.craft/ledger.yml` remains authoritative, while embedded indexes, `.craft/index.json`, and `CRAFT.md` remain derived. It clarified that a caller should send a structured operation with a target context, semantic values, evidence, request identity, and expected source revision instead of editing YAML directly. It separated dry-run planning from explicit apply and required stale-source comparison inside the atomic commit boundary. It recorded operation-to-schema differences, incomplete legacy compatibility, index-policy gaps, ID-policy gaps, and runtime ownership as unresolved rather than silently choosing them. Two proposed diagrams were rejected by the operator, and the final discovery intentionally contains no diagrams. A governed review strategy passed readiness and independent tension checks but was never confirmed, registered, or executed; the operator closed the session instead. The resulting discovery is non-governing evidence for a later DomainSpec or design decision.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Craft ledger mutation discovery](../runtime/craft-ledger/docs/features/ledger-mutation/discovery.md) | `contextualizes` | This session records the decisions, evidence boundary, rejected diagram direction, and unresolved questions surrounding the discovery. |
| [Craft Ledger Analysis](../docs/analysis/craft-ledger-evaluation/analysis.md) | `derives-from` | The discovery builds on the analysis that separates interpretive judgment from deterministic enforcement and limits the currently supported validator and index behavior. |
| [Root Craft ledger](../.craft/ledger.yml) | `is-part-of` | This work belongs to the existing `CTX-CRAFT-LEDGER-INTEGRITY` scope and its ledger-mutation child context. |

## Open questions

- Which component owns the mutable runtime and its public interface?
- Which mutation operations and `0.3.0` policies form the first supported slice?
- Which authorities define ID allocation, index completeness, apply authorization, and legacy compatibility?
- Which platform mechanism supplies compare-and-commit and atomic file replacement?

## Next steps

1. Review the discovery's open policy boundaries and choose the first supported operation/profile.
2. Record the required authority decisions before authoring a DomainSpec for the mutable runtime.

## Recommendation

Start the next design pass from one `0.3.0` operation whose method-to-schema mapping, ID behavior, index rules, and apply authority can all be stated without inference; keep every other operation fail-closed.

## Files touched

- docs/analysis/craft-ledger-evaluation/analysis.md
- docs/analysis/craft-ledger-evaluation/review/analysis-assessment/review.md
- docs/analysis/craft-ledger-evaluation/robot-talks/analysis-assessment/review.md
- .arcanum/runtime/evidence-grounded-diagrams/20260828-craft-ledger-mutation-boundary/diagram.mmd
- .arcanum/runtime/evidence-grounded-diagrams/20260828-craft-ledger-mutation-boundary/diagram.yml
- .arcanum/runtime/evidence-grounded-diagrams/20260828-craft-ledger-mutation-flow/diagram.mmd
- .arcanum/runtime/evidence-grounded-diagrams/20260828-craft-ledger-mutation-flow/diagram.yml
- runtime/craft-ledger/docs/features/ledger-mutation/discovery.md
- .craft/ledger.yml
- CRAFT.md
- sessions/2026-08-28-1718-craft-ledger-mutation-discovery.md
