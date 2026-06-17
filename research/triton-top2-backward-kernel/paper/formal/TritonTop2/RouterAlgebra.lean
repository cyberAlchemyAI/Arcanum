import Std

namespace TritonTop2

abbrev Matrix (α : Type u) (m n : Nat) := Fin m -> Fin n -> α

def logits {α : Type u}
    {T E D : Nat} (mul : α -> α -> α) (reduceD : (Fin D -> α) -> α)
    (X : Matrix α T D) (W : Matrix α E D) : Matrix α T E :=
  fun t e => reduceD (fun d : Fin D => mul (X t d) (W e d))

def dWFromDZ {α : Type u}
    {T E D : Nat} (mul : α -> α -> α) (reduceT : (Fin T -> α) -> α)
    (dZ : Matrix α T E) (X : Matrix α T D) : Matrix α E D :=
  fun e d => reduceT (fun t : Fin T => mul (dZ t e) (X t d))

def dXRouterFromDZ {α : Type u}
    {T E D : Nat} (mul : α -> α -> α) (reduceE : (Fin E -> α) -> α)
    (dZ : Matrix α T E) (W : Matrix α E D) : Matrix α T D :=
  fun t d => reduceE (fun e : Fin E => mul (dZ t e) (W e d))

theorem logits_apply {α : Type u}
    {T E D : Nat} (mul : α -> α -> α) (reduceD : (Fin D -> α) -> α)
    (X : Matrix α T D) (W : Matrix α E D) (t : Fin T) (e : Fin E) :
    logits mul reduceD X W t e = reduceD (fun d : Fin D => mul (X t d) (W e d)) := by
  rfl

theorem dWFromDZ_apply {α : Type u}
    {T E D : Nat} (mul : α -> α -> α) (reduceT : (Fin T -> α) -> α)
    (dZ : Matrix α T E) (X : Matrix α T D) (e : Fin E) (d : Fin D) :
    dWFromDZ mul reduceT dZ X e d = reduceT (fun t : Fin T => mul (dZ t e) (X t d)) := by
  rfl

theorem dXRouterFromDZ_apply {α : Type u}
    {T E D : Nat} (mul : α -> α -> α) (reduceE : (Fin E -> α) -> α)
    (dZ : Matrix α T E) (W : Matrix α E D) (t : Fin T) (d : Fin D) :
    dXRouterFromDZ mul reduceE dZ W t d = reduceE (fun e : Fin E => mul (dZ t e) (W e d)) := by
  rfl

end TritonTop2
