# Writing Sequence Review - Essay Identity And Draft State

- Review target: `DRAFT-SUBSTACK-002.md` and `DRAFT-SUBSTACK-003.md`
- Scope: naming, sequence continuity, artifact lifecycle, and Whisper type model
- Date: 2026-06-23
- Result: pass for writing bridge; flag for lifecycle/type ambiguity

## Findings

### Major: draft numbering is carrying two different meanings

`DRAFT-SUBSTACK-003.md` is currently the first draft of a second essay, but the
filename reads like the third draft of the same Substack artifact family. This
will become more confusing as the series grows, because "draft 03" can mean a
revision count, an essay sequence index, or merely a generated file number.

Decision: treat `DRAFT-SUBSTACK-*` as development provenance only. The stable
public-writing identity should be essay-based:

| Stable Identity | Title | Development Source | Relationship |
| --- | --- | --- | --- |
| `essay-001` | The First Thing a Tool Needs Is a Name | `DRAFT-SUBSTACK-002.md` | series opener |
| `essay-002` | Object, the First Abstraction | `DRAFT-SUBSTACK-003.md` | sequel to `essay-001` |

### Major: the reader-facing bridge should name the prior essay, not the prior draft

The current opening says "Draft 02 ended with a small instruction." That is
accurate inside the development folder, but it leaks the production process into
the public essay. A reader should meet the prior piece as a named essay, not as
a draft artifact.

Recommended public opening direction:

> The First Thing a Tool Needs Is a Name ended with a small instruction: name
> one workflow, give it a purpose, give it a few constraints, and then treat the
> name as an object you can revise.

The rest of the current bridge can stay, because it correctly makes the sequel
snap into place.

### Medium: "Object" is already doing title-level work

`Object, the First Abstraction` is not just a working draft label. It is the
essay's public object. It should be represented as title metadata and sequence
identity before any future publish-prep step. Keeping it only inside a draft file
name or composition plan weakens downstream review, promotion, and linking.

### Medium: Whisper lacks a series relation type

The current Whisper contract has `draft_artifact` and `learning_residue`, but it
does not yet model a series node, predecessor relation, or bridge contract. This
matters here because the second essay does not merely follow the first by date;
it consumes the first essay's closing instruction as its opening premise.

Recommended relation:

```yaml
series_relation:
  series_id: language-as-toolmaking
  essay_id: essay-002
  sequence_index: 2
  previous_essay_id: essay-001
  relation_type: sequel
  bridge_contract: consumes_previous_closing_prompt
```

### Minor: the current draft bridge is conceptually strong

The transition from name to object works. The strongest sentence-level mechanism
is the handle-to-shape movement. The issue is not that the prose needs a new
argument; the issue is that the artifact lifecycle should support what the prose
is already doing.

## Recommendation

Promote `DRAFT-SUBSTACK-002.md` to the canonical identity `essay-001` for this
series, with title `The First Thing a Tool Needs Is a Name`. Treat
`DRAFT-SUBSTACK-003.md` as the first draft of `essay-002`, with title `Object,
the First Abstraction`.

Do not rename or move the existing development draft files yet. First add a
Whisper lifecycle/type layer that separates:

- essay identity from draft revision;
- public title from file provenance;
- sequence relation from filesystem ordering;
- publish status from validation status.

## Proposed Edit To Essay 02 Opening

Replace the first sentence:

```text
Draft 02 ended with a small instruction: name one workflow, give it a purpose,
give it a few constraints, and then treat the name as an object you can revise.
```

With:

```text
The First Thing a Tool Needs Is a Name ended with a small instruction: name one
workflow, give it a purpose, give it a few constraints, and then treat the name
as an object you can revise.
```

Keep the next sentence. It is doing the right work:

```text
That last phrase is doing more work than it first appears to do.
```

## Review Verdict

The writing bridge passes. The lifecycle model flags.

Next owner: `invoke` for a lifecycle/type management packet, then `spellcraft`
for Whisper lifecycle acceptance.
