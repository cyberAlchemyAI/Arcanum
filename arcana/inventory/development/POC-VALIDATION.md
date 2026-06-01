# POC Validation: Inventory Evidence-Card

## Invoke Result

- Mode: refresh
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Source evidence: `presentation.html` distilled decision slide and current discussion
- Target artifacts: `IMPLEMENTATION-PLAN.md`, `WORK-PACK.md`, `REFRESH-REPORT.md`, `refresh-report.json`
- Mutation mode: apply-approved

## Purpose

Define the data-backed gates for deciding whether the evidence-card POC should continue, refine, or stop.

The POC can start directly. The open questions are not blocker decisions; they are measurable validation gates.

## Distilled Decision Gates

| Gate | Smallest Decision Unit | Data To Gather | Continue If | Refine If |
| --- | --- | --- | --- | --- |
| Source slice | 3-5 bounded source sections | Count useful cards produced from the slice | The slice yields at least 10 distinct cards without needing whole-repo context. | Useful evidence requires broad repo rereading. |
| Card size | One reusable evidence object | Median card word count and claim count per card | Median card stays under 120 words and usually carries one main claim/concept/question/method. | Cards become mini-documents or pointer-only stubs. |
| Selector quality | One reviewable source pointer per material claim | Reviewer inspection time for card claims | A reviewer can inspect each material claim in under 30 seconds. | Selectors are vague, unstable, or require search. |
| Validation strictness | Required failure set | Invalid examples and real-card lint findings | Missing selectors, unknown enums, bad owner/status pairs, and unsafe relation candidates fail for named reasons. | Real useful cards fail for harmless reasons. |
| Retrieval value | One concrete task query | Selected cards, excluded matches, and raw-source comparison | Retrieval returns fewer, better cards than raw source rereading and explains exclusions. | Retrieval is noisy or indistinguishable from broad search. |
| Handoff safety | One candidate packet | Reader review of packet authority language | Reader can tell the packet is candidate-only and not promoted. | Authority fields confuse ownership or imply downstream governance. |

## Candidate Intermediate Artifact: EvidenceSet

The current refinement candidate is an intermediate composed artifact provisionally named `EvidenceSet`.

`EvidenceSet` is not a replacement for `EvidenceCard`. It is a task- or topic-scoped composition of multiple cards with its own index, selection rationale, exclusions, residue, and handoff intent.

### Distilled Shape

| Part | Purpose |
| --- | --- |
| `set_id` | Stable ID for the composition. |
| `purpose` | The task, topic, question, or downstream handoff this set supports. |
| `card_refs` | Ordered evidence-card IDs with inclusion reasons. |
| `excluded_card_refs` | Near matches rejected with reasons. |
| `index_terms` | Tags, source paths, card types, authority levels, and handoff targets used for lookup. |
| `synthesis_note` | Short note explaining what the group proves, suggests, or leaves unresolved. |
| `residue` | Remaining ambiguity across the set. |
| `handoff_target` | Optional downstream consumer when the set is meant as a packet seed. |

### Why It Might Be Needed

| Tension | Evidence To Gather |
| --- | --- |
| Retrieval needs a reusable grouped result, not just independent cards. | The same card group is useful for more than one task or follow-up. |
| Handoff packets need a stable pre-packet structure. | Ontology/Definitions packet assembly repeats the same grouping logic. |
| Indexing individual cards is not enough for task context. | Users need the relationship among cards, not only the cards themselves. |

### Keep It Out If

- one retrieval output is enough and does not need reuse;
- card groups are always one-off;
- the set starts becoming a synthesis document with hidden claims;
- it duplicates Context Builder packs or downstream handoff packets.

### POC Test

Create one `EvidenceSet` from the pilot cards only if the first retrieval query naturally produces a reusable group. Continue with `EvidenceSet` if it improves retrieval explanation or handoff assembly. Refine or drop it if it adds ceremony without reducing confusion.

## Minimal POC Dataset

| Item | Target |
| --- | --- |
| Source sections | 3-5 bounded sections selected from `POC-CANDIDATES.md` |
| Cards | about 10 |
| Required card mix | source-summary, concept, method, claim, question |
| Invalid examples | selector, enum, owner/status, relation notice, minimal-profile misuse |
| Retrieval query | one real task-shaped query |
| Handoff packets | one Ontology Vault packet and one Definitions Governance packet |

## Decision Rule

- Continue if at least five of six gates pass and the failing gate has a narrow repair.
- Refine if two or more gates fail, or if any failure indicates the canonical card unit is the wrong abstraction.
- Stop or redesign if authority boundaries cannot be made obvious to a reader.

## Next Route

Start implementation with the POC validation gates visible in `WORK-PACK.md` and the source slice selected in `POC-CANDIDATES.md`.
