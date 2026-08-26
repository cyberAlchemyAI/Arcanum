---
tags: [unified-skill-model, skill-governance, compatibility, research-review]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-26T13:59:00-03:00
updated_at: 2026-08-26T13:59:00-03:00
expires: 2026-10-25
decisions_made: true
contradictions_found: true
specs_updated: [arcana/research/SKILL.md, arcana/research-initial-definitions/SKILL.md, research/unified-skill-model/research-initial-definitions.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session establishes the evidence-bounded direction for replacing Arcanum's three capability tiers with a unified skill model without breaking path-dependent consumers."
---

# Unified Skill Model Review

## Summary

The session set out to determine what `arcana/`, `formulae/`, and `transmutations/` mean in practice and whether they should become one skill model. It inspected the current creation lifecycle, structural representations, governance surfaces, runtime consumers, publication paths, and compatibility references. Updated `research` and `research-initial-definitions` capabilities were brought into Arcanum, and the informational baseline was expanded to exactly 15 research questions. The collected evidence shows that all three families are exposed as skills and that tier values are not witnessed as selectors of differentiated execution permissions, dispatch behavior, or dependency semantics. The directory names nevertheless remain active path-bearing inputs for discovery, provenance, publication, validation, and several runtime resolvers. The resulting decision is to design one canonical skill model while deferring physical renames or moves until identity, schema, precedence, and compatibility behavior are explicit. Two independent reviewers found citation, schema-strength, process-topology, and writing-contract defects; verified corrections were incorporated into the final findings. The original research dispatch was not represented as canonically resolved because its stale adapter combined synthesis and writing. The surviving recommendation is therefore a design `GO` and an immediate migration `NO-GO`.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Unified skill model initial definitions](../research/unified-skill-model/research-initial-definitions.md) | `is-part-of` | This session advances the repository-wide decision framed by the validated 15-question baseline. |
| [Unified skill model review](../research/unified-skill-model/review.md) | `derives-from` | The session verdict incorporates the two-agent adversarial review and its verified change requests. |
| [Unified skill model findings](../research/unified-skill-model/findings.md) | `derives-from` | The recommendation and evidence boundaries are drawn from the corrected synthesis. |

## Open questions

- Which external consumers depend on tiered URLs, downloads, schema identifiers, or generated provenance?
- Which structural artifact should own the minimum skill schema and precedence across frontmatter, body, sidecars, dependencies, registries, and projections?
- How should `arcana/research/SKILL.md` reconcile its output-shape requirements with the writing contracts it delegates to?

## Next steps

1. Define a stable capability ID and minimum skill schema independently of canonical directory placement.
2. Inventory every internal and external consumer of category-qualified paths.
3. Introduce ID-based resolution and compatibility aliases before moving canonical packages.
4. Reconcile the canonical research workflow with its delegated writing contracts.

## Recommendation

Proceed with the unified skill-model design, licensed by the absence of witnessed tier-selected runtime semantics, but block directory consolidation until the path-consumer inventory and compatibility transition pass bounded trials.

## Files touched

- `.agents/skills/research-initial-definitions/SKILL.md`
- `.agents/skills/research-initial-definitions/scripts/validate_initial_definitions.py`
- `arcana/research/SKILL.md`
- `arcana/research-initial-definitions/SKILL.md`
- `arcana/research-initial-definitions/development/test_validate_initial_definitions.py`
- `arcana/research-initial-definitions/scripts/validate_initial_definitions.py`
- `research/unified-skill-model/dispatch-ledger.jsonl`
- `research/unified-skill-model/findings.md`
- `research/unified-skill-model/material-strategy.json`
- `research/unified-skill-model/research-initial-definitions.md`
- `research/unified-skill-model/research.md`
- `research/unified-skill-model/review.md`
- `research/unified-skill-model/runtime-profile.json`
- `research/unified-skill-model/unified-skill-model-research.dispatch.json`
