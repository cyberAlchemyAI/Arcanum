# x-ray Reader On-Ramp Research

## Status

Status: pass

Research mode: local-first repository research

Target: improve `x-ray` explanations so generated HTML pages can teach a reader who does not already know the target vocabulary.

## Reusable Techniques Found

### 1. Feature Language Before Formal Terms

Source:

- `/home/vrondelli/projects/domainspec-core/projects/whisky-doses/domainspec/templates/glossary.md`
- `/home/vrondelli/projects/domainspec-core/projects/body-war/domainspec/templates/glossary.md`

Reusable rule:

Put a short feature-language glossary before formal concept rows. Explain important words in ordinary product language and link each formal term back to its authoritative source.

Use in `x-ray`:

- Add a `concept_glossary` or `reader_terms` area to every generated page.
- Include plain-language terms for labels that appear in diagrams.
- Keep local glossary entries explanatory, not authoritative.

### 2. Formal Meaning Plus Plain-Language Intuition

Source:

- `/home/vrondelli/projects/domainspec-core/arcanum/arcana/definitions-governance/SKILL.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/definitions/DEFINITIONS.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/definitions/DEFINITIONS-INDEX.md`

Reusable rule:

For critical concepts, keep the minimum interpretation package together:

- formal or local definition,
- operational interpretation,
- plain-language intuition,
- boundary or misuse warning,
- source or consumer links.

Use in `x-ray`:

- Treat important lane labels as local concepts with a small interpretation package.
- Use `Plain-language intuition` for newcomer text.
- Use `Boundary` or `misuse warning` for concepts that are easy to overread.
- Avoid promoting x-ray-local terms into global definitions.

### 3. Reader Stories As Section Obligations

Source:

- `/home/vrondelli/projects/domainspec-core/implementation/mars/templates/paper-stories-template.md`

Reusable rule:

Write each section as a reader story:

```text
As a [reader type], I want [section outcome], so that [why it matters].
Given [inputs], when I read [section], then I should understand [expected outcome].
```

Use in `x-ray`:

- Each major page section or layer should have a reader outcome.
- Validation can check that every layer has a `reader_should_understand` note.

### 4. Notation Bridge With Misuse Warning

Source:

- `/home/vrondelli/projects/domainspec-core/arcanum/research/shared-notation-glossary.md`

Reusable rule:

When a symbol, label, or formal expression arrives before the reader has a mental model, preserve the original symbol but add:

- generic reading,
- how to read it aloud,
- safe analogy,
- misuse warning,
- local meaning when overloaded.

Use in `x-ray`:

- For technical diagrams, arrows, state labels, function-like names, and compact badges, include a local notation or label bridge.
- Explain arrows by what moves or changes, not only by naming source and target nodes.

### 5. Opening Contract And Part Responsibilities

Source:

- `/home/vrondelli/projects/domainspec-core/arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`
- `/home/vrondelli/projects/domainspec-core/arcanum/spells/whisper/tools/validate-whisper-draft.py`

Reusable rule:

An explanation can enforce its opening and body responsibilities with schema-backed validation:

- target public,
- assumed knowledge,
- reader reward,
- required body parts,
- opening contract,
- forbidden starts,
- draft-level required terms,
- failure message.

Use in `x-ray`:

- Add a page-level `reader_contract`.
- Require a concrete reader-facing opening before dense lane details.
- Give each lane a responsibility, not just a handle.
- Add validator checks after the example schema grows.

### 6. Readability Dynamics

Source:

- `/home/vrondelli/projects/domainspec-core/arcanum/spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/RESULT.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/stages/06-invoke-design.md`

Reusable rule:

Readable writing should be a first-class artifact layer. Model beats, blocks, discourse moves, visual treatments, density limits, scan anchors, and validation rules.

Use in `x-ray`:

- Add an optional `readability_dynamics` layer for generated HTML examples.
- Check paragraph density, missing examples, scan-anchor spacing, and whether abstract terms have local examples.
- Prefer micro-headings, example boxes, question lines, and transition lines over dense explanatory walls.

### 7. Existing x-ray Risk: Visual Complexity Can Outrun Explanation

Source:

- `/home/vrondelli/projects/domainspec-core/arcanum/arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/stages/10-final-interrogation-and-synthesis.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/arcana/x-ray/development/REFINE-SEED.md`

Reusable rule:

The visual model must remain an explanation surface. Text should explain what the reader is looking at, reveal assumptions, connect visual pieces, and allow deeper inspection without turning the page into a static report.

Use in `x-ray`:

- Make visual layer clarity a validation target.
- Require each diagram layer to name what the reader should notice.
- Keep Mermaid, Three.js, and other adapters subordinate to explanation clarity.

## Recommended x-ray Shape

Add these candidate fields after one example proves the shape:

```yaml
reader_contract:
  reader_baseline: newcomer | working-reader | expert | unknown
  target_public: string
  assumed_knowledge: []
  reader_reward: string
  opening_contract:
    must_start_with: []
    must_not_start_with: []
    failure_message: string

reader_terms:
  - term: string
    plain_meaning: string
    why_it_matters: string
    source_or_lane: string
    authority: explanatory | source-backed | inferred
    misuse_warning: string

layer_reader_outcomes:
  - layer: surface | properties | components | internal_dependencies | external_dependencies | flow | lifecycle | risk_questions
    as_a_reader: string
    should_understand: string
    because_it_matters_for: string

readability_dynamics:
  max_words_per_paragraph: 120
  max_consecutive_dense_blocks: 1
  require_scan_anchor_every_n_blocks: 3
  allowed_visual_treatments:
    - micro_heading
    - example_box
    - question_line
    - transition_line
```

## Recommendation

Do not only keep the current `reader-onramp` prose rule. Promote the reusable writing techniques into the next x-ray example and validator pass:

1. Add reader contract and local terms to the lane model candidate.
2. Update the order-ingestion example HTML so diagram labels have adjacent explanations.
3. Extend validation to check baseline, reader terms, and layer outcomes.
4. Keep all new reader terms x-ray-local until Definitions Governance explicitly promotes anything.
