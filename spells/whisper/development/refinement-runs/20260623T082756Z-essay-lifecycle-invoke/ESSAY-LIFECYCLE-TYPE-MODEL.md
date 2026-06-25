# Whisper Essay Lifecycle Type Model

- Target spell: `whisper`
- Model status: proposal-ready
- Source review: `WRITING-SEQUENCE-REVIEW.md`
- Owner decision: Spellcraft lifecycle acceptance required before canonical mutation

## Purpose

Whisper needs a small type layer that distinguishes a public essay from its draft
files. This keeps a series legible when one essay has multiple revisions and the
next essay is a sequel, not merely the next draft number.

## Core Distinction

| Concept | Meaning | Example |
| --- | --- | --- |
| `essay_artifact` | Stable public-writing unit with title, sequence identity, and lifecycle state. | `essay-002`, `Object, the First Abstraction` |
| `draft_artifact` | Mutable development artifact created during composition or revision. | `DRAFT-SUBSTACK-003.md` |
| `essay_revision` | Versioned relation between one essay and one draft/source state. | `essay-002.draft-001` |
| `series_relation` | Link between essays in a sequence. | `essay-002` consumes `essay-001` closing prompt |
| `publication_state` | Readiness of the essay for external release. | `draft`, `reviewed`, `publish_ready`, `published` |

## Minimum Field Set

```yaml
essay_artifact:
  series_id: language-as-toolmaking
  essay_id: essay-002
  essay_title: Object, the First Abstraction
  essay_slug: object-first-abstraction
  sequence_index: 2
  artifact_type: essay
  publication_state: draft
  current_revision_id: essay-002.draft-001

draft_artifact:
  draft_id: draft-substack-003
  revision_index: 1
  source_path: arcanum/spells/whisper/development/refinement-runs/20260623T045653Z-object-first-abstraction/DRAFT-SUBSTACK-003.md
  source_schema: arcanum/spells/whisper/development/refinement-runs/20260623T045653Z-object-first-abstraction/text-intent-substrate.yaml
  validation_state: pass

series_relation:
  previous_essay_id: essay-001
  relation_type: sequel
  bridge_contract: consumes_previous_closing_prompt
```

## Lifecycle States

| State | Meaning | Exit Gate |
| --- | --- | --- |
| `intent` | Author objective and transport exist, but no plan exists. | Text intent substrate exists. |
| `planned` | Composition plan exists. | Draft artifact exists. |
| `draft` | Draft text exists but is not accepted as an essay candidate. | Review or validator pass/flag is recorded. |
| `reviewed` | Review feedback has been consumed or explicitly deferred. | Revision or acceptance decision exists. |
| `essay_candidate` | Draft is stable enough to carry essay identity. | Title, sequence, and relation metadata exist. |
| `publish_ready` | Essay is ready for external publishing prep. | Citation, title, subtitle, sequence, and bridge checks pass. |
| `published` | Public copy is released or archived as released. | Publication path or URL is recorded. |
| `superseded` | A later revision or essay replaces this state. | Replacement reference is recorded. |

## Series Identity Decision

Current sequence proposal:

| Essay ID | Title | Current Draft Source | Publication State | Relation |
| --- | --- | --- | --- | --- |
| `essay-001` | The First Thing a Tool Needs Is a Name | `../20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md` | essay_candidate | opener |
| `essay-002` | Object, the First Abstraction | `../20260623T045653Z-object-first-abstraction/DRAFT-SUBSTACK-003.md` | draft | sequel to `essay-001` |

## Validation Rules

- An `essay_artifact` must have `essay_id`, `essay_title`, `series_id`,
  `sequence_index`, and `publication_state`.
- A `draft_artifact` must have a source path and revision index.
- A sequel must name its `previous_essay_id` and `bridge_contract`.
- Draft validation does not imply publish readiness.
- Publication readiness does not require renaming development files.
- Existing development draft paths remain provenance, not stable public identity.

## Integration Points

Whisper contract:

- Add `essay_artifact`, `essay_revision`, and `series_relation` to the artifact
  lifecycle contract.
- Add the same types to shared state or schema package guidance.
- Make the opening bridge rule for sequels explicit: name the prior essay title
  in public prose, not the prior development draft number.

Canonical schema package:

- Add these fields as optional extension families first.
- Treat `essay-001` and `essay-002` as examples until evidence proves the model
  should be base-required for all transports.

Validator:

- No immediate executable validator change is required for L0.
- Later validation can check that a sequel with `series_relation` names a prior
  essay and does not expose development-only draft labels in public opening text.

## Non-Goals

- Do not rename existing development draft files in this step.
- Do not create a public publishing directory before the contract admits it.
- Do not promote all Whisper transports to series-aware behavior.
- Do not make essay lifecycle fields mandatory for short copy or non-series text.
