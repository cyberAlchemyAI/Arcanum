# Context Pack - Reference/TDD/Math Validation Scaffold

Task: first implementation-readiness task from
`development/invoke-runs/20260612T123402Z-baselines-tdd-math-validation/RUNTIME-HANDOFF.md`.

## Selected Sources

- `OPEN-QUESTIONS-DECISION-LEDGER.md`: V0 baseline decisions.
- `FORMAL-MATH-SPEC.md`: proof targets.
- `INVOKE-PLAN.md`: wave plan and stop conditions.
- `RUNTIME-HANDOFF.md`: first task session scope.

## Controlling Constraints

- Implement reference/tests only.
- No Triton kernel.
- No CAP2 novelty claim.
- No FP16 performance benchmark.
- No full FFN backward.
- Do not claim gradient through hard Top2 selection.

## Local Environment

- `torch`: not installed.
- `pytest`: not installed.

Consequence: this session implements a standard-library reference harness and
`unittest` tests. PyTorch-specific work remains pending until dependencies are
available.

## Gate Verdict

`pass-with-substitution`: the task can proceed with a pure Python oracle and
finite-difference validation. PyTorch autograd/gradcheck is recorded as follow-up.
