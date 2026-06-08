---
profile: autobayes-research
name: Closure Gates
description: Objective gates for AutoBayes research closure.
type: gate-list
status: active
last_updated: 2026-06-06
---

# Closure Gates

## Gate 1 - Source Visibility

Every claim must name its source kind:

- `AutoBayes paper`
- `related paper`
- `derived reading`
- `Arcanum analogy`
- `candidate bridge`
- `open question`

Fail condition:

> A statement sounds like the paper's claim but has no source marker.

## Gate 2 - Layer Separation

Any discussion of model, inversion, loss, parameters, or optimization must say which layer it belongs to.

Fail condition:

> Optimization semantics are used to explain model syntax, or model syntax is treated as enough to define optimization.

## Gate 3 - Arcanum Translation Safety

An Arcanum reading must preserve the source term first.

Fail condition:

> A source term is replaced by sigil/spell/dispatch language before its paper meaning is recorded.

## Gate 4 - Related-Paper Closure

Related papers must be classified as prerequisite, contrast, background, or optional.

Fail condition:

> All citations are treated as equally necessary.

## Gate 5 - Glossary Promotion Guard

Local research glossary entries do not become canonical Arcanum definitions.

Fail condition:

> A glossary item is promoted to Inventory, Ontology, registry, sigil, spell, or runtime contract without owner review.

## Gate 6 - Distill Usefulness

A distill closes only if it gives the operator a reusable mental model.

Fail condition:

> The distill is a generic summary that does not improve Arcanum-shaped understanding.

## Gate 7 - Full-Mode Permission

Subagent fanout requires explicit operator approval before execution.

Fail condition:

> The strategy recommends subagents and then silently runs delegated research.

