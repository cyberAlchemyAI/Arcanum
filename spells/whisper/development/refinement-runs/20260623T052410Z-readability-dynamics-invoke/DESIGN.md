# Invoke Design - Whisper Readability Dynamics

Status: `flag`

Mode contract: `spells/invoke/design.md`

Flag reason: design is plan-ready, but direct source mutation remains gated on
Spellcraft lifecycle acceptance because the target is a reusable library spell.

## Design Objective

Add a non-breaking `readability_dynamics` layer to Whisper so drafts can be
checked for paragraph density, abstraction load, scan anchors, rhythm, and
discourse-move coverage while preserving existing review anchors and draft
validation behavior.

## Six-View Design

### 1. Context View

Whisper currently turns author intent into a substrate, composition plan, draft,
review HTML, validation report, and learning residue. The review HTML contract
anchors comments at paragraph-level `block_id` and `part_id` values.

The missing concern is reader-processing structure: whether each visible unit
has a clear role, whether dense paragraphs are grounded by examples or scan
anchors, and whether the draft gives readers enough rhythm to continue.

### 2. High-Level Structure View

```text
text_intent_substrate
  includes readability_dynamics defaults and validation rules

draft_artifact
  parsed into prose paragraphs by existing validator utilities

readability validation
  computes paragraph and term/density signals
  emits pass/flag/block without rewriting prose

review_html
  unchanged in L0; later SWU may render rhythm units
```

The L0 design does not change the renderer. It adds substrate fields and
validator checks that can prove the layer without changing draft content.

### 3. Low-Level Components View

| Component | Responsibility | L0 Behavior |
| --- | --- | --- |
| `text_intent_substrate.readability_dynamics` | Transport-specific readability config. | Optional section. Absence preserves current behavior. |
| `density_profile` | Bounds concepts, terms, abstractions, and examples per unit. | Validator reads defaults and emits flags. |
| `discourse_moves` | Names allowed prose moves. | Validator can check declared expected moves when present. |
| `validate-whisper-draft.py` | Existing draft validator. | Adds optional readability checks after current checks. |
| `build-whisper-review-html.py` | Existing review renderer. | No L0 change. |
| `validation_report` output | Current pass/block messaging. | Adds `FLAG` behavior for readability warnings if no blocking issues exist. |

### 4. Workflow Process View

1. Author or Invoke output adds `readability_dynamics` to a substrate.
2. Draft remains normal Markdown.
3. Validator loads the substrate and draft.
4. Existing validation runs first.
5. Readability validation runs only when the optional layer exists.
6. Readability failures default to `flag`, except review-anchor breakage, which
   is `block`.
7. Later review or drafting work uses flagged block numbers as revision targets.

### 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Is `readability_dynamics` absent? | Preserve current validator behavior. |
| Does a paragraph exceed max words? | Flag with paragraph index and configured limit. |
| Does a dense block introduce abstractions without an example or scan anchor? | Flag with reason and suggested repair route. |
| Does a proposed rhythm unit break `block_id`/`part_id` continuity? | Block. |
| Does the draft pass existing hard gates but fail readability checks? | Report `FLAG`, not `BLOCK`, unless configured otherwise. |

### 6. Dependency Interface View

| Interface | Dependency | Compatibility Rule |
| --- | --- | --- |
| Substrate YAML | PyYAML loader in validator | Optional section; old substrates parse unchanged. |
| Draft parser | `prose_paragraphs` in validator | Reuse existing paragraph extraction before introducing beat parsing. |
| Review payload | `block_id`, `part_id`, paragraph index, source line | L0 must not change payload shape. |
| Future renderer | `build-whisper-review-html.py` and template | Deferred to SWU-002. |
| Browser validation | Playwright / local server | Deferred to SWU-003. |

## Proposed Schema Shape

```yaml
readability_dynamics:
  layer_id: substack_research_post_readability_v1
  defaults:
    severity_default: flag
    max_words_per_paragraph: 120
    max_sentences_per_paragraph: 6
    max_consecutive_dense_paragraphs: 1
    require_scan_anchor_every_n_blocks: 3
  density_profile:
    max_new_terms_per_unit: 3
    max_unexplained_abstractions_per_unit: 2
    max_claims_before_example: 2
  scan_anchors:
    terms:
      - for example
      - try this
      - the point is
      - in practice
      - asked another way
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
    review_anchor_integrity: block
    density_limit_violation: flag
    scan_anchor_gap: flag
    abstraction_without_example: flag
```

## Validator Design

L0 adds a local readability check function to `validate-whisper-draft.py`.

Inputs:

- loaded schema,
- extracted prose paragraphs,
- full draft text.

Outputs:

- existing errors list for blocking failures,
- new warnings or flags for readability issues,
- printed `FLAG whisper draft validation` when only readability flags exist.

Rules:

- Existing hard errors remain blocking.
- Readability checks are skipped if the schema lacks `readability_dynamics`.
- `review_anchor_integrity` is defined for L0 but should only block once rhythm
  units are introduced in a later SWU.
- All messages cite paragraph indexes.

## Design Decisions

| ID | Decision | Rationale |
| --- | --- | --- |
| D1 | Optional schema section | Keeps existing substrates and drafts compatible. |
| D2 | Validator-only first SWU | Proves governance before renderer complexity. |
| D3 | Default readability severity is `flag` | Readability is important but should not block all draft proof until tuned. |
| D4 | No renderer change in L0 | Avoids mixing validation design with visual layout behavior. |
| D5 | Spellcraft before mutation | Target is a reusable spell lifecycle change. |

## Glossary Consistency

| Term | Define Status | Design Status |
| --- | --- | --- |
| `readability_dynamics` | proposed | consistent |
| `density_limits` | proposed | renamed internally to `density_profile` plus rule statuses |
| `scan_anchor` | proposed | consistent |
| `rhythm_unit` | proposed | deferred to renderer SWU |
| `review_anchor_integrity` | required | reserved as block rule for rhythm-unit introduction |

Result: `pass` with one deliberate deferral around `rhythm_unit`.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Thresholds become arbitrary. | False flags or style policing. | Keep default severity at `flag`; validate fixtures before promotion. |
| Readability checks punish good long-form prose. | Choppy writing. | Check density and grounding, not only word count. |
| Renderer rewrite starts too early. | Larger blast radius. | L0 is validator-only. |
| Spell lifecycle owner is bypassed. | Authority drift. | Next route is Spellcraft before Task Session mutation. |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | define evidence -> six-view design -> L0 plan | Every view consumes defined scope. | pass |
| `owner_boundary_check` | Invoke / Spellcraft / Task Session split | Design does not claim lifecycle completion. | pass |
| `artifact_contract_bridge` | substrate fields -> validator behavior | Every proposed field has validation meaning or is deferred. | pass |
| `validation_loop` | validator-first proof | L0 creates measurable proof before renderer changes. | pass |
| `recomposition_proof` | L0 validator -> full readability layer | L0 recomposes into later renderer and browser proof. | pass |
| `residue_ledger` | deferred renderer and threshold tuning | Deferred complexity is explicit. | pass |

## Distill Design Check

Status: `pass`

Selected unit: `readability_dynamics_layer`, narrowed for execution to
`SWU-WHISPER-READABILITY-001`.

Recomposition proof: optional substrate config plus validator checks preserve
the larger target because later renderer/browser work can consume the same layer
without changing the initial proof.

## Next Route

`plan`, then `spellcraft` for lifecycle acceptance before mutation-capable
execution.

