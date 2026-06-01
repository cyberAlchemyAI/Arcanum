# Whisper

## Identity

- Canonical ID: `whisper`
- Primary alias: `Whisper`
- Candidate aliases: `muse`, `scribe`, `echoform`, `voiceforge`, `utterance`, `quill`
- Scope: library

## Purpose

Whisper turns author intent into meaningful text through a governed composition lifecycle. It extracts a small text intent substrate, selects a balanced combination of narrative primitives and techniques, proposes a construction plan, drafts the text, validates the result, and preserves learning residue for future writing.

The first proof target is a Substack post for an Arcanum research group. Fundraising copy is the next planned transport, so the initial substrate must preserve an extension boundary for persuasion, proof, trust, and ask mechanics without building that transport in L0.

## Trigger Conditions

- The user wants to create or revise meaningful text, not just summarize existing material.
- The text needs a target public, tone, style, narrative anchor, structure, and validation criteria.
- The output can range from short copy to a post, article, slide narrative, fundraising page, or book section.
- The operator wants an interactive lifecycle with decisions, drafts, review, and iteration.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| ----- | ------------- | ------------- |
| `structured-interview-kits` | Ask one high-discrimination question when intent, transport, audience, or validation is ambiguous. | auto / interrogation |
| `distill` | Reduce broad author intent into the smallest coherent text intent substrate and prove recomposition into the full artifact. | standard or tournament |

## Optional Sigils

| Sigil | Use When | Notes |
| ----- | -------- | ----- |
| `decision-gate` | A consequential choice blocks the writing direction, such as audience priority, ethical stance, evidence standard, or call to action. | Route only blocker-level decisions. |
| `feature-glossary` | A domain vocabulary or recurring research language needs stabilization before drafting. | Useful for research group posts and technical articles. |
| `context-builder` | Source material, notes, or prior artifacts need compact selection before composition. | Keeps drafting grounded without ingesting everything. |
| `task-session` | A long text needs SWUs, review tasks, or multi-step development. | Use for books, series, large articles, or fundraising campaigns. |
| `experiment-harness` | The reusable spell needs validation examples across transports. | Required before broad promotion. |

## Prerequisites

- A raw author intent, topic, rough thesis, or source material exists.
- A target transport is selected or can be selected through one focused question.
- The operator accepts that L0 optimizes for `substack_research_post`; other transports remain schema extensions until proven.

## Shared State

| State | Owner | Updated By | Consumed By |
| ----- | ----- | ---------- | ----------- |
| `text_intent_substrate` | Whisper | intake, distill | candidate tournament, composition plan, validation |
| `transport_schema` | Whisper | transport selection | composition plan, validation |
| `scu_candidate_set` | Whisper | distill tournament | Pareto consensus |
| `composition_plan` | Whisper | plan phase | draft phase, review |
| `draft_artifact` | Whisper | draft phase | validation, revision |
| `learning_residue` | Whisper | validation, reflection | future composition runs |

## Artifact Lifecycle Contract

Whisper treats composition as an artifact state machine, not as a loose sequence of writing tasks. Each artifact has a phase owner, a gate, and downstream consumers.

| Artifact | Category | Produced In | Feeds | Gate |
| -------- | -------- | ----------- | ----- | ---- |
| `text_intent_substrate` | intent substrate | intake, distill | candidate tournament, composition plan, validation | transport, objective, audience, SCU cores, and constraints are explicit |
| `transport_schema` | transport contract | transport selection | composition plan, validation | required body parts, length, evidence, introduction, ending, and CTA policy are named |
| `scu_candidate_set` | primitive/technique tournament | distill tournament | Pareto consensus | each candidate combines resonance, relevance, and trajectory rather than optimizing one category repeatedly |
| `pareto_consensus` | selection decision | candidate tournament | composition plan | selected set is non-dominated across resonance, relevance, trajectory, and cost |
| `composition_plan` | construction plan | plan phase | draft phase, review | body parts, sequence, anchor, examples, and validation checklist are ready |
| `draft_artifact` | text artifact | draft phase | validation, revision | draft exists, names its schema source, and preserves known citation gaps |
| `review_html` | review surface | review phase | revision, learning residue | every draft can be rendered into stable comment blocks whose agent payload preserves `block_id`, `part_id`, selected text, and requested change mode |
| `validation_report` | quality gate | validation | revision, learning residue | checks pass, flag, or block with actionable reasons |
| `learning_residue` | reusable memory | validation, reflection | future composition runs | distinguishes observed lessons from canonical author voice or transport rules |

`task-session` is used only when one artifact needs bounded execution, such as drafting the article, verifying a source gap, or revising from review notes. The spell itself remains responsible for the lifecycle, gates, and artifact transitions.

## Review HTML Contract

Every reviewable draft should be convertible into a Whisper review HTML page using `spells/whisper/templates/draft-review-base.html` and `spells/whisper/tools/build-whisper-review-html.py`.

The review page is the operator-facing surface for comments. It anchors each paragraph to a stable `block_id`, maps the block to a Whisper composition `part_id`, stores comments in browser `localStorage`, and exposes `window.WhisperReview.getAgentPayload()` for Playwright extraction.

Agent revision requests should consume the exported payload rather than vague prose-only feedback. Each comment carries:

- `block_id` and `part_id`,
- paragraph index and source line,
- selected text when available,
- issue type,
- requested change mode,
- priority,
- comment text,
- original block text.

This keeps review feedback addressable enough for the next Whisper revision pass to offer alternatives, apply a targeted change, or route a part-level mini-tournament when the comment says the local section failed.

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| ----- | ----- | ----- | ------ | ---- | -------------- |
| 1. Transport and intent intake | `structured-interview-kits` | raw author intent | selected transport and blocker decisions | transport, objective, target public, and success signal are named | Ask one focused question; block only when target text cannot be identified. |
| 2. Substrate distillation | `distill` | intake record | `text_intent_substrate` with resonance, relevance, and trajectory cores | each core has named values and recomposes into the target artifact | Flag unsupported assumptions; route consequential uncertainty to `decision-gate`. |
| 3. SCU candidate tournament | `distill` | substrate and transport schema | candidate primitive/technique sets | one balanced candidate preserves Pareto trade-offs across all three cores | Keep stable disagreement in the ledger; do not optimize only tone/style. |
| 4. Composition plan | Whisper | selected candidate set | body-part plan, template, validation checklist | plan includes introduction policy, narrative anchor, sections, ending, and constraints | Revise plan if it violates transport schema. |
| 5. Draft and review | Whisper | composition plan | draft text and review notes | draft passes constraint, audience, resonance, and structure checks | Produce revision tasks or return flag when quality is below target. |
| 6. Learning residue | Whisper | final or flagged draft | reusable lessons, technique results, unresolved gaps | residue distinguishes observed result from canonical truth | Defer promotion to inventory or glossary owners when durable knowledge appears. |

## SCU Core Model

Whisper uses three Smallest Coherent Unit cores:

| Core | Responsibility | Typical Fields |
| ---- | -------------- | -------------- |
| `resonance_core` | Define the felt meaning the text should carry. | tone, voice, style register, emotional residue, value signal, forbidden feels |
| `relevance_core` | Define why this text belongs to this audience and domain. | target public, reader state, domain, authority mode, assumptions, objections |
| `trajectory_core` | Define the movement the text performs. | objective, transport type, narrative anchor, structure, introduction, body parts, ending, length |

Each viable candidate must include one coherent selection from all three cores. Advanced mode may test multiple candidates per core, but L0 prevents three tone variants from crowding out audience fit or structure.

## Transport Sequence

| Order | Transport | Status | Reason |
| ----- | --------- | ------ | ------ |
| 1 | `substack_research_post` | selected L0 proof | Forces clarity, voice, research-group relevance, argument structure, and reflective ending without immediate conversion pressure. |
| 2 | `fundraising_copy` | next extension | Adds trust, proof, urgency, ask mechanics, and donor psychology after the base substrate works. |

## Local Customization

- Spell root: `spells/whisper/` for this reusable library spell.
- Development artifacts: `spells/whisper/development/`.
- Gate strictness: standard for L0, strict for blocker audience/objective decisions.
- Interaction mode: guided-auto, with one-question interrogation when a decision changes the draft.
- Runtime execution: long model-backed work should use native skill/subagent execution with a receipt, or `tools/arcanum --exec --adapter local-skill --timeout <seconds> ...` as a deterministic handoff. Explicit legacy adapters are opt-in.

## Observability

Record spell-level telemetry when `.arcanum/observability/` exists:

- spell name and transport,
- phases attempted,
- sigils invoked,
- SCU cores selected,
- candidate set count,
- gates passed, flagged, or blocked,
- draft artifact status,
- validation result,
- user corrections,
- learning residue and next transport pressure.

## Output Contract

Return:

```markdown
## Whisper Result

- Spell: whisper
- Transport: <transport id>
- Objective: <author objective>
- Target public: <audience>
- SCU cores: <resonance | relevance | trajectory summary>
- Candidate selected: <candidate id and rationale>
- Composition plan: <sections or body parts>
- Draft status: pass | flag | block
- Validation: <checks and result>
- Learning residue: <durable lessons or none>
- Next route: revise | publish-prep | task-session | decision-gate | deferred
```
