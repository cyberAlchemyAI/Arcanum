# Stage 06: Invoke Redefine / Design

Status: `pass`

## Revised Capability Stack

```text
User
  owns learning/profile/glossary ledger

Translate
  owns vocabulary, analogy, and domain bridge transformations

Guide
  owns guided route orchestration and may dispatch Translate, research, x-ray, inventory, or subagents
```

## Translate Schema Candidates

| Row / Artifact | Purpose |
| --- | --- |
| `translation_request` | Captures source domain, target domain, target concept/artifact, and user context handles. |
| `term_map` | Maps source vocabulary to target vocabulary. |
| `bridge_map` | Maps analogy/metaphor components and names where the bridge breaks. |
| `primitive_alignment` | Links concrete terms to primitives like schema, system, behavior, interface, validation, constitution. |
| `translation_receipt` | Records strategy, output, limits, user reaction, and ledger-update proposal. |

## Guide Dispatch Shape

`/guide this architecture` should be able to create a route like:

```text
frame request
  -> inspect architecture artifact
  -> dispatch research/subagents if missing context exists
  -> x-ray structure
  -> call Translate for the user's vocabulary/domain frame
  -> assemble guided walkthrough
  -> ask active evidence question
  -> emit guide receipt and user-ledger update proposal
```

## Design Rule

Guide should call Translate, not contain Translate.

Translate should be reusable by:

- Guide,
- CyberAlchemy install game,
- glossary creation,
- documentation explanation,
- architecture reviews,
- cross-domain teaching artifacts.
