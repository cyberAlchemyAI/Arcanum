---
type: governed-local-definitions
status: pass
promotion_scope: local-research-only
---

# Definitions

These definitions are local to this research tower. They explain source
meaning and operator intuition; they are not canonical Arcanum definitions.

## D-MCM-001 Monoidal Category

Formal shape:

```text
(C, b, I, alpha, rho, lambda)
```

Source meaning: a category `C`, tensor product functor `b : C x C -> C`,
unit object `I`, associator `alpha`, right unitor `rho`, left unitor `lambda`,
subject to triangle and pentagon coherence diagrams.

Plain intuition: a monoidal category is a context where objects and morphisms
can be combined like a monoid operation, but equality is replaced by coherent
isomorphism.

Misuse warning: do not use "monoidal" for any system with a merge operation.
The merge must be functorial and coherently compatible with units and
associativity.

## D-MCM-002 Unbiased Monoidal Category

Formal shape:

```text
(C, b_n, gamma, iota)
```

Source meaning: a category with n-fold tensor product functors for all arities,
plus coherence isomorphisms `gamma` and `iota`.

Plain intuition: the biased version says "combine two at a time"; the unbiased
version gives the whole arity spectrum directly and uses coherence to move
between groupings.

Misuse warning: the arity-general view is not just syntactic sugar in the proof;
it is what makes the underlying multicategory construction clean.

## D-MCM-003 Multicategory

Formal shape:

```text
objects ob(C)
homsets C(A1 ... An; B)
composition f o (f1 ... fn)
identities 1_A
```

Source meaning: a category-like structure with multimorphisms from finite lists
of inputs to one output, with composition and identities.

Plain intuition: a multicategory makes many-input operations first-class.

Misuse warning: unary-only multicategories collapse back toward ordinary
categories; the theorem depends on the extra arity structure.

## D-MCM-004 Representable Multicategory

Formal shape:

```text
for every A1 ... An:
  R(A1 ... An)
  u_A1...An : A1 ... An -> R(A1 ... An)
```

Source meaning: every multimorphism can be uniquely factored through
representing objects for grouped input lists.

Plain intuition: the input list has a canonical packed object, and every use of
the separate inputs can be replayed as a unique unary use of the packed object.

Misuse warning: canonical factorization and uniqueness are required; a mere
adapter or bundle is not enough.

## D-MCM-005 Underlying Multicategory Functor

Formal shape:

```text
V : UMonCat -> Multicat
V(C)(A1 ... An; B) = C((A1 b ... b An), B)
```

Source meaning: an unbiased monoidal category can be viewed as a multicategory
whose multimorphisms are morphisms out of n-fold tensor products.

Plain intuition: tensor products supply the packed input object; morphisms out
of that object become multi-input arrows.

Misuse warning: `V` is a paper-specific construction; do not treat it as a
general Arcanum runtime adapter.

