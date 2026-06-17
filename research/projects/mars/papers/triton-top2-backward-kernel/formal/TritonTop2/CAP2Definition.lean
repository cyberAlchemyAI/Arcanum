import TritonTop2.SoftmaxCoordinate
import TritonTop2.FixedLoadCAP2

open scoped BigOperators

namespace TritonTop2

noncomputable def cap2Sigmoid (x : ℝ) : ℝ :=
  (1 + Real.exp (-x))⁻¹

noncomputable def cap2Capacity (E : Nat) : ℝ :=
  (2.1 : ℝ) / E

noncomputable def cap2Overload {E : Nat}
    (load : Fin E -> ℝ) (j : Fin E) (tauCap : ℝ) : ℝ :=
  cap2Sigmoid ((load j - cap2Capacity E) / tauCap)

noncomputable def cap2AdjustedLogit {E : Nat}
    (z load : Fin E -> ℝ) (j : Fin E) (tauCap mu : ℝ) : ℝ :=
  z j - mu * cap2Overload load j tauCap

noncomputable def cap2PairwiseSoftRank {E : Nat}
    (u : Fin E -> ℝ) (j : Fin E) (tauRank : ℝ) : ℝ :=
  ∑ k : Fin E, if k = j then 0 else cap2Sigmoid ((u j - u k) / tauRank)

noncomputable def cap2Membership {E : Nat}
    (softRank : Fin E -> ℝ) (j : Fin E) (tauGate : ℝ) : ℝ :=
  cap2Sigmoid ((softRank j - ((E : ℝ) - 2 - 0.5)) / tauGate)

noncomputable def cap2Gated {E : Nat}
    (z load : Fin E -> ℝ) (j : Fin E)
    (tauCap tauRank tauGate mu : ℝ) : ℝ :=
  let u : Fin E -> ℝ := fun q => cap2AdjustedLogit z load q tauCap mu
  let softRank : Fin E -> ℝ := fun q => cap2PairwiseSoftRank u q tauRank
  cap2Membership softRank j tauGate * softmaxCoord u j

noncomputable def cap2WeightDen {E : Nat}
    (z load : Fin E -> ℝ) (epsilon tauCap tauRank tauGate mu : ℝ) : ℝ :=
  epsilon + ∑ j : Fin E, cap2Gated z load j tauCap tauRank tauGate mu

noncomputable def cap2Weight {E : Nat}
    (z load : Fin E -> ℝ) (j : Fin E)
    (epsilon tauCap tauRank tauGate mu : ℝ) : ℝ :=
  cap2Gated z load j tauCap tauRank tauGate mu /
    cap2WeightDen z load epsilon tauCap tauRank tauGate mu

theorem cap2AdjustedLogit_fixed_load_data {E : Nat}
    (z load : Fin E -> ℝ) (j : Fin E) (tauCap mu : ℝ) :
    cap2AdjustedLogit z load j tauCap mu =
      z j - mu * cap2Overload load j tauCap := by
  rfl

theorem cap2Weight_uses_fixed_load_argument {E : Nat}
    (z load : Fin E -> ℝ) (j : Fin E)
    (epsilon tauCap tauRank tauGate mu : ℝ) :
    cap2Weight z load j epsilon tauCap tauRank tauGate mu =
      cap2Gated z load j tauCap tauRank tauGate mu /
        cap2WeightDen z load epsilon tauCap tauRank tauGate mu := by
  rfl

theorem cap2Definition_load_boundary :
    fixedLoadCAP2Boundary.load = .fixedDataAssumption := by
  exact fixedLoad_is_fixed_data

theorem cap2Definition_not_triton_proof :
    fixedLoadCAP2Boundary.tritonMemory = .nonTheorem := by
  exact triton_memory_status_is_not_proved_in_lean

end TritonTop2
