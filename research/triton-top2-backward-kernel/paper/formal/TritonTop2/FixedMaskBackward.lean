import TritonTop2.RealBackwardIdentities

open scoped BigOperators

namespace TritonTop2

noncomputable def fixedMaskDZ {T E : Nat}
    (mask upstream : RealMatrix T E) : RealMatrix T E :=
  fun t e => mask t e * upstream t e

noncomputable def fixedMaskDW {T E D : Nat}
    (mask upstream : RealMatrix T E) (X : RealMatrix T D) : RealMatrix E D :=
  dWReal (fixedMaskDZ mask upstream) X

noncomputable def fixedMaskDXRouter {T E D : Nat}
    (mask upstream : RealMatrix T E) (W : RealMatrix E D) : RealMatrix T D :=
  dXRouterReal (fixedMaskDZ mask upstream) W

theorem fixedMaskDW_adjoint {T E D : Nat}
    (mask upstream : RealMatrix T E) (X : RealMatrix T D) (W : RealMatrix E D) :
    (∑ t : Fin T, ∑ e : Fin E,
        fixedMaskDZ mask upstream t e * logitsReal X W t e) =
      (∑ e : Fin E, ∑ d : Fin D,
        fixedMaskDW mask upstream X e d * W e d) := by
  simpa [fixedMaskDW] using
    (dWReal_adjoint (fixedMaskDZ mask upstream) X W)

theorem fixedMaskDXRouter_adjoint {T E D : Nat}
    (mask upstream : RealMatrix T E) (X : RealMatrix T D) (W : RealMatrix E D) :
    (∑ t : Fin T, ∑ e : Fin E,
        fixedMaskDZ mask upstream t e * logitsReal X W t e) =
      (∑ t : Fin T, ∑ d : Fin D,
        fixedMaskDXRouter mask upstream W t d * X t d) := by
  simpa [fixedMaskDXRouter] using
    (dXRouterReal_adjoint (fixedMaskDZ mask upstream) X W)

theorem fixedMask_is_data_not_selection_gradient {T E : Nat}
    (mask upstream : RealMatrix T E) :
    fixedMaskDZ mask upstream = fun t e => mask t e * upstream t e := by
  rfl

end TritonTop2
