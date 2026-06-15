# DomainSpec Spec Template Family

The `define`-mode baseline for invoke: a capability-driven feature spec in the **DomainSpec** format. Replaces the former Module Formulae family.

## Files
- `SPEC.md` — the feature spec: What This Module Owns → Module Map → Capabilities → Domain Concepts → **Concept Registry** (typed IDs).
- `operations.md` · `queries.md` · `interfaces.md` · `states.md` · `events.md` · `mappings.md` — the per-aspect docs the spec links to.

## Why this shape
The aspect docs and Concept Registry are the stable interface that downstream DomainSpec capabilities consume (spec→test derivation, doc→metrics derivation, registry sync). Authoring a spec in this format makes those capabilities derivable from one source.

## Vocabulary
Concepts and edges are typed against the canonical DomainSpec definitions in [`arcanum/definitions/DEFINITIONS.md`](../../../../definitions/DEFINITIONS.md) (DS-D1 meta-types, DS-D2 relationships). `TAXONOMY.md` / `RELATIONSHIPS.md` are the prose example layer.
