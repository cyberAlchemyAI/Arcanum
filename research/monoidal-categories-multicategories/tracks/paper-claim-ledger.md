---
type: source-claim-ledger
status: pass
promotion_scope: local-research-only
---

# Paper Claim Ledger

| ID | Claim | Source kind | Evidence | Local reading | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | Monoidal categories are categories with tensor product encoded as a bifunctor. | primary-source | Abstract; Section 3.1. | Tensor structure is extra structure plus coherence. | accepted |
| C2 | Multicategories generalize categories by allowing finite lists of domains. | primary-source | Abstract; Section 4.1. | Multi-input operations become first-class. | accepted |
| C3 | Hermida showed `MonCat` is equivalent to representable multicategories. | primary-source citing related-source | Introduction; Section 5.1. | The target is representable multicategories, not all multicategories. | accepted |
| C4 | Leinster reformulated the result but did not publish proof details. | primary-source citing related-source | Abstract; Introduction. | The paper's contribution is reconstruction of that proof route. | accepted |
| C5 | Unbiased monoidal categories are central because they expose n-fold tensor products. | primary-source | Section 3.2. | Variadic tensor structure makes the multicategory construction direct. | accepted |
| C6 | A representable multicategory has representing objects and universal factorization multimorphisms. | primary-source | Definition 4.2.1; Proposition 4.2.6; Corollary 4.2.7. | Canonical packing plus uniqueness is the bridge condition. | accepted |
| C7 | The proof constructs `V : UMonCat -> Multicat`, restricts to `RMulticat`, and proves full, faithful, essentially surjective. | primary-source | Section 5.2. | Equivalence proof is a structure-preserving translation route. | accepted-standard |
| C8 | `MonCat ~= UMonCat` plus `UMonCat ~= RMulticat` yields `MonCat ~= RMulticat`. | primary-source | Theorem 3.2.9; final proof. | The theorem uses a chain of equivalences. | accepted |
| C9 | The theorem does not imply `MonCat ~= Multicat`. | primary-source | Remark 5.1.2. | Multicategories are more general; representability is the boundary. | accepted |

## Open Claim Residue

| ID | Question | Blocking artifact | Next route |
| --- | --- | --- | --- |
| R1 | How does the reconstructed proof compare line-by-line with Hermida and Leinster originals? | External source expansion. | Future deep run. |
| R2 | Can the proof spine be formalized in Lean or another proof assistant? | Formalization design. | Future proof tower. |

