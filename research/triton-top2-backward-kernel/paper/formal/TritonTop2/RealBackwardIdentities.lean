import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset

open scoped BigOperators

set_option linter.unusedSimpArgs false

namespace TritonTop2

abbrev RealMatrix (m n : Nat) := Fin m -> Fin n -> ℝ

noncomputable def logitsReal {T E D : Nat}
    (X : RealMatrix T D) (W : RealMatrix E D) : RealMatrix T E :=
  fun t e => ∑ d : Fin D, X t d * W e d

noncomputable def dWReal {T E D : Nat}
    (dZ : RealMatrix T E) (X : RealMatrix T D) : RealMatrix E D :=
  fun e d => ∑ t : Fin T, dZ t e * X t d

noncomputable def dXRouterReal {T E D : Nat}
    (dZ : RealMatrix T E) (W : RealMatrix E D) : RealMatrix T D :=
  fun t d => ∑ e : Fin E, dZ t e * W e d

theorem dWReal_adjoint {T E D : Nat}
    (dZ : RealMatrix T E) (X : RealMatrix T D) (W : RealMatrix E D) :
    (∑ t : Fin T, ∑ e : Fin E, dZ t e * logitsReal X W t e) =
      (∑ e : Fin E, ∑ d : Fin D, dWReal dZ X e d * W e d) := by
  calc
    (∑ t : Fin T, ∑ e : Fin E, dZ t e * logitsReal X W t e)
        = ∑ t : Fin T, ∑ e : Fin E, ∑ d : Fin D, dZ t e * X t d * W e d := by
          simp [logitsReal, Finset.mul_sum, mul_assoc]
    _ = ∑ e : Fin E, ∑ t : Fin T, ∑ d : Fin D, dZ t e * X t d * W e d := by
          rw [Finset.sum_comm]
    _ = ∑ e : Fin E, ∑ d : Fin D, ∑ t : Fin T, dZ t e * X t d * W e d := by
          apply Finset.sum_congr rfl
          intro e _
          rw [Finset.sum_comm]
    _ = ∑ e : Fin E, ∑ d : Fin D, dWReal dZ X e d * W e d := by
          simp [dWReal, Finset.mul_sum, mul_assoc, mul_left_comm, mul_comm]

theorem dXRouterReal_adjoint {T E D : Nat}
    (dZ : RealMatrix T E) (X : RealMatrix T D) (W : RealMatrix E D) :
    (∑ t : Fin T, ∑ e : Fin E, dZ t e * logitsReal X W t e) =
      (∑ t : Fin T, ∑ d : Fin D, dXRouterReal dZ W t d * X t d) := by
  calc
    (∑ t : Fin T, ∑ e : Fin E, dZ t e * logitsReal X W t e)
        = ∑ t : Fin T, ∑ e : Fin E, ∑ d : Fin D, dZ t e * X t d * W e d := by
          simp [logitsReal, Finset.mul_sum, mul_assoc]
    _ = ∑ t : Fin T, ∑ d : Fin D, ∑ e : Fin E, dZ t e * X t d * W e d := by
          apply Finset.sum_congr rfl
          intro t _
          rw [Finset.sum_comm]
    _ = ∑ t : Fin T, ∑ d : Fin D, dXRouterReal dZ W t d * X t d := by
          simp [dXRouterReal, Finset.mul_sum, mul_assoc, mul_left_comm, mul_comm]

end TritonTop2
