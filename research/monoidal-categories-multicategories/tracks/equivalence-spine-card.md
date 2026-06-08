---
type: theorem-spine-card
status: pass
promotion_scope: local-research-only
---

# Equivalence Spine Card

## Theorem

`MonCat ~= RMulticat`.

Source: Theorem 5.1.1.

## Route

1. Establish ordinary category theory basics: categories, functors, natural
   transformations, equivalence of categories.
2. Define monoidal categories and monoidal functors.
3. Move to unbiased monoidal categories, where n-fold tensor products are
   explicit.
4. Define multicategories and multifunctors.
5. Define representable multicategories through representing objects and
   universal factorization.
6. Construct the underlying multicategory functor:

```text
V : UMonCat -> Multicat
V(C)(A1 ... An; B) = C((A1 b ... b An), B)
```

7. Show `V(C)` is a well-defined multicategory and `V(F, pi)` is a well-defined
   multifunctor.
8. Show representability corresponds to being isomorphic to some `V(D)`.
9. Restrict `V` to:

```text
V1 : UMonCat -> RMulticat
```

10. Show `V1` is full, faithful, and essentially surjective.
11. Combine with `MonCat ~= UMonCat` to obtain `MonCat ~= RMulticat`.

## Operator Interpretation

The proof is a two-direction receipt:

- from tensor/coherence data to multi-input arrows;
- from representable multi-input arrows back to tensor/coherence data.

The hard work is proving the receipts preserve composition, identities,
universals, and morphism structure.

## Cutoff

This card preserves the proof route. It does not certify every diagram chase or
omitted notationally-heavy step.

