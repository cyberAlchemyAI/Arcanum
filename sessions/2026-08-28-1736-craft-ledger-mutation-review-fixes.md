---
tags: [craft, ledger-integrity, deterministic-mutation, idempotency]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-28T17:36:10-03:00
updated_at: 2026-08-28T17:36:10-03:00
expires: 2026-10-27
decisions_made: true
contradictions_found: true
specs_updated: [runtime/craft-ledger/docs/features/ledger-mutation/discovery.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session closes load-bearing safety gaps in the proposed Craft ledger mutation contract before DomainSpec or implementation planning."
---

# Craft ledger mutation review fixes

## Summary

The session red-teamed the existing Craft ledger mutation discovery against fidelity, mechanical correctness, operability, and abuse resistance. The review found load-bearing gaps in plan identity, idempotent replay, workspace confinement, request operability, result classification, and high-level system visualization. The operator authorized the fixes without authorizing runtime implementation. The discovery now binds each plan to the normalized request, source revision, operational profile, serializer, candidate bytes, and authorization scope. It distinguishes `NO_OP`, `ALREADY_APPLIED`, `CONFLICT`, `PLAN_MISMATCH`, `INVALID`, `UNKNOWN`, `UNSUPPORTED`, and `STALE_SOURCE`, and requires durable replay proof before idempotent apply can be claimed. It derives the target ledger from a canonically resolved workspace, completes the `add_gap` example, and defines deterministic byte identity. Two confirmed Mermaid diagrams now expose the responsibility boundaries and the plan-to-apply sequence with editable sources, metadata, and PNG previews. Validation confirmed the YAML example, all local links, Mermaid source parity, metadata, and rendered PNGs. The discovery remains non-governing evidence and preserves unresolved ownership, authorization, compatibility, serializer-policy, and atomicity choices for later authority decisions.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Craft ledger mutation discovery](../runtime/craft-ledger/docs/features/ledger-mutation/discovery.md) | `validates` | This session records the adversarial findings, bounded fixes, and verification evidence applied to the discovery. |
| [Prior Craft ledger mutation discovery session](2026-08-28-1718-craft-ledger-mutation-discovery.md) | `refines` | This later session preserves the earlier historical closeout while recording the subsequently approved diagrams and stricter mutation contracts. |

## Open questions

- Which component owns the mutable runtime and its public interface?
- Which operation and `0.3.0` profile form the first supported slice?
- Which authorities close ID allocation, index completeness, apply authorization, replay retention, and legacy compatibility?
- Which serializer policies and platform mechanism provide deterministic bytes and atomic compare-and-commit?

## Next steps

1. Resolve the discovery's authority and first-profile questions before DomainSpec authoring.
2. Specify fixtures for plan identity, replay, target confinement, deterministic bytes, and every fail-closed result.

## Recommendation

Start with one `0.3.0` operation whose mapping, serializer, replay proof, index rules, and apply authority can all be specified without inference; keep unsupported policy combinations fail-closed.

## Files touched

- runtime/craft-ledger/docs/features/ledger-mutation/discovery.md
- output/diagrams/20260828-craft-ledger-mutation-boundaries/diagram.mmd
- output/diagrams/20260828-craft-ledger-mutation-boundaries/diagram.png
- output/diagrams/20260828-craft-ledger-mutation-boundaries/diagram.yml
- output/diagrams/20260828-craft-ledger-plan-apply-flow/diagram.mmd
- output/diagrams/20260828-craft-ledger-plan-apply-flow/diagram.png
- output/diagrams/20260828-craft-ledger-plan-apply-flow/diagram.yml
- sessions/2026-08-28-1736-craft-ledger-mutation-review-fixes.md
