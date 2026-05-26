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
  -> SRU cores
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

The fundraising extension should not become a fourth SRU core by default. It is a transport-specific relevance and trajectory extension unless repeated use proves that trust/proof/ask mechanics need their own core.

## Pareto-Aware Candidate Selection

Each candidate set must be scored across the three SRU cores:

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
  -> SRU candidate tournament
  -> Pareto-aware consensus
  -> composition plan
  -> draft
  -> validation
  -> revision tasks or final
  -> learning residue
```

## First Proof Scenario

Input shape:

```text
Write a Substack post for our research group about <topic>, aimed at <target readers>, leaving them with <desired reader change>.
```

Expected outputs:

- completed `TextIntentSubstrate`,
- selected SRU candidate set,
- body-part composition plan,
- draft readiness verdict,
- validation checklist result,
- learning residue for future research posts and fundraising copy.

## Deferred Complexity

- Full cross-transport schema library.
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
