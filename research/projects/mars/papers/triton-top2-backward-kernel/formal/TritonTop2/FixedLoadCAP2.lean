import TritonTop2.FormalBoundary

namespace TritonTop2

structure CAP2Boundary where
  load : BoundaryStatus
  routerAlgebra : BoundaryStatus
  tritonMemory : BoundaryStatus
  fp16Numerics : BoundaryStatus
  deriving Repr

def fixedLoadCAP2Boundary : CAP2Boundary :=
  { load := .fixedDataAssumption
    routerAlgebra := .provedInsideModel
    tritonMemory := .nonTheorem
    fp16Numerics := .deferred }

theorem fixedLoad_is_fixed_data :
    fixedLoadCAP2Boundary.load = .fixedDataAssumption := by
  rfl

theorem cap2_router_algebra_is_inside_model :
    fixedLoadCAP2Boundary.routerAlgebra = .provedInsideModel := by
  rfl

theorem triton_memory_status_is_not_proved_in_lean :
    fixedLoadCAP2Boundary.tritonMemory = .nonTheorem := by
  rfl

theorem fp16_numerics_are_deferred :
    fixedLoadCAP2Boundary.fp16Numerics = .deferred := by
  rfl

end TritonTop2
