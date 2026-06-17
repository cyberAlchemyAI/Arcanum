import TritonTop2.CAP2Definition

namespace TritonTop2

theorem cap2AdjustedLogit_coordLine_self {E : Nat}
    (z load : Fin E -> ℝ) (k : Fin E) (h tauCap mu : ℝ) :
  cap2AdjustedLogit (coordLine z k h) load k tauCap mu =
      cap2AdjustedLogit z load k tauCap mu + h := by
  simp [cap2AdjustedLogit, coordLine, basis, sub_eq_add_neg, add_assoc, add_comm]

theorem cap2AdjustedLogit_coordLine_of_ne {E : Nat}
    (z load : Fin E -> ℝ) {k j : Fin E} (h tauCap mu : ℝ) (hjk : j ≠ k) :
    cap2AdjustedLogit (coordLine z k h) load j tauCap mu =
      cap2AdjustedLogit z load j tauCap mu := by
  simp [cap2AdjustedLogit, coordLine, basis, hjk]

theorem cap2FixedLoad_no_dynamic_load_claim :
    fixedLoadCAP2Boundary.load = .fixedDataAssumption := by
  exact fixedLoad_is_fixed_data

end TritonTop2
