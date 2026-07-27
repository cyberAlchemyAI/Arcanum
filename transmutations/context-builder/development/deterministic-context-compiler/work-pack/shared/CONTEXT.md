# Shared Context

## Objective

Implement and validate a deterministic compilation boundary for Context
Builder that accepts already-authored obligation/candidate mappings, binds
current selector-level bytes, reuses non-authority excerpt objects, renders one
runtime payload, and records honest cost evidence.

## Required Source Anchors

- [Define specification](../../SPEC.md)
- [Architecture](../../ARCHITECTURE.md)
- [Planned witnesses](../../WITNESS-CONTRACTS.md)
- [Implementation layering](../../IMPLEMENTATION-LAYERING.md)
- [Validation strategy](../../VALIDATION-STRATEGY.md)
- Canonical target: `transmutations/context-builder/SKILL.md`
- Current templates:
  `transmutations/context-builder/templates/runtime-handoff-pack.md` and
  `transmutations/context-builder/templates/runtime-handoff-index.json`

## Fixed Boundaries

- Semantic obligation authoring and candidate mapping are upstream inputs.
- The compiler owns structural validation and deterministic transforms only.
- Inventory handles may seed candidates but never prove freshness or authority.
- Cache state is rebuildable, consumer-local, and non-authoritative.
- The runtime receives exactly one declared payload.
- Actual prompt usage comes only from a runtime receipt.
- Invoke did not select an SWU and did not authorize source mutation.

## Current Evidence State

- Define: pass
- Design: pass with deterministic two-pass fixed point
- Plan: authored; validation pending until package closeout
- Implementation: not started
- Reusable behavior: unproven
- Lifecycle admission: owned by Sigil Development
