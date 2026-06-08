---
type: distilled-knowledge
status: pass
promotion_scope: local-research-only
---

# Distilled Knowledge

## One Sentence

The paper shows that monoidal categories and representable multicategories are
two encodings of the same compositional structure: one starts from tensor
products, the other starts from multi-input arrows with canonical
factorization.

## Concept Spine

```text
category
  -> monoidal category
  -> unbiased monoidal category
  -> underlying multicategory V(C)
  -> representable multicategory
  -> MonCat ~= UMonCat ~= RMulticat
```

## Operator Model

For Arcanum thinking, read the theorem like this:

```text
If every multi-input operation has a canonical way to pack its inputs,
then the multi-input world can be read as a tensor/composition world.
If the tensor world gives coherent n-fold packing,
then its operations can be read as multi-input arrows.
The equivalence lives in the receipts that prove these translations preserve
structure, not in a slogan that "multi-input equals tensor."
```

## Why Representability Matters

Multicategories are broader than monoidal categories. Representability is the
condition that trims multicategories down to the exact part that can be
recovered from monoidal tensor structure.

## What This Teaches Research Tower

This paper stresses the sigil in three useful ways:

- notation is a prerequisite, not a side artifact;
- proof-spine artifacts need to preserve construction direction;
- final packs must block over-strong analogies.

