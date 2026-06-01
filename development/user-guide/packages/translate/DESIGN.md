# Translate Design

## Invoke Result

- Mode: full authoring package, design slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/translate/`
- Phase status: `pass`
- Mode contract: `spells/invoke/design.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Next route: `sigil-development`

## View 1: Context

Translate sits between User and Guide.

```text
User handles -> Translate -> Guide explanation
```

Translate is reusable by Guide, install games, glossary workflows, docs, and architecture explanations.

## View 2: High-Level Structure

| Component | Responsibility |
| --- | --- |
| Translation request | Defines source domain, target domain, concept/artifact, and style. |
| Term map | Maps source vocabulary to target vocabulary. |
| Bridge map | Maps analogy components and limits. |
| Primitive alignment | Relates concrete language to abstractions. |
| Translation receipt | Records strategy, result, limits, and update proposal. |

## View 3: Low-Level Components

Required receipt fields:

- `translation_id`
- `target_concept`
- `source_domain`
- `target_domain`
- `user_preference_handles`
- `term_map`
- `bridge_map`
- `maps_well`
- `breaks_here`
- `target_domain_definition`
- `translated_explanation`
- `ledger_update_proposal`

## View 4: Workflow Process

```text
request translation
  -> read optional User handles
  -> map terms and primitives
  -> write target-domain definition
  -> produce bridge explanation
  -> name mapping limits
  -> emit receipt
```

## View 5: Decision Flow

| Condition | Decision |
| --- | --- |
| Analogy hides target truth. | Block or rewrite with explicit target definition. |
| No user domain anchor exists. | Use generic plain-language bridge and record residue. |
| User dislikes metaphor family. | Avoid it and propose vocabulary preference update. |
| Translation requires external facts. | Return research-needed flag to Guide; Translate does not research. |

## View 6: Dependency Interface

| Dependency | Direction | Contract |
| --- | --- | --- |
| User ledger | read handles, return receipt | User owns durable memory updates. |
| Guide | caller | Guide frames the route and receives translated explanation. |
| Inventory/Ontology | optional read | Canonical definitions can be referenced but not mutated. |

## Design Decision

Translate is a sigil candidate, not a spell. It should be a callable primitive that other spells compose.
