# Stage 06: Invoke Redefine / Design

Status: `pass`

## Design Overview

The candidate package should be shaped as:

```text
development/user-guide/
  -> User Learning Ledger candidate
  -> Guide Interaction Receipt candidate
  -> CyberAlchemy install-game candidate
  -> Concept library seed candidate
  -> Validation gates
```

Future canonical package candidates:

```text
arcana/user/
spells/guide/
spells/cyberalchemy-install-game/
libraries/concepts/
```

Those paths are candidates only in this refinement.

## User Ledger Row Families

| Row Family | Purpose |
| --- | --- |
| `profile_seed` | Initial self-declared domains, roles, projects, interests, and learning goals. |
| `domain_anchor` | Domains the user can use as explanation source domains, such as sales, music, construction, software, science, finance, writing. |
| `vocabulary_preference` | Preferred words, disliked words, aliases, native-language notes, and style preferences. |
| `concept_state` | Per-concept status: unknown, exposed, partial, clarified, practiced, transferable, mastered, stale. |
| `guide_receipt` | One explanation/clarification interaction and its observed outcome. |
| `bridge_pattern` | Source-domain to target-domain mappings that worked, with mismatch warnings. |
| `glossary_entry` | User-local mastered definitions with evidence and review notes. |
| `residue` | Confusions, failed analogies, open questions, and concepts needing a different route. |
| `consent_visibility` | What can be stored, shown, exported, reset, or promoted after review. |

## Guide Interaction Receipt Fields

Minimum fields:

- `receipt_id`
- `timestamp`
- `target_concept`
- `target_domain`
- `source_domain_anchor`
- `guide_section_id`
- `strategy`
- `analogy_or_metaphor_used`
- `attempt_count`
- `friction_type`
- `user_signal`
- `evidence_type`
- `evidence_summary`
- `ledger_update_proposal`
- `user_confirmation`
- `promotion_boundary`

## Guide Strategy Set

| Strategy | When To Use |
| --- | --- |
| `domain_bridge` | The user knows a source domain that maps partially to the target. |
| `contrast_pair` | The user confuses two nearby concepts. |
| `concept_ladder` | The user needs concrete -> meta -> abstract movement. |
| `self_explanation_prompt` | The user has seen an example but needs to connect it to principles. |
| `retrieval_prompt` | The user says it is clear and the system needs mastery evidence. |
| `failure_case` | The user needs to see what breaks when a primitive is missing. |
| `mapping_limits` | The analogy is useful but dangerous if taken literally. |

## CyberAlchemy Install Game Shape

The install game should be short, playful, optional, and evidence-producing.

Rounds:

1. Domain cards: "Which worlds have you lived in?" User picks or writes domains.
2. Translation cards: user chooses which analogy makes a concept clearer.
3. Primitive cards: user sorts simple examples into primitives such as data, schema, behavior, flow, interface, constitution, validation.
4. Confidence cards: user marks "I can explain this", "I recognize this", "new to me".
5. Transfer card: user explains one known-domain pattern in another domain.

Outputs:

- profile seed rows,
- domain anchors,
- vocabulary preferences,
- initial concept states,
- no durable canonical promotion.

## Concept Library Seed

Start with a tiny software/systems primitive library:

| Primitive | Plain Role |
| --- | --- |
| `data` | Values or observations that can be stored, moved, checked, or transformed. |
| `schema` | A shape rule for what counts as valid data or artifact structure. |
| `form` | A user-facing structure for entering or shaping data. |
| `api` | A boundary where one system asks another system to do something or return something. |
| `axios` | A concrete JavaScript HTTP client; teach only after API/request/response are clear. |
| `constitution` | A rule artifact that controls acceptable artifact form or behavior. |
| `behavior` | What a system does under conditions. |
| `system` | A set of parts and relations whose behavior is more than one isolated part. |

The library must be extensible at install time and later sessions. If no domain library exists, Guide can still create a one-off bridge receipt without promoting the bridge into a reusable library.
