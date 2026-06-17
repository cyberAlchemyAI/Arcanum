# Runtime Handoff - Baselines, TDD, Math Validation

Run id: `20260612T123402Z-baselines-tdd-math-validation`

## Objective

Execute the first implementation-readiness task session:

```text
Build the PyTorch reference/TDD harness and math-validation scaffold before any
Triton implementation.
```

## Required Inputs

- `INVOKE-DEFINE.md`
- `INVOKE-DESIGN.md`
- `INVOKE-PLAN.md`
- `research/triton-top2-backward-kernel/OPEN-QUESTIONS-DECISION-LEDGER.md`
- `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md`
- `research/triton-top2-backward-kernel/PRIOR-ART-MAP.md`
- `research/triton-top2-backward-kernel/NOVELTY-SEARCH-MAP.md`

## First Task Session Scope

Implement reference/tests only:

1. contract tests;
2. V0 fixed-mask PyTorch reference;
3. autograd/finite-difference gradient checks;
4. initial math theorem stubs or proof notes;
5. at least soft-routing baseline.

Out of scope:

- Triton kernel;
- CAP2 novelty claim;
- FP16 performance benchmark;
- full FFN backward.

## Completion Criteria

- tests can be run locally;
- V0 fixed-mask baseline is a working oracle;
- no test claims hard Top2 differentiability;
- next CAP2 design gap is explicit.
