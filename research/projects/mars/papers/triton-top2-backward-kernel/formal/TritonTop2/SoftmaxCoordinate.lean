import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace TritonTop2

noncomputable def softmaxDen {E : Nat} (z : Fin E -> ℝ) : ℝ :=
  ∑ j : Fin E, Real.exp (z j)

noncomputable def softmaxCoord {E : Nat} (z : Fin E -> ℝ) (i : Fin E) : ℝ :=
  Real.exp (z i) / softmaxDen z

def basis {E : Nat} (k : Fin E) (j : Fin E) : ℝ :=
  if j = k then 1 else 0

def coordLine {E : Nat} (z : Fin E -> ℝ) (k : Fin E) (h : ℝ) : Fin E -> ℝ :=
  fun j => z j + h * basis k j

theorem basis_self {E : Nat} (k : Fin E) :
    basis k k = 1 := by
  simp [basis]

theorem basis_of_ne {E : Nat} {k j : Fin E} (hjk : j ≠ k) :
    basis k j = 0 := by
  simp [basis, hjk]

theorem coordLine_zero {E : Nat} (z : Fin E -> ℝ) (k : Fin E) :
    coordLine z k 0 = z := by
  funext j
  simp [coordLine]

theorem coordLine_self {E : Nat} (z : Fin E -> ℝ) (k : Fin E) (h : ℝ) :
    coordLine z k h k = z k + h := by
  simp [coordLine, basis]

theorem coordLine_of_ne {E : Nat} (z : Fin E -> ℝ) {k j : Fin E} (h : ℝ) (hjk : j ≠ k) :
    coordLine z k h j = z j := by
  simp [coordLine, basis, hjk]

theorem coordLine_hasDerivAt {E : Nat} (z : Fin E -> ℝ) (k j : Fin E) :
    HasDerivAt (fun h : ℝ => coordLine z k h j) (basis k j) 0 := by
  simpa [coordLine] using
    ((hasDerivAt_id (0 : ℝ)).mul_const (basis k j)).const_add (z j)

theorem exp_coordLine_hasDerivAt {E : Nat} (z : Fin E -> ℝ) (k i : Fin E) :
    HasDerivAt
      (fun h : ℝ => Real.exp (coordLine z k h i))
      (Real.exp (z i) * basis k i)
      0 := by
  simpa [coordLine] using (coordLine_hasDerivAt z k i).exp

theorem softmaxDen_coordLine_hasDerivAt {E : Nat} [Nonempty (Fin E)]
    (z : Fin E -> ℝ) (k : Fin E) :
    HasDerivAt
      (fun h : ℝ => softmaxDen (coordLine z k h))
      (Real.exp (z k))
      0 := by
  have hsum :
      HasDerivAt
        (fun h : ℝ => ∑ j : Fin E, Real.exp (coordLine z k h j))
        (∑ j : Fin E, Real.exp (z j) * basis k j)
        0 := by
    exact HasDerivAt.fun_sum fun j _ => exp_coordLine_hasDerivAt z k j
  have hsingle : (∑ j : Fin E, Real.exp (z j) * basis k j) = Real.exp (z k) := by
    rw [Finset.sum_eq_single k]
    · simp [basis]
    · intro j _ hj
      simp [basis, hj]
    · intro hk
      exact False.elim (hk (Finset.mem_univ k))
  simpa [softmaxDen, hsingle] using hsum

theorem softmaxDen_pos {E : Nat} [Nonempty (Fin E)] (z : Fin E -> ℝ) :
    0 < softmaxDen z := by
  unfold softmaxDen
  exact Finset.sum_pos (fun j _ => Real.exp_pos (z j)) Finset.univ_nonempty

theorem softmaxDen_ne_zero {E : Nat} [Nonempty (Fin E)] (z : Fin E -> ℝ) :
    softmaxDen z ≠ 0 := by
  exact ne_of_gt (softmaxDen_pos z)

theorem softmaxCoord_coordLine_hasDerivAt_raw {E : Nat} [Nonempty (Fin E)]
    (z : Fin E -> ℝ) (k i : Fin E) :
    HasDerivAt
      (fun h : ℝ => softmaxCoord (coordLine z k h) i)
      (((Real.exp (z i) * basis k i) * softmaxDen z
        - Real.exp (z i) * Real.exp (z k)) / (softmaxDen z) ^ 2)
      0 := by
  have hden0 : softmaxDen (coordLine z k 0) ≠ 0 := by
    simpa [coordLine_zero] using softmaxDen_ne_zero z
  have hq :=
    (exp_coordLine_hasDerivAt z k i).div
      (softmaxDen_coordLine_hasDerivAt z k)
      hden0
  simpa [softmaxCoord, coordLine_zero] using hq

theorem softmaxCoord_coordLine_hasDerivAt {E : Nat} [Nonempty (Fin E)]
    (z : Fin E -> ℝ) (k i : Fin E) :
    HasDerivAt
      (fun h : ℝ => softmaxCoord (coordLine z k h) i)
      (softmaxCoord z i * (basis k i - softmaxCoord z k))
      0 := by
  refine (softmaxCoord_coordLine_hasDerivAt_raw z k i).congr_deriv ?_
  have hden : softmaxDen z ≠ 0 := softmaxDen_ne_zero z
  unfold softmaxCoord
  field_simp [hden]

theorem softmaxCoord_def {E : Nat} (z : Fin E -> ℝ) (i : Fin E) :
    softmaxCoord z i = Real.exp (z i) / softmaxDen z := by
  rfl

end TritonTop2
