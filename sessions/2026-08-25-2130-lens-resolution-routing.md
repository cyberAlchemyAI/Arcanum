---
tags: [lens-routing, resolution-routing, skill-installation, validation-evidence]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-25T21:30:50-03:00
updated_at: 2026-08-25T21:30:50-03:00
expires: 2026-10-24
decisions_made: true
contradictions_found: true
specs_updated:
  - transmutations/lens-router/SKILL.md
  - transmutations/resolution-router/SKILL.md
  - transmutations/low-resolution-explanation/SKILL.md
  - framework/SIGIL-DEVELOPMENT-WORKFLOW.md
  - framework/templates/sigil-template.md
  - registry/SIGILS.md
  - registry/SIGIL-DEPENDENCIES.tsv
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session established two reusable routing capabilities and their first writer while exposing promotion-evidence gaps that constrain canonical claims."
---

# Lens and Resolution Routing Implementation and Review

## Summary

The session turned the supplied Three Lenses material into a `lens-router` and separated it from a cumulative `resolution-router`. The first reader-facing writer, `low-resolution-explanation`, was implemented while medium and high writers remained explicitly unavailable and reserved. The three skills were installed in the repository with dependency closure, adapters, metadata, registry exposure, bootstrap support, schemas, semantic validators, and routing documentation. Independent governance and operability attacks followed by a skeptic produced a `FIX` review with five surviving `MAJOR` findings, while the ownership split, route mechanics, unavailable stopping, dependency closure, and installed-package fidelity survived. Current central validation passed for all six canonical/installed skill surfaces, the three semantic validators, metadata, dependencies, bootstrap syntax, and focused `orchestrate` tests. Broader Windows runs exposed CRLF-sensitive fixture digests, a hard-coded `bash` path that reaches the broken WSL installation, and a PowerShell UTF-16LE fixture path. The operator decided not to repair failures that are specific to Windows in this session. Four platform-neutral findings remain open around current-hash forward evidence, raw evidence preservation, lifecycle promotion enforcement, and mandatory ownership/input authoring surfaces.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Post-promotion review](../transmutations/resolution-router/development/validation/post-promotion-review/review.md) | `contextualizes` | This session records the implementation boundary, operator decision, and remaining work around the verified review verdict. |
| [Root Craft ledger](../.craft/ledger.yml) | `is-part-of` | The routing capability, review artifact, deferred Windows repair, and open platform-neutral gap are registered under the repository-level Craft space. |

## Open questions

- Should the four platform-neutral `MAJOR` findings be repaired before the routing trio is treated as canonically promoted?

## Next steps

1. Preserve the installed routing trio and do not alter Windows-specific failure paths under `DEC-ROUTING-WINDOWS-PORTABILITY-001`.
2. Decide whether to authorize bounded repairs for review findings F1, F2, F3, and F5.
3. If authorized, apply those repairs, rerun deterministic and forward tests against the exact current bytes, and commission a fresh post-fix review.

## Recommendation

Resolve whether to authorize F1, F2, F3, and F5 before making a canonical-promotion claim; the licensing fact is the independent `FIX` verdict and its evidence-binding findings.

## Files touched

- `transmutations/lens-router/`
- `transmutations/resolution-router/`
- `transmutations/low-resolution-explanation/`
- `.agents/skills/lens-router/`
- `.agents/skills/resolution-router/`
- `.agents/skills/low-resolution-explanation/`
- `registry/SIGILS.md`
- `registry/SIGIL-DEPENDENCIES.tsv`
- `registry/SIGIL-DEPENDENCIES.tsv.artifact.yml`
- `framework/SIGIL-DEVELOPMENT-WORKFLOW.md`
- `framework/templates/sigil-template.md`
- `tools/bootstrap_arcanum.sh`
- `tools/validate-artifact-metadata.py`
- `tools/validate-sigil-dependencies.py`
- `runtime/orchestrate/scripts/native_dispatch_driver.py`
- `runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py`
- `.agents/skills/orchestrate/`
- `transmutations/resolution-router/development/validation/post-promotion-review/confirmed-briefings.json`
- `transmutations/resolution-router/development/validation/post-promotion-review/review.dispatch.json`
- `transmutations/resolution-router/development/validation/post-promotion-review/review.md`
- `.craft/ledger.yml`
- `CRAFT.md`
- `sessions/2026-08-25-2130-lens-resolution-routing.md`
