---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: architecture-bundle
---

# Architecture Bundle: {Module Name}

Translate an approved DomainSpec `SPEC.md` into structural and process design views. This is the design-stage companion to the DomainSpec template family.

## Design Intent
Summarize architecture goals and constraints in two to three sentences.

## Inputs
- [SPEC.md](SPEC.md) — capabilities + Concept Registry (typed against DS-D1)
- aspect docs: [operations.md](operations.md), [queries.md](queries.md), [interfaces.md](interfaces.md), [states.md](states.md), [events.md](events.md), [mappings.md](mappings.md)
- canonical vocabulary: `arcanum/definitions/DEFINITIONS.md` (DS-D1 meta-types, DS-D2 edges)

## Required View Set

### 1. Context View
```mermaid
graph TD
    Actor --> Module[{Module}]
    Module --> External[External Dependency]
```

### 2. Capability View
One node per SPEC capability; edges are DS-D2 relationship verbs between the Concept Registry entries they touch.

### 3. Concept/Type View
The Concept Registry as a typed graph: nodes carry their DS-D1 meta-type; edges carry DS-D2 verbs and must satisfy the DS-D8 edge signature.

### 4. Operation/Flow View
For each Operation (from `operations.md`): inputs → rules → calculations → state transition → postconditions → events. Maps the write-side flow.

### 5. State View
The State Machine(s) from `states.md`: states + transition table; one transition row = one behavioral obligation downstream (test-derivation / obs-derivation).

### 6. Dependency/Interface View
Interfaces (`interfaces.md`) and mappings (`mappings.md`): exposure boundaries, contracts, and cross-shape transformations.

## Design Rules
- Every view references Concept Registry IDs; do not introduce concepts absent from `SPEC.md`.
- Forbidden edges are those whose endpoint meta-types violate the DS-D8 signature — flag, do not draw.
- Keep the aspect-doc contract (M2-CONTRACT) stable; design adds views, it does not redefine the spec interface.

## Output
A six-view design that downstream `plan` (execution-pack) and the M2 derivation capabilities can consume without reopening discovery.
