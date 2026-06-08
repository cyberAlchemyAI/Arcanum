---
type: notation-bridge
status: pass
promotion_scope: local-research-only
---

# Notation Bridge

Read this before the glossary or final learning pack. The paper's extraction
uses imperfect glyphs, so this bridge normalizes the important notation into
ASCII-friendly forms.

Shared reusable entries were added to
[../shared-notation-glossary.md](../shared-notation-glossary.md).

## Local Symbols

| Notation | Source meaning | Plain reading | Arcanum-safe analogy | Used in |
| --- | --- | --- | --- | --- |
| `C(A, B)` | Homset of morphisms from `A` to `B` in category `C`. | Morphisms from `A` to `B`. | One-input handoff space. | Category basics. |
| `C(A1 ... An; B)` | Homset of multimorphisms from finite input list to output `B`. | Multi-input arrows to `B`. | Multi-input handoff surface. | Multicategory definition. |
| `f : A -> B` | Morphism from object `A` to object `B`. | `f` goes from `A` to `B`. | Typed route step. | Sections 2-5. |
| `f : A1 ... An -> B` | Multimorphism with arity `n`. | `f` consumes a list and outputs `B`. | Multi-source synthesis step. | Section 4. |
| `b` | Tensor product functor in a monoidal category. | Tensor/combine. | Composition that combines surfaces. | Section 3. |
| `I` | Unit object for a monoidal category. | Monoidal identity object. | Neutral boundary. | Section 3. |
| `alpha`, `rho`, `lambda` | Associator and unitors for biased monoidal categories. | Coherence witnesses. | Receipts proving rearrangements are allowed. | Section 3.1. |
| `b_n` | n-fold tensor product functor. | Variadic tensor. | Variadic composition surface. | Section 3.2. |
| `gamma` | Unbiased coherence isomorphism that removes/rearranges brackets. | Rebracketing witness. | Boundary-normalization receipt. | Section 3.2 and proof. |
| `iota` | Natural isomorphism from identity functor to one-fold tensor. | One-fold tensor coherence. | No-op boundary bridge. | Section 3.2 and proof. |
| `R(A1 ... An)` | Representing object for a list of inputs in a representable multicategory. | Condensed object for the input list. | Canonical receipt object. | Section 4.2. |
| `u_A1...An` | Universal/representation multimorphism from inputs into `R(A1 ... An)`. | Canonical factorization arrow. | Standard packing handoff. | Section 4.2. |
| `V(C)` | Underlying multicategory of unbiased monoidal category `C`. | View `C` as multi-input operations. | Re-encoding layer. | Section 5.2. |
| `MonCat`, `UMonCat`, `Multicat`, `RMulticat` | Categories of monoidal, unbiased monoidal, multicategory, and representable multicategory structures. | Worlds being compared. | Governance zones with structure-preserving maps. | Sections 3-5. |

## Reading Rule

The theorem is not saying "all multi-input systems are tensor systems." It says
that representable multicategories are exactly the multicategories whose
multi-input arrows can be canonically condensed into unary arrows out of tensor-
like representing objects.

