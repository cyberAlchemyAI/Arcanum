namespace TritonTop2

inductive BoundaryStatus where
  | provedInsideModel
  | fixedDataAssumption
  | deferred
  | nonTheorem
  deriving DecidableEq, Repr

def hardTop2SelectionStatus : BoundaryStatus := .nonTheorem

def smoothRelaxationStatus : BoundaryStatus := .provedInsideModel

theorem hardTop2Selection_is_not_a_formal_claim :
    hardTop2SelectionStatus = .nonTheorem := by
  rfl

theorem smoothRelaxation_boundary_is_inside_model :
    smoothRelaxationStatus = .provedInsideModel := by
  rfl

end TritonTop2
