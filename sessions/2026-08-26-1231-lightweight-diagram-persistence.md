---
tags: [diagram-governance, artifact-persistence, mermaid, json-schema]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-26T12:31:00-03:00
updated_at: 2026-08-26T12:31:00-03:00
expires: 2026-10-25
decisions_made: true
contradictions_found: false
specs_updated:
  - transmutations/evidence-grounded-diagrams/SKILL.md
  - transmutations/evidence-grounded-diagrams/schemas/diagram.schema.json
  - transmutations/evidence-grounded-diagrams/references/artifact-lifecycle.md
  - transmutations/evidence-grounded-diagrams/references/runbooks.md
  - transmutations/evidence-grounded-diagrams/references/schema-guide.md
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session changes the default storage and lifecycle contract for every ordinary diagram while preserving the advanced governed path."
---

# Lightweight Diagram Persistence

## Summary

This session set out to understand why the diagram capability produced no simple durable diagram and why its development surface carried many scripts and artifacts. The existing contract made the complete governed publication bundle mandatory for ordinary creation, so request models, manifests, receipts, hashes, indexes, commit markers, and immutable revision directories accompanied every saved result. The capability now selects a lightweight basic profile by default and reserves the existing governed profile for explicit publication, claim-level traceability, immutable lineage outside Git, receipts, or promotion controls. A basic diagram is exactly `diagram.yml`, `diagram.mmd`, and `diagram.png`, with Git providing revision history. A self-documenting JSON Schema defines identity, ownership, structural kinds and constraints, business meaning, applicability, reader question, scope, optional source locators, status, dates, and tags. Deterministic validation and atomic persistence reject missing renders, extra members, invalid metadata, silent replacement, and staging inside the output root. The permanent example was migrated to the three-file shape and the redundant rendered demonstration and obsolete prompts were removed. Package validation, basic-profile tests, rendered-example inspection, the complete governed regression suite, generated runtime validation, and the final diff all passed; a fresh-agent test also exposed and closed a renderer-cache leak into the output root.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Evidence-Grounded Diagrams skill](../transmutations/evidence-grounded-diagrams/SKILL.md) | `is-part-of` | This session records a behavioral and persistence-contract iteration of that capability. |
| [Evidence-Grounded Diagrams Robot Talks session](2026-08-25-1629-evidence-grounded-diagrams-robot-talks.md) | `refines` | The lightweight default retains the earlier governed design as an explicit advanced profile instead of applying it universally. |
| [Final validation report](../transmutations/evidence-grounded-diagrams/development/PROMOTION-VALIDATION.md) | `derives-from` | The closing claims about package, quality-bar, workflow-gap, and regression status rely on this final deterministic report. |

## Files touched

- `.agents/skills/evidence-grounded-diagrams/README.md`
- `.agents/skills/evidence-grounded-diagrams/SKILL.md`
- `.agents/skills/evidence-grounded-diagrams/agents/openai.yaml`
- `.agents/skills/evidence-grounded-diagrams/references/artifact-lifecycle.md`
- `.agents/skills/evidence-grounded-diagrams/references/runbooks.md`
- `.agents/skills/evidence-grounded-diagrams/references/schema-guide.md`
- `.agents/skills/evidence-grounded-diagrams/schemas/diagram.schema.json`
- `.agents/skills/evidence-grounded-diagrams/scripts/persist_basic_diagram.py`
- `.agents/skills/evidence-grounded-diagrams/scripts/validate_diagram.py`
- `.agents/skills/evidence-grounded-diagrams/scripts/validate_skill_package.py`
- `.agents/skills/evidence-grounded-diagrams/templates/diagram.yml`
- `sessions/2026-08-26-1231-lightweight-diagram-persistence.md`
- `transmutations/evidence-grounded-diagrams/README.md`
- `transmutations/evidence-grounded-diagrams/SKILL.md`
- `transmutations/evidence-grounded-diagrams/agents/openai.yaml`
- `transmutations/evidence-grounded-diagrams/development/.gitignore`
- `transmutations/evidence-grounded-diagrams/development/PROMOTION-VALIDATION.md`
- `transmutations/evidence-grounded-diagrams/development/README.md`
- `transmutations/evidence-grounded-diagrams/development/REFLECTION.md`
- `transmutations/evidence-grounded-diagrams/development/TASK-MATRIX.md`
- `transmutations/evidence-grounded-diagrams/development/VALIDATION-EXPERIMENT.md`
- `transmutations/evidence-grounded-diagrams/development/VALIDATION.md`
- `transmutations/evidence-grounded-diagrams/development/example-diagrams/reviewer-draft-options/diagram.mmd`
- `transmutations/evidence-grounded-diagrams/development/example-diagrams/reviewer-draft-options/diagram.png`
- `transmutations/evidence-grounded-diagrams/development/example-diagrams/reviewer-draft-options/diagram.yml`
- `transmutations/evidence-grounded-diagrams/development/example-prompts/create-low.md`
- `transmutations/evidence-grounded-diagrams/development/example-prompts/forward-revise.md`
- `transmutations/evidence-grounded-diagrams/development/example-prompts/review-medium.md`
- `transmutations/evidence-grounded-diagrams/development/example-prompts/revise-complex.md`
- `transmutations/evidence-grounded-diagrams/development/render_mermaid.py`
- `transmutations/evidence-grounded-diagrams/development/run_validation_fixtures.py`
- `transmutations/evidence-grounded-diagrams/development/test_basic_profile.py`
- `transmutations/evidence-grounded-diagrams/development/test_rendered_example.py`
- `transmutations/evidence-grounded-diagrams/references/artifact-lifecycle.md`
- `transmutations/evidence-grounded-diagrams/references/runbooks.md`
- `transmutations/evidence-grounded-diagrams/references/schema-guide.md`
- `transmutations/evidence-grounded-diagrams/schemas/diagram.schema.json`
- `transmutations/evidence-grounded-diagrams/scripts/persist_basic_diagram.py`
- `transmutations/evidence-grounded-diagrams/scripts/validate_diagram.py`
- `transmutations/evidence-grounded-diagrams/scripts/validate_skill_package.py`
- `transmutations/evidence-grounded-diagrams/templates/diagram.yml`
