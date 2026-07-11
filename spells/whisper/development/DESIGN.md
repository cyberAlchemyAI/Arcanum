---
title: Whisper Design
status: draft
updatedAt: 2026-05-26
owner: Arcanum maintainers
scope: spell-design
---

# Whisper Design

## Source Decision

The first Whisper proof targets a Substack post for an Arcanum research group. Fundraising copy is the next transport and should shape the extension boundary, not the L0 implementation.

## Design Intent

Whisper treats text as a lifecycle artifact. A text starts as raw author intent, becomes an explicit substrate, receives a balanced primitive and technique selection, moves through a composition plan, becomes a draft, and is validated against the reason it exists.

The spell should support short copy, posts, articles, slide narratives, fundraising projects, and long-form works over time. The L0 proof remains narrow: produce a high-quality research-group Substack post substrate and plan.

## Current Smallest Coherent Unit

`TextIntentSubstrate`

Responsibility: capture the minimum constraints needed to construct and validate a meaningful text artifact.

This unit is smaller than a full writing workflow and larger than a style guide. It closes because it names inputs, outputs, structure, audience fit, author objective, validation checks, and extension pressure.

## Concept Layer Map

```text
meaningful text lifecycle
  -> Whisper spell
  -> transport-specific composition flow
  -> TextIntentSubstrate
  -> SCU cores
  -> fields and constraints
```

## Substrate Schema

```yaml
text_intent_substrate:
  metadata:
    substrate_version: "0.1"
    transport_type: substack_research_post
    next_transport_pressure: fundraising_copy
    artifact_status: proposal | draft | reviewed | final

  author_objective:
    primary_outcome: inform | clarify | persuade | inspire | recruit | fundraise | teach | invite
    desired_reader_change: string
    success_signal: string
    author_stance: exploratory | confident | provocative | reflective | invitational

  resonance_core:
    tone: string
    voice: string
    style_register: conversational | research_note | essayistic | manifesto | field_report
    emotional_residue: string
    value_signal: string
    forbidden_feels:
      - string

  relevance_core:
    target_public: string
    reader_state: unaware | curious | skeptical | aligned | expert | tired | urgent
    domain: string
    authority_mode: personal | research_group | technical | institutional | poetic | evidence_led
    assumed_knowledge:
      - string
    likely_objections:
      - string
    reader_reward: string

  trajectory_core:
    narrative_anchor: string
    transport_type: substack_research_post
    introduction_strategy: scene | question | claim | tension | field_note | direct_context
    body_parts:
      - hook
      - research_context
      - core_insight
      - implications
      - invitation_or_next_thread
    ending_strategy: reflection | invitation | synthesis | next_question
    max_characters: number
    must_include:
      - string
    must_avoid:
      - string

  technique_stack:
    candidates:
      - candidate_id: string
        attached_core: resonance | relevance | trajectory
        technique: string
        reason_selected: string
        tradeoff: string
    selected:
      - candidate_id: string

  validation:
    checks:
      - objective_fit
      - audience_fit
      - resonance_fit
      - structure_completeness
      - research_group_credibility
      - constraint_compliance
    review_mode: self_review | operator_review | audience_simulation | adversarial_review
```

## Substack Research Post Transport

### Purpose

Create a post that helps a research-group audience understand why an idea matters, what the group is learning, and what kind of conversation or continuation the author wants.

### Required Body Parts

| Part | Responsibility | Validation Question |
| ---- | -------------- | ------------------- |
| `hook` | Open a live tension, question, scene, or claim. | Would the target reader know why to keep reading? |
| `research_context` | Situate the idea in the group's work. | Is the post grounded without becoming internal-only? |
| `core_insight` | Name the central claim or discovery. | Can a reader repeat the point in one sentence? |
| `implications` | Show why the insight changes thinking or action. | Does the text move beyond describing itself? |
| `invitation_or_next_thread` | Leave a human continuation path. | Does the ending invite reflection, reply, or future work? |

### Default Constraints

| Field | Default |
| ----- | ------- |
| Length | 800-1600 words unless overridden |
| Introduction | required |
| Evidence | at least one concrete example, observed pattern, or research claim |
| Call to action | soft invitation, not conversion pressure |
| Style | clear, alive, and intellectually generous |

## Fundraising Extension Boundary

Fundraising copy should reuse the substrate but add fields only after Substack L0 proves the core flow.

Candidate extension fields:

```yaml
fundraising_extension:
  trust_basis: string
  proof_points:
    - string
  urgency_source: string
  donor_identity: string
  ask_shape: one_time | recurring | sponsorship | grant | patronage
  impact_path: string
  objection_handling:
    - string
```

The fundraising extension should not become a fourth SCU core by default. It is a transport-specific relevance and trajectory extension unless repeated use proves that trust/proof/ask mechanics need their own core.

## Live Presentation Extension Boundary

Live presentation is a candidate preset extension created from repeated
presentation quality failures. It does not change the three SCU cores. It adds
transport-owned surfaces and a strict pre-generation language audition.

The transport keeps `projected_copy`, `spoken_copy`, `speaker_notes`,
`interaction_prompt`, and `authoring_metadata` separate. The first generated
artifact is an opening/tension/reveal audition, not a complete deck. Full
generation remains blocked until an operator approves the voice.

This gate exists because source fidelity, schema validity, and browser validity
do not prove that projected or spoken language works in a room.

## Pareto-Aware Candidate Selection

Each candidate set must be scored across the three SCU cores:

| Axis | Question | Reject When |
| ---- | -------- | ----------- |
| Resonance | Does the voice carry the intended feeling and values? | It sounds polished but emotionally wrong. |
| Relevance | Does it fit the audience, domain, authority mode, and reader reward? | It is beautiful but addressed to the wrong public. |
| Trajectory | Does it move from opening tension to meaningful continuation? | It has style but no movement. |

The selected candidate should be non-dominated: no alternative improves one core without damaging another or increasing cost beyond the current transport's need.

## Lifecycle

```text
raw author intent
  -> transport selection
  -> one-question interrogation for blocker ambiguity
  -> TextIntentSubstrate
  -> SCU candidate tournament
  -> Pareto-aware consensus
  -> composition plan
  -> draft
  -> validation
  -> revision tasks or final
  -> learning residue
```

## Artifact State Machine

The lifecycle is implemented through schema-bearing artifacts. Tasks execute bounded transitions; they do not replace the schema.

| State | Responsibility | Produced By | Next States | Task Boundary |
| ----- | -------------- | ----------- | ----------- | ------------- |
| `text_intent_substrate` | Canonical intent, constraints, and three SCU cores. | intake, distill | `scu_candidate_set`, `composition_plan`, `validation_report` | Use direct Whisper intake unless the source packet is large enough to need context-builder. |
| `transport_schema` | Transport-specific body parts, constraints, validation checks, and publication expectations. | transport selection | `composition_plan`, `validation_report` | Use structured-interview only when transport or public is ambiguous. |
| `scu_candidate_set` | Candidate combinations of primitives and techniques across resonance, relevance, and trajectory. | distill tournament | `pareto_consensus` | Use distill tournament; do not turn each candidate into its own task. |
| `pareto_consensus` | Non-dominated selection that balances audience, feel, movement, and cost. | candidate tournament | `composition_plan` | Use decision-gate only for consequential disagreement. |
| `composition_plan` | Ordered construction plan for the text. | plan phase | `draft_artifact`, review | Use task-session when drafting will take multiple SWUs. |
| `draft_artifact` | The actual text produced from the plan. | draft phase | `validation_report`, revision | Use task-session for long drafting, source verification, or revisions. |
| `validation_report` | Pass/flag/block result against objective, audience, resonance, structure, and constraints. | validation | `learning_residue`, revision | Use review tasks only when the report creates actionable fixes. |
| `learning_residue` | Reusable lessons from this run. | validation, reflection | future composition runs | Promote durable terms to glossary/inventory only after repeated evidence. |

This answers the "just running tasks?" concern: the spell should run tasks only at transition points where a bounded unit of work is useful. The schema remains the memory and control surface.

## First Proof Scenario

Input shape:

```text
Write a Substack post for our research group about <topic>, aimed at <target readers>, leaving them with <desired reader change>.
```

Expected outputs:

- completed `TextIntentSubstrate`,
- selected SCU candidate set,
- Pareto consensus record,
- body-part composition plan,
- draft artifact or draft task handoff,
- draft readiness verdict,
- validation checklist result,
- learning residue for future research posts and fundraising copy.

## Deferred Complexity

- Full cross-transport schema library beyond the current Substack proof and
  candidate business-plan and live-presentation presets.
- Automated memory of all author voice preferences.
- Multi-agent writing room.
- Fundraising-specific validation.
- Publication platform integration.
- Long-form SWU decomposition.

## Interrogation Record

| Question | Answer | Decision |
| -------- | ------ | -------- |
| Should the first proof optimize for a general substrate or one high-value transport first? | Start with a Substack post for the research group; fundraising is next. | L0 selects `substack_research_post`; fundraising remains next transport pressure. |

## Readiness

Verdict: `pass` for spellcraft design draft, `flag` for implementation.

Flag reason: the first actual Substack run still needs a concrete topic, target reader, desired reader change, and source/evidence packet.

Next route: `task-session` can implement fixtures or `structured-interview-kits` can ask the next question for the first real post.
