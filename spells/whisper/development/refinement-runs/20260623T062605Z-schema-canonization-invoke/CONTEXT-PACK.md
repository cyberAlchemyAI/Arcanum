# Context Pack - Whisper Schema Canonization Plan

- Task: plan canonicalization of Whisper schema artifacts
- Mode: standard
- Strict coverage: pass
- Output: Invoke plan packet
- Handoff pack: none

## Planning Objective

Whisper now has schema-relevant artifacts in development refinement runs:

- `text-intent-substrate.yaml` with the operational `substack_research_post`
  substrate, Pareto tournament, composition parts, draft artifact, validation,
  and learning residue.
- `WHISPER-SCHEMA.md` as a human-readable schema explanation.
- `REFRESH-REPORT.md` and `REFRESH-PATCH-PROPOSAL.md` as refresh evidence for
  the two-tier Pareto schema refresh.
- `TASK-SESSION-PARETO-REPORT.md` as execution evidence for Pareto validator
  support.
- `readability-dynamics-fixture.yaml` and
  `TASK-SESSION-READABILITY-REPORT.md` as execution evidence for optional
  `readability_dynamics`.
- `20260623T045653Z-object-first-abstraction/text-intent-substrate.yaml` as a
  current downstream substrate candidate that should be checked against any
  canonical schema surface.

The missing stable surface is a canonical Whisper schema package under
`arcanum/spells/whisper/`, separate from development-only evidence.

## Included Evidence

| Source | Why Included | Planning Use |
| --- | --- | --- |
| `arcanum/spells/whisper/README.md` | Canonical Whisper spell contract and artifact lifecycle model. | Defines owner, artifact names, and promotion boundary. |
| `20260526T204134Z-language-ai-substack/text-intent-substrate.yaml` | Most complete machine-readable substrate. | Candidate source for canonical schema fields and example fixture. |
| `20260526T204134Z-language-ai-substack/WHISPER-SCHEMA.md` | Human-readable schema narrative. | Candidate source for canonical schema README language. |
| `20260526T204134Z-language-ai-substack/REFRESH-REPORT.md` | Refresh evidence and delta summary for Pareto schema drift. | Shows how refresh artifacts prepared schema/validator changes. |
| `20260526T204134Z-language-ai-substack/TASK-SESSION-PARETO-REPORT.md` | Evidence that Pareto schema enforcement was implemented. | Promotion evidence for `pareto_tournament` and `composition_parts`. |
| `20260623T052410Z-readability-dynamics-invoke/TASK-SESSION-READABILITY-REPORT.md` | Evidence that optional readability validation now works. | Promotion evidence for `readability_dynamics` as candidate schema layer. |
| `20260623T045653Z-object-first-abstraction/text-intent-substrate.yaml` | Newer downstream substrate. | Compatibility fixture for canonical schema review. |
| `arcanum/spells/whisper/tools/validate-whisper-draft.py` | Current executable validator. | Validation surface and drift detector for canonical schema examples. |

## Findings

1. Whisper has canonical lifecycle language but no canonical schema home.
2. Development artifacts contain both source evidence and candidate canonical
   language, so copying them directly would preserve run-local assumptions.
3. Pareto schema support has stronger evidence than readability dynamics because
   Pareto is already part of the main substrate and validator contract.
4. `readability_dynamics` is implemented as optional validator behavior but still
   needs owner review and broader fixture evidence before full spell promotion.
5. The next post substrate should become a compatibility fixture, not a
   canonical source by itself.

## Planning Assumptions

- Stable schema artifacts should live under `arcanum/spells/whisper/schemas/`.
- Canonical schema files must be public-safe, transport-neutral where possible,
  and free of run-local article-specific source context unless stored as examples.
- Invoke can author this plan, but Spellcraft owns Whisper lifecycle acceptance.
- Task Session should execute one selected SWU at a time.
- Experiment Harness or equivalent fixture evidence is required before broad
  canonical promotion claims.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Draft prose artifacts | Useful as examples, but not canonical schema authority. |
| Review HTML artifacts | Renderer/review surface is related but not first canonical schema package scope. |
| `.agents/skills/whisper/` | Generated runtime surface, not canonical source. |
| Parent private repo artifacts outside `arcanum` | Whisper canonicalization targets the public spell submodule. |
