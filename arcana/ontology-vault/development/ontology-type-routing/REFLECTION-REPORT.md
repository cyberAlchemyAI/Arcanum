# Ontology Type Routing Reflection

Date: 2026-07-31

Target: Ontology Vault

Trigger: manual user correction plus one recorded medium process gap

## Signal Summary

- Meaningful executions reviewed: 2
- Initial routing: business-system bridge
- Corrected routing: architecture-property ontology
- User correction signals: 1
- Severe safety or authority gaps: 0
- Output-contract drift: selection evidence was absent from the reusable
  output contract

## Pattern Found

The sigil had branch-aware traversal but no explicit model-archetype selection.
That allowed two system-facing questions—cross-branch traceability and
architecture-property evaluation—to collapse into one route.

## Proposed And Accepted Changes

- Add six product-neutral ontology routing archetypes.
- Make ontology type the primary model-shape axis.
- Infer only clear intent; ask for a bounded selection when ambiguous.
- Treat project-local types as aliases of a reusable archetype.
- Derive branch defaults while preserving compatible explicit branch filters.
- Add type-selection fields to runtime profiles, observability, and results.
- Add an architecture-property mapping process and a correction regression
  fixture.

## Changes Explicitly Rejected

- Promoting the routing archetypes to canonical Arcanum definitions.
- Copying any project-local ontology taxonomy into the catalog.
- Replacing `--branch`, `--branches`, or `--bridge` with a competing mechanism.
- Treating architecture-property projections as authority or conformance
  verdicts.
- Adding automatic ontology-type catalog mutation from usage history.

## Thresholds

The default reflection thresholds remain unchanged: five meaningful uses, ten
artifacts since the prior reflection, three related gaps, or one severe gap.

## Next Review Trigger

Reflect again after five post-update meaningful Ontology Vault executions, or
immediately if a clear intent prompts unnecessarily, an ambiguous intent is
silently selected, or architecture-property intent routes to a bridge again.

## Iteration Decision

Targeted update. Promotion is not requested.
