# Invoke Define - Whisper Readability Dynamics

Status: `pass`

Mode contract: `spells/invoke/define.md`

## Intent Record

The target is a Whisper spell revision candidate: add a first-class
`readability_dynamics` layer so paragraph information density, abstraction load,
scan path, discourse move, and review granularity can be governed by substrate
and validation instead of discovered only after a human says the prose feels like
a wall.

The immediate authoring objective is not to mutate Whisper. It is to define the
change clearly enough for Spellcraft to validate the spell lifecycle boundary and
for Task Session to execute one bounded SWU later.

## Source Evidence

| Source | Evidence Used |
| --- | --- |
| `arcanum/spells/whisper/README.md` | Whisper owns `text_intent_substrate`, `draft_artifact`, `review_html`, `validation_report`, and review payload anchors. |
| `arcanum/spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/RESULT.md` | Existing refinement selected `readability_dynamics` between `draft_artifact` and `review_html` and named `density_limits`, `scan_path`, and validation fields. |
| `arcanum/spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/RUNTIME-HANDOFF.md` | Existing handoff recommends `SWU-WHISPER-READABILITY-001` as non-breaking schema plus validator-only checks. |
| `arcanum/spells/whisper/tools/validate-whisper-draft.py` | Current validator checks opening contract, Pareto completeness, required terms, and length, but not readability dynamics. |
| `arcanum/spells/whisper/tools/build-whisper-review-html.py` | Current renderer parses Markdown into paragraph review blocks. |

## Problem Definition

Whisper can already express body-part responsibilities and validate some prose
constraints, but it does not govern the reader-processing density inside or
across paragraphs. The same paragraph-level review block is used for hooks,
claims, bridges, definitions, examples, concessions, and invitations.

That makes a dense paragraph look like a styling problem, even when the actual
issue is a missing discourse move, too many abstractions without an example, or
no scan anchor before the next conceptual turn.

## Defined Capability

`readability_dynamics` is a transport-aware, source-stable, validator-backed
layer that annotates prose with rhythm and density expectations while preserving
the existing Whisper lifecycle:

```text
text_intent_substrate
  -> composition_plan
  -> draft_artifact
  -> readability_dynamics
  -> review_html
  -> review_payload
  -> revision_plan
```

## Scope

### Included In This Define

- Define `readability_dynamics` as a Whisper artifact layer.
- Keep the first implementation non-breaking and validator-only.
- Treat paragraph density as one dimension of readability, not the whole model.
- Preserve stable `block_id`, `part_id`, paragraph index, source line, and review
  payload compatibility.
- Route spell lifecycle acceptance through Spellcraft before source mutation.

### Excluded From This Define

- No immediate edits to `spells/whisper/README.md`.
- No renderer rewrite in the first SWU.
- No browser validation or review-page regeneration in the first SWU.
- No full academic readability metric engine.
- No automatic public promotion of a new canonical Whisper contract.

## Minimum Schema Concept

```yaml
readability_dynamics:
  layer_id: substack_research_post_readability_v1
  defaults:
    max_words_per_paragraph: 120
    max_consecutive_dense_paragraphs: 1
    require_scan_anchor_every_n_blocks: 3
  density_profile:
    max_new_terms_per_unit: 3
    max_unexplained_abstractions_per_unit: 2
    max_claims_before_example: 2
  discourse_moves:
    allowed:
      - hook
      - claim
      - bridge
      - example
      - contrast
      - concession
      - implication
      - invitation
      - pause
  validation_rules:
    severity_default: flag
    preserve_review_anchor_integrity: block
```

## Glossary

| Term | Definition | Status |
| --- | --- | --- |
| `readability_dynamics` | Whisper layer that governs rhythm, density, scan path, and discourse movement between draft and review. | proposed |
| `density_limits` | Transport-specific thresholds for claims, terms, abstractions, examples, and paragraph/beat size. | proposed |
| `abstraction_load` | Amount of conceptual material introduced before grounding, example, or pause. | proposed |
| `scan_anchor` | A visible reader handle such as a question, micro-heading, transition, callout, or example. | proposed |
| `rhythm_unit` | A reviewable reading beat that may be a paragraph or a child unit inside a paragraph. | proposed |
| `review_anchor_integrity` | Guarantee that new readability units do not break existing review payload addressing. | required |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | define -> design -> plan -> Spellcraft review | Each later artifact consumes explicit prior evidence. | pass |
| `scu_swu_reduction` | first executable boundary | First SWU is non-breaking schema plus validator checks only. | pass |
| `owner_boundary_check` | Invoke vs Spellcraft vs Task Session | Invoke authors artifacts only; Spellcraft owns spell lifecycle acceptance; Task Session owns later execution. | pass |
| `artifact_contract_bridge` | schema and validator contracts | Proposed fields map to validation behavior and review payload constraints. | pass |
| `residue_ledger` | renderer/browser/future metric gaps | Deferred scope remains visible and owned. | pass |
| `concrete_path_evidence` | all source claims | Evidence cites concrete repository paths. | pass |

## Template Selection

Selected template family: standalone Invoke artifacts with DomainSpec-style
companions.

Reason: the target is a library spell revision, not a new product module. The
prebuilt standalone `implementation-layering` and `work-pack` templates fit the
planning boundary without requiring a full DomainSpec module scaffold.

## Distill Sanity

Status: `pass`

The prior refinement already selected `readability_dynamics_layer` as the
smallest coherent unit. This define preserves that unit and narrows the first
executable step to `SWU-WHISPER-READABILITY-001`.

## Decisions

- Use `readability_dynamics`, not paragraph-length policing.
- Make the first SWU validator-only and non-breaking.
- Keep renderer behavior as a later SWU.
- Route lifecycle acceptance to Spellcraft before mutation.

## Unresolved Gaps

| Gap | Owner | Route |
| --- | --- | --- |
| Exact default thresholds may need examples across transports. | Whisper / Experiment Harness | Validate with fixtures after SWU-001. |
| Renderer beat support is useful but not part of the first mutation. | Whisper / Task Session | Defer to SWU-002 after schema and validator proof. |
| Canonical spell contract update requires lifecycle acceptance. | Spellcraft | Review this packet, then authorize or revise downstream work-pack. |

