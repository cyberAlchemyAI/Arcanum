# Invoke Design: Language AI Substack

## Status

- Command: `invoke`
- Mode: `design`
- Phase status: `pass`
- Command surface: `.codex/commands/invoke.md`
- Mode contract: `spells/invoke/design.md`
- Target artifact: `REFINE-SEED-PROPOSAL.md`
- Source distill artifact: `stages/05-distill.md`
- Design artifact: `DESIGN-REDEFINITION.md`

## Design Summary

Invoke design converts the distill result into a plan-ready design/redefinition artifact. The selected unit is the **Draft-Readiness Composition Plan**, which is smaller than a full Substack draft and larger than isolated thesis, citation, or Arcanum-example fragments.

The design preserves stage ownership:

- prior seed, define, glossary, and layering artifacts are treated as source contracts;
- this stage writes only design-stage evidence;
- drafting remains downstream Task Session work;
- citation verification remains a bounded research gap, not an invented claim.

## Outputs

| Output | Status |
| --- | --- |
| `DESIGN-REDEFINITION.md` | produced |
| glossary consistency report | embedded in `DESIGN-REDEFINITION.md` |
| dependency/interface map | embedded in `DESIGN-REDEFINITION.md` |
| design transport report | this stage file |
| implementation layering | existing seed retained; design-ready evidence recorded without mutating seed |
| work-pack | n/a for design mode |

## Six-View Coverage

| View | Status | Evidence |
| --- | --- | --- |
| Context view | pass | `DESIGN-REDEFINITION.md#1-context-view` |
| High-level structure view | pass | `DESIGN-REDEFINITION.md#2-high-level-structure-view` |
| Low-level components view | pass | `DESIGN-REDEFINITION.md#3-low-level-components-view` |
| Workflow process view | pass | `DESIGN-REDEFINITION.md#4-workflow-process-view` |
| Decision flow view | pass | `DESIGN-REDEFINITION.md#5-decision-flow-view` |
| Dependency interface view | pass | `DESIGN-REDEFINITION.md#6-dependency-interface-view` |

## Decisions

- Selected `Draft-Readiness Composition Plan` as the design unit.
- Kept the thesis spine as an internal article claim structure rather than the whole refinement unit.
- Preserved `G1-harari-citation` as a source-integrity gap.
- Kept Arcanum as a translated live example, not a product pitch.
- Preserved `IMPLEMENTATION-LAYERING-SEED.md` without mutating upstream seed state.

## Validation

- Read `.codex/commands/invoke.md` and followed the embedded command contract.
- Read `spells/invoke/README.md` and `spells/invoke/design.md`.
- Verified command resolution with `tools/arcanum --resolve invoke`.
- Checked existing stage dependencies and confirmed stage 07 was blocked only because invoke design evidence was absent.
- Produced six design views and glossary consistency coverage.

## Gaps

Invoke gaps: none blocking.

Target artifact gaps:

- `G1-harari-citation`: verify before precise source claim, quotation, or attribution.
- `G2-public-translation`: draft must explain Arcanum terms in reader-facing language.
- `G3-meta-schema-example`: provide one concrete example or omit the term in first draft.

## Next Route

`refine` continuation: rerun or update `stages/07-interrogation-refine-design-review.md` against `DESIGN-REDEFINITION.md`, then continue to distill repair and `invoke plan` if review passes.
