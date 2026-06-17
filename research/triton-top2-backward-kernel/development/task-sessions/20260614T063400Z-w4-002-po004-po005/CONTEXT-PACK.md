# Context Pack - TASK-W4-002

Task: `TASK-W4-002`

Objective: prove or manually validate `PO-004` and `PO-005`.

## Controlling Sources

- `WORK-PACK.md`: task row, dependencies, validation surface.
- `FORMAL-MATH-SPEC.md`: fixed-mask V0 assumptions and proof obligations.
- `FORMAL-MATH-STUBS.md`: theorem targets and non-theorems.
- `W4-PROOF-NOTES.md`: Lean-shaped stubs and proof order.
- `RIGOR-VALIDATION-MAP.md`: separation of formal math, numerical parity, and
  systems claims.
- `tests/test_router_reference.py`: executable standard-library evidence.
- `reference/router_reference.py`: V0 reference implementation and manual
  backward formulas.

## Hard Constraints

- Do not claim gradient through hard `Top2` selection.
- Do not claim Triton, FP16, zero-allocation, or full FFN backward correctness.
- Keep validation limited to the idealized fixed-mask V0 graph.
- Completion requires a proof note or blocked note for `PO-004`/`PO-005`.

## Execution Choice

Use manual finite-sum proof notes plus narrow finite-difference tests rather than
creating a full Lean project. This matches the task acceptance wording and keeps
formalization debt explicit.
