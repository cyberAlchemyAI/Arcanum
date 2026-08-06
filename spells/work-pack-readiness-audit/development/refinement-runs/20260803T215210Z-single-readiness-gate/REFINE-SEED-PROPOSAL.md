# Refine Seed Proposal

- Target: `arcanum/spells/work-pack-readiness-audit` and its Task Session admission handoff
- Seed needed: `yes`
- Source context: canonical audit runner, v1 schemas, Task Session mutation-admission verifier, and the Anime.js readiness report
- Write scope: this refinement-run folder only
- Done criteria: define a backward-compatible one-audit contract; prove that missing per-SWU material cannot authorize mutation; produce a non-executed implementation plan with fixtures and owner boundaries
- Validation surface: Dispatch Spec validation, JSON validation, selector coverage, reviewer counterexamples, Distill recomposition, and final artifact/index checks
- Preset: `standard`
- Loop count: canonical ten-stage loop with two Distill rounds and one repair pass
- Research: `no-research`
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass`
- Dispatch techniques: `sequence`, `frame_handoff`, `validation_loop`, `owner_boundary_check`, `observability_grouping`, `dialectic`, `toy_game`, `recomposition_proof`
- Technique overlays selected: `baseline_sequence`, `dialectic_for_tension`
- Technique overlays considered but not selected:
  - `tournament_for_alternatives`: three independent design tracks are unnecessary; two alternatives can be rejected inside Standard Distill.
  - `xray_for_hidden_structure`: the duplicated gates are explicit in the canonical runner and Task Session verifier.
  - `protected_context_for_external_or_sensitive_evidence`: the run is local-only and public-safe.
- Planned execution stages: the canonical Context Builder → Invoke Define → Interrogation → research decision → Distill → Invoke Design → Interrogation → Distill Repair → Invoke Plan → final synthesis sequence
- Runtime default: parent-owned native capabilities plus one approved read-only admission-boundary critic
- Runtime eligibility: `pass`
- Blocked runtime fields: none
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Result artifact: `RESULT.md`
- Recommended next route: `sigil-development --update work-pack-readiness-audit`, followed by one explicitly selected Task Session SWU

The proposal does not authorize canonical implementation, generated-mirror synchronization, or a project Task Session.
