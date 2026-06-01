# Stage 05: Distill

Status: `pass`

## Smallest Coherent Unit

Selected SCU: `readability_dynamics_layer`

Definition:

A schema-governed layer that converts a draft into reader-processing units, each with a discourse role, rhythm role, visual treatment, validation expectations, and stable review anchors.

## Recomposition Proof

The unit recomposes into Whisper because it fills a gap between existing artifacts:

`draft_artifact -> readability_dynamics -> review_html -> review_payload -> revision_plan`

It does not replace:

- `text_intent_substrate`
- `composition_parts`
- `pareto_tournament`
- `draft_artifact`
- `review_html`

It adds:

- `beat_id`
- `discourse_move`
- `rhythm_role`
- `visual_treatment`
- `density_limits`
- `scan_path`
- `validation_rules`

## Rejected Alternatives

| Candidate | Verdict | Reason |
| --- | --- | --- |
| CSS-only readability pass | reject | Helps the page, but does not govern the writing process or prevent future walls. |
| Always split every paragraph | reject | Can create choppy prose and over-optimization; violates the existing two-tier Pareto spirit. |
| Full computational readability scoring first | defer | Valuable later, but too heavy before a simple schema and validator layer exists. |
| `readability_dynamics_layer` | select | Small enough to implement, strong enough to bridge schema, draft, review, and validation. |

