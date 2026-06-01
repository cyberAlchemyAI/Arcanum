# Design Redefinition: Language AI Substack

## Status

- Invoke mode: `design`
- Phase status: `pass`
- Owner of this artifact: `invoke`
- Target lifecycle owner: `whisper` refinement run
- Target seed: `REFINE-SEED-PROPOSAL.md`
- Source distill artifact: `stages/05-distill.md`
- Stage output: `stages/06-invoke-design.md`

## Redefined Unit

The design unit is a **Draft-Readiness Composition Plan** for the Substack post, not the full article draft.

This redefines the seed from a broad article idea into a plan-ready composition surface that maps the reader-grounded hook, reference-checked Harari bridge, research context, core insight, Arcanum example, implications, and invitation into a first-draft SWU without writing prose in this stage.

## Source Contracts

| Source | Contract Role | Design Use |
| --- | --- | --- |
| `REFINE-SEED-PROPOSAL.md` | Seed and target artifact | Preserves thesis, target public, non-goals, schema substrate, research policy, and done criteria. |
| `INVOKE-DEFINE.md` | Approved define baseline | Supplies reader change, acceptance criteria, scope, and explicit citation policy. |
| `GLOSSARY.md` | Local term boundary | Keeps key terms local and prevents registry promotion by design stage. |
| `IMPLEMENTATION-LAYERING-SEED.md` | Layer boundary | Treats L1 as composition proof and L2 as draft proof. |
| `stages/05-distill.md` | Refinement unit decision | Selects Draft-Readiness Composition Plan and rejects full draft execution. |
| `REFERENCE-CHECK-HARARI.md` | Reference-checked bridge | Promotes shared fiction / cooperation as the first external frame after the reader-grounded opening while keeping exact quotes and page references gated. |

## Six Design Views

### 1. Context View

The refinement run is shaping a public Substack research post about language, generative AI, and personal symbolic code. The live example is Arcanum-style naming, aliasing, schema work, and workflow capture. The target reader is an AI-curious creative builder who should leave with a practical mental model, not an internal product pitch.

The design must preserve three boundaries:

- article planning is allowed;
- full draft execution is deferred to Task Session;
- precise Harari/Sapiens quotation or page attribution remains blocked until owned-copy verification.

### 2. High-Level Structure View

The article composition should use this sequence:

1. Hook: start from the concrete act of naming, language, or compressing a workflow.
2. Reference bridge: Harari's shared-fiction / cooperation frame widens the opening after the reader has a local handle.
3. Research context: generative AI makes this tool-making capacity more available and iterative.
4. Core insight: naming, aliases, schemas, and meta-schemas can function as personal symbolic code.
5. Arcanum example: show how aliases compress workflows and make reasoning reusable.
6. Implications: personal code broadens tool-making beyond software syntax and inherited jargon.
7. Invitation: ask readers what names, schemas, or workflows they would encode for themselves.

### 3. Low-Level Components View

| Component | Purpose | Constraint |
| --- | --- | --- |
| Thesis spine | Hold the article's central claim. | Must not overclaim that natural language replaces engineering. |
| Body-part composition plan | Convert the thesis into ordered sections. | Must remain plan-level; no full draft prose in invoke design. |
| Arcanum example bridge | Ground the claim in a concrete practice. | Must translate internal terms for public readers. |
| Reference bridge | Widen the reader-grounded hook through Harari's shared-fiction / cooperation frame without overclaiming. | Use `REFERENCE-CHECK-HARARI.md`; do not place before the opening hook; no direct quote or page citation until verified. |
| Draft SWU handoff | Prepare execution for Task Session. | Must be accepted by later plan/final synthesis before execution. |

### 4. Workflow Process View

```text
seed proposal
  -> invoke define baseline
  -> interrogation and research decision
  -> distill selects Draft-Readiness Composition Plan
  -> invoke design redefines the plan-ready article surface
  -> interrogation reviews design readiness
  -> repair distill if design review flags composition defects
  -> invoke plan emits task-session handoff
  -> lightweight reference-checked repair
  -> task-session drafts SWU-WHISPER-ARTICLE-001
```

Invoke design stops at the plan-ready composition surface. It does not draft, publish, verify external citations, or mutate the seed.

### 5. Decision Flow View

| Decision | Selected Option | Reason |
| --- | --- | --- |
| Design unit | Draft-Readiness Composition Plan | Smallest coherent unit that still recomposes into the article drafting SWU. |
| Article scope | Public research post with Arcanum as example | Preserves reader agency while avoiding a product pitch. |
| Research policy | Use checked paraphrase first; research only for direct quotation or page citation | Keeps local refinement moving without inventing evidence. |
| Stage ownership | Write a new design/redefinition artifact and stage output | Preserves seed ownership and unblocks stage 07 without editing prior stages. |
| Next route | `refine` continuation, then `invoke plan`/`task-session` | The existing refine route owns review/repair before execution. |

### 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| `DESIGN-REDEFINITION.md` | invoke design | refine design review, invoke plan | Six-view design and redefined plan-ready unit. |
| `stages/06-invoke-design.md` | invoke design | `stages/07-interrogation-refine-design-review.md` | Pass evidence for the blocked review dependency. |
| `GLOSSARY.md` | invoke define | invoke design, drafting SWU | Local definitions only; no canonical promotion. |
| `IMPLEMENTATION-LAYERING-SEED.md` | invoke define | invoke plan, task-session | L1 composition proof before L2 draft proof. |
| `REFERENCE-CHECK-HARARI.md` | lightweight refine | task-session | Reference-checked bridge and citation discipline. |
| `SWU-WHISPER-ARTICLE-001` | invoke plan, later | task-session | Draft execution unit; not executed here. |

## Composition Plan

| Body Part | Intent | Drafting Note |
| --- | --- | --- |
| Hook | Make language feel operational before naming AI or Arcanum. | Open from a reader-facing act of naming, language, or workflow compression. |
| Reference bridge | Make symbolic coordination legible before introducing Arcanum or AI. | After the hook, use Harari's shared-fiction / cooperation frame as paraphrase, not quote. |
| Research context | Frame generative AI as a collaborator in symbolic system building. | Avoid generic AI hype. |
| Core insight | State personal symbolic code clearly. | Keep metaphor grounded: language is not identical to software execution. |
| Arcanum example | Show aliases, schemas, and meta-schemas as live practice. | Translate `whisper`, `invoke`, and aliasing into reader-facing language. |
| Implications | Explain why non-engineers can build reusable symbolic tools. | Avoid condescension toward non-engineers. |
| Invitation | Give the reader a next mental action. | Ask what they would name, compress, or schema for themselves. |

## Pareto Dynamics Addendum

The approved Pareto dynamic is `two_tier`.

Global tournament selects the whole-text composition strategy across `resonance`, `relevance`, and `trajectory`. Part-level mini-tournaments run only when a part is delegated, revised, or fails validation. This preserves the article-level strategy while allowing localized repair for sections such as `introduction`, `reference_bridge`, or `invitation`.

Design implication: the next schema refresh should add `pareto_tournament` and `composition_parts` without treating every paragraph as an always-on optimization unit.

## Glossary Consistency

| Term | Design Status | Notes |
| --- | --- | --- |
| Personal symbolic code | consistent | Central design unit and article thesis. |
| Naming as compression | consistent | Should appear as a concrete example, not only a phrase. |
| Alias | consistent | Needs reader-facing translation before internal Arcanum examples. |
| Schema | consistent | Safe as public term when paired with a simple example. |
| Meta-schema | flag | Needs one concrete sentence or can be omitted from the first draft. |
| Whisper | consistent with boundary | Mention only as the shaping method if useful; avoid tool pitch. |
| Arcanum | consistent with boundary | Live example, not product positioning. |
| Harari/Sapiens reference | reference-checked, quote-gated | Use shared-fiction / cooperation paraphrase after the opening hook; do not quote or page-cite without verification. |

Glossary promotion status: no terms are promoted beyond this refinement run.

## Implementation Layering Seed

Existing seed retained: `IMPLEMENTATION-LAYERING-SEED.md`.

Design advances L1 from `pending` to design-ready evidence by defining the composition proof. The seed file is not mutated here; downstream refine synthesis or invoke plan can record acceptance after design review.

## Risks And Gaps

| Gap | Owner | Severity | Handling |
| --- | --- | --- | --- |
| `G1-harari-citation` | target artifact | non-blocker for design, blocker for direct quote/page citation | Use `REFERENCE-CHECK-HARARI.md` as the draft-safe bridge; verify exact edition/page only if quoting. |
| `G2-public-translation` | target artifact | non-blocker | Draft must translate Arcanum terms before relying on them. |
| `G3-meta-schema-example` | target artifact | non-blocker | Either provide one concrete example or omit meta-schema from the first draft. |

Invoke-specific gaps: none blocking. Design examples remain locally produced; canonical template promotion is not implied.

## Design Handoff

- Continue the refine loop through `stages/07-interrogation-refine-design-review.md`.
- If design review accepts this artifact, use it as input to repair distill and `invoke plan`.
- Execution should route to Task Session for `SWU-WHISPER-ARTICLE-001`, using `REFERENCE-CHECK-HARARI.md` as the first source anchor; invoke design must not draft the article.
